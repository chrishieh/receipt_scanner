import cv2 
import pytesseract

def process_image(image):
    img = cv2.imread('/home/cshieh/receipt_scanner/IMG_0522.jpg')

    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    receipt_items = pytesseract.image_to_string(img, config=custom_config).splitlines()
    return receipt_items