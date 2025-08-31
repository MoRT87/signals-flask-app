import cv2
import os
from pdf2image import convert_from_path
import numpy as np
import re
import shutil
import time
from google import genai
from google.genai import types
import PIL.Image
from pydantic import BaseModel

expression = re.compile(r"STA[\.,]?\s\d+\+[\d\.]+", re.IGNORECASE)
ocr_config = r"--oem 3 --psm 6"


async def extract_signals_from_file(file_path, output_folder="uploads"):
    """
    Extracts signals from an image or pdf file.
    Args:
        file_path (str): Path to the image or pdf file.
    Returns:
        list: A list of extracted signals.
    """

    async def extract_rectangles_and_text(image):

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Rango extendido para amarillo con plumón (incluso desgastado)
        lower_yellow = np.array([15, 70, 70])
        upper_yellow = np.array([45, 255, 255])

        # Crear máscara de color amarillo
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Aplicar operaciones morfológicas para limpiar ruido
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Buscar contornos en la máscara
        contours, _ = cv2.findContours(
            mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        tasks = []
        rects = []
        thumbnails_dir = os.path.join("uploads", "thumbnails")
        os.makedirs(thumbnails_dir, exist_ok=True)
        timestamp = int(time.time())
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 10 and h > 10:  # filter small rectangles
                roi = image[y : y + h, x : x + w]
                roi_filename = f"roi_{x}_{y}_{w}_{h}_{timestamp}.png"
                roi_path = os.path.join(output_folder, roi_filename)
                cv2.imwrite(roi_path, roi)
                # Copiar a thumbnails para acceso persistente
                thumbnail_path = os.path.join(thumbnails_dir, roi_filename)
                shutil.copy2(roi_path, thumbnail_path)
                rects.append((x, y, w, h, roi_filename))
                

        results = await ocr_with_gemma(map(lambda x: os.path.join(output_folder, x[4]), rects),)
        for rect, signal in zip(rects, results):
            x, y, w, h, roi_filename = rect
            signals.append(
                {
                    "station": signal["station"],
                    "reference": signal["reference"],
                    "rect": (x, y, w, h),
                    "information": signal["information"],
                    # Miniatura persistente
                    "image_path": f"/thumbnails/{roi_filename}",
                }
            )
        return signals

    signals = []
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        image = cv2.imread(file_path)
        if image is not None:
            signals = await extract_rectangles_and_text(image)
    elif file_ext == ".pdf":
        pages = convert_from_path(file_path)
        for page in pages:
            image = np.array(page)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            signals.extend(await extract_rectangles_and_text(image))

    return signals


class SignalSchema(BaseModel):
    station: str
    reference: str
    information: str
    def __getitem__(self, item):
        return self.dict().get(item)


async def ocr_with_gemma(
    image_paths: list[str], model: str = "gemini-2.5-flash"  # "google/gemma-3-4b",
) -> SignalSchema:
    # try:
 

    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
    instruct = "You are a OCR focused AI assistant and provide the information extracted from the image. " \
        "Please provide the station, reference, and information. " \
        "examples: " \
        "station: 1234+5678" \
        "reference: 700-1-12" \
        "information: Rest of the information text on the image with station and reference."
    
    # image = genai.types.Image(image_path)

    config = types.GenerateContentConfig(response_mime_type="application/json", response_schema=list[SignalSchema], system_instruction=instruct)
    resp = client.models.generate_content(model=model, contents=[*map(lambda x: PIL.Image.open(fp=x), image_paths)], config=config)
    return resp.parsed
