import cv2
import os
from pdf2image import convert_from_path
import numpy as np

import pytesseract
import re

expression = re.compile(r"STA[\.,]?\s\d+\+[\d\.]+", re.IGNORECASE)
ocr_config = r"--oem 3 --psm 6"


def extract_signals_from_file(
    file_path,
    rotation=None,
    enhance=True,
    noise_reduction=True,
    adaptive_thresholding=True,
    aggressive_upsampling=True,
    auto_best_transformation=True,
    max_scale=16,
):
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
        threshold = None
        signals = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 10 and h > 10:  # filter small rectangles
                roi = image[y : y + h, x : x + w]
                # Save each ROI in a new file
                roi_filename = f"roi_{x}_{y}_{w}_{h}.png"
                match (int(rotation)):
                    case 90:
                        roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
                    case 180:
                        roi = cv2.rotate(roi, cv2.ROTATE_180)
                    case 270:
                        roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)

                # Enhance image for OCR
                if enhance:
                    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # Apply bilateral filter for noise reduction
                if noise_reduction:
                    roi = cv2.bilateralFilter(roi, 9, 75, 75)

                # Apply adaptive thresholding
                if adaptive_thresholding:
                    roi = cv2.adaptiveThreshold(
                        roi,
                        255,
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY,
                        11,
                        2,
                    )

                # Apply a bit more aggressive thresholding after upscaling

                # Detect the best transformation for OCR
                if aggressive_upsampling:
                    _, roi = cv2.threshold(
                        roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                    )

                if auto_best_transformation:
                    threshold = detect_best_transformation(roi, max_scale)
                    if threshold:
                        roi = cv2.resize(
                            roi,
                            None,
                            fx=threshold if threshold else 1,
                            fy=threshold if threshold else 1,
                            interpolation=cv2.INTER_LINEAR,
                        )

                cv2.imwrite("uploads/" + roi_filename, roi)
                # roi = cv2.threshold(roi, 150 if (threshold== None) else threshold[0], 255 if (threshold== None) else threshold[1], cv2.THRESH_BINARY)[1]

                text = pytesseract.image_to_string(roi, config=ocr_config).replace(
                    "\n", " "
                )

                signals.append(
                    {
                        "rect": (x, y, w, h),
                        "text": text,
                        "title": expression.findall(text),
                        "size": roi.shape,
                        "image_path": roi_filename,
                        "scale": threshold,
                    }
                )
                # Draw rectangle for debugging
            # cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
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


# function to detect the best image transformation for OCR
def detect_best_transformation(image, max_scale):
    """
    Detects the best image threshold values for OCR by searching for a specific pattern.
    Args:
        image (numpy.ndarray): Input image.
    Returns:
        tuple: (threshold1, threshold2) values.
    """

    for k in np.arange(max_scale + 1, 0, -1):
        if k not in [1, 8, 16, 32]:
            continue
        transformed = cv2.resize(
            image, None, fx=k, fy=k, interpolation=cv2.INTER_LINEAR
        )
        text = pytesseract.image_to_string(transformed, config=ocr_config)
        result = expression.findall(text)
        print(result, k, len(result) > 0)
        if len(result) > 0:
            return k

    return None
