import pytesseract
import cv2


def find_text(filename):
    img = cv2.imread(filename, 0)
    text = pytesseract.image_to_string(img, lang="eng+mar+san+hin+fra")
    text = text.split("\n")
    r_text = []
    for line in text:
        if not line.isspace():
            if line != "\n":
                r_text.append(line)
    text = "\n".join(r_text)
    return text