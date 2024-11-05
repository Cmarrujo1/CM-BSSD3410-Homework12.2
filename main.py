from PIL import Image, ImageOps
import math

def convolve(img, sz, step):
    start = math.floor(sz / 2)
    con_pixels = []
    for x in range(start, img.size[0] - 1, step):
        for y in range(start, img.size[1] - 1, step):
            tl = img.getpixel((y - 1, x - 1))
            tc = img.getpixel((y - 1, x))
            tr = img.getpixel((y - 1, x + 1))
            lc = img.getpixel((y, x - 1))
            cc = img.getpixel((y, x))
            rc = img.getpixel((y, x + 1))
            bl = img.getpixel((y + 1, x - 1))
            bc = img.getpixel((y + 1, x))
            br = img.getpixel((y + 1, x + 1))

            sum = tl * 3 + tc * 10 + tr * 3 + lc * 0 + cc * 0 + rc * 0 + bl * -3 + bc * -10 + br * -3
            y_ave = math.floor(sum)

            sum = tl * 3 + tc * 0 + tr * -3 + lc * 10 + cc * 0 + rc * -10 + bl * 3 + bc * 0 + br * -3
            x_ave = math.floor(sum)

            top_left_sum = tl * -3 + tc * -10 + tr * -3 + lc * 0 + cc * 0 + rc * 0 + bl * 3 + bc * 10 + br * 3
            top_ave = math.floor(top_left_sum)

            left_right_sum = tl * -3 + tc * 0 + tr * 3 + lc * -10 + cc * 0 + rc * 10 + bl * -3 + bc * 0 + br * 3
            left_ave = math.floor(left_right_sum)

            final_ave = 0
            if x_ave != 0:
                final_ave += abs(x_ave)
            if y_ave != 0:
                final_ave += abs(y_ave)
            if top_ave != 0:
                final_ave += abs(top_ave)
            if left_ave != 0:
                final_ave += abs(left_ave)

            # Clamp final_ave to range 0-255
            final_ave = max(0, min(255, final_ave))
            con_pixels.append(final_ave)

    dims = (math.floor(img.size[0] / step) - 1, math.floor(img.size[1] / step) - 1)
    output = Image.new('L', dims)
    output.putdata(con_pixels)
    output.show()

def main():
    og_image = Image.open("demo.png")
    gray_image = ImageOps.grayscale(og_image)
    gray_image.show()
    convolve(gray_image, 3, 2)

if __name__ == "__main__":
    main()
