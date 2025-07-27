import cv2
import os
from pdf2image import convert_from_path
import numpy as np

import pytesseract


def extract_signals_from_file(file_path):
    """
    Extracts signals from an image or pdf file.
    Args:
        file_path (str): Path to the image or pdf file.
    Returns:
        list: A list of extracted signals.
    """

    def extract_rectangles_and_text(image):

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

      
        signals = []
        debug_image = image.copy()
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 10 and h > 10:  # filter small rectangles
                roi = image[y : y + h, x : x + w]
                # Elimina el color amarillo fuera del rectángulo usando la máscara
                roi_mask = cv2.bitwise_not(mask_cleaned[y : y + h, x : x + w])
                roi = cv2.bitwise_not(roi, roi, mask=roi_mask)

                # Save each ROI in a new file
                roi_filename = f"roi_{x}_{y}_{w}_{h}.png"
                
                # Upscale ROI for better OCR
                roi = cv2.resize(roi, None, fx=16, fy=16, interpolation=cv2.INTER_CUBIC)

                # Enhance and rotate image
                roi = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY)[1]
                roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)

                cv2.imwrite("uploads/" + roi_filename, roi)

                # Recognize text in any direction using Tesseract's OCR engine mode and orientation/segmentation mode
                custom_config = r"--oem 3"
                text = pytesseract.image_to_string(roi, config=custom_config)
                signals.append(
                    {
                        "rect": (x, y, w, h),
                        "text": text.strip().replace("\n", " "),
                        "image_path": roi_filename,
                    }
                )
                # Draw rectangle for debugging
                cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return signals

    signals = []
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        image = cv2.imread(file_path)
        if image is not None:
            signals = extract_rectangles_and_text(image)
    elif file_ext == ".pdf":
        pages = convert_from_path(file_path)
        for page in pages:
            image = np.array(page)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            signals.extend(extract_rectangles_and_text(image))

    return signals
