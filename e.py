import argparse
import os
from PIL import Image
def trim_white_border(image_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    data = img.getdata()
    width, height = img.size
    left, right, top, bottom = width, 0, height, 0
    for y in range(height):
        for x in range(width):
            r, g, b, a = data[y * width + x]
            if a != 0 and (r, g, b) != (255, 255, 255):
                left = min(left, x)
                right = max(right, x)
                top = min(top, y)
                bottom = max(bottom, y)
    cropped_img = img.crop((left, top, right + 1, bottom + 1))
    cropped_img.save(image_path)
def get_latest_png_file(directory):
    png_files = [f for f in os.listdir(directory) if f.endswith('.png')]
    if not png_files:
        return None
    latest_file = max(png_files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)
def main():
    parser = argparse.ArgumentParser(description="裁剪PNG图片的白色边框")
    parser.add_argument("image_path", type=str, nargs='?', help="要裁剪的PNG图片的路径")
    args = parser.parse_args()
    if not args.image_path:
        args.image_path = get_latest_png_file('.')
        if not args.image_path:
            print("当前目录中没有找到PNG文件。")
            return
    trim_white_border(args.image_path)
    print(f"已裁剪并覆盖保存: {args.image_path}")
if __name__ == "__main__":
    main()
