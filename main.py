import cv2
import numpy as np
import pytesseract

def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def recognize_number_plate(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    config = '--psm 7'
    text = pytesseract.image_to_string(invert, config=config)
    return cleanup_text(text)

def detect_and_ocr(image_path):
    img = cv2.imread(image_path)
    anpr = PyImageSearchANPR()
    text = anpr.find_and_ocr(img)
    return text

class PyImageSearchANPR:
    def __init__(self, minAR=4, maxAR=5, debug=False):
        self.minAR = minAR
        self.maxAR = maxAR
        self.debug = debug

    def find_and_ocr(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        candidates = self.find_license_plate_candidates(gray)
        lp = self.locate_license_plate(gray, candidates)

        if lp is not None:
            options = ""
            lpText = pytesseract.image_to_string(lp, config=options)
            lpText = cleanup_text(lpText)
            return lpText
        else:
            return None

    def find_license_plate_candidates(self, gray):
        pass

    def locate_license_plate(self, gray, candidates):
        pass

if __name__ == "__main__":
    image_path = 'image.jpg'
    number_plate_text = recognize_number_plate(image_path)
    print(number_plate_text)
