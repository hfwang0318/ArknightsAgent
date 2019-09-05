import cv2 

def to_binary(img, inv=False):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if not inv:
        _, img = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY)
    else:
        _, img = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY_INV)
    return img