import argparse
import cv2
import numpy as np
import os
def trim_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image.shape[-1] == 4:
        mask = image[:, :, 3] > 0
    else:
        mask = np.any(image != image[0, 0], axis=-1)
    coords = np.argwhere(mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    cv2.imwrite(image_path, image[y0:y1, x0:x1])
def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".jpg", ".png")):
                trim_image(os.path.join(root, file))
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    if os.path.isdir(args.input):
        process_directory(args.input)
    else:
        trim_image(args.input)
