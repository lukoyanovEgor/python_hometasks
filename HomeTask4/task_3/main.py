import math
import struct
import os

import numpy as np
import matplotlib.pyplot as plt

# BMP format structures ------------------------------------------------------------------------------------------------
# BITMAPFILEHEADER struct in Windows OS
bitmap_file_header = {
    'file_type': 19778,         # (u_short) It must be 'BM' or '0x42 0x4D' in hexadecimals for compatibility reasons.
    'file_size': 0,             # (u_int)   This value is basically the number of bytes in a BMP image file.
    'reserved_1': 0,            # (u_short) It should be initialized to '0' integer (unsigned) value.
    'reserved_2': 0,            # (u_short) Same as the above.
    'pixel_data_offset': 62     # (u_int)   It is the number of bytes between start of the file (0) and the first
                                #           byte of the pixel data.
}  # Total size = 14 bytes

# BITMAPINFOHEADER struct in Windows OS
bitmap_info_header = {
    'header_size': 40,          # (u_int)   It should be '40' in decimal to represent BITMAPINFOHEADER header type.
    'image_width': 0,           # (s_int)   An integer (signed) representing the width of the final image in pixels.
    'image_height': 0,          # (s_int)   An integer (signed) representing the height of the final image in pixels.
    'planes': 1,                # (u_short) The number of color planes of the target device. Should be '1' in decimal.
    'bits_per_pixel': 8,        # (u_short) It is number of bits a pixel takes (in pixel data) to represent a color.
    'compression': 0,           # (u_int)   Should be '0' in decimal to represent no-compression.
    'image_size': 0,            # (u_int)   Should be '0' in decimal when no compression algorithm is used.
    'x_pixels_per_meter': 0,    # (s_int)   Should be set to '0' in decimal to indicate no preference.
    'y_pixels_per_meter': 0,    # (s_int)   Same as the above.
    'total_colors': 2,          # (u_int)   If this is set to '0' in decimal: 2^BitsPerPixel colors are used.
    'important_colors': 0       # (u_int)   Generally ignored by setting '0' decimal value.
}  # Total size = 40 bytes

# COLORTABLE struct in Windows OS
color_table = {
    'red_ent0': 255,            # (u_char) Red color channel density for pure white color.
    'green_ent0': 255,          # (u_char) Green color channel density for pure white color.
    'blue_ent0': 255,           # (u_char) Blue color channel density for pure white color.
    'reserved_ent0': 0,         # (u_char) Reserved for other uses.

    'red_ent1': 0,              # (u_char) Red color channel density for pure black color.
    'green_ent1': 0,            # (u_char) Green color channel density for pure black color.
    'blue_ent1': 0,             # (u_char) Blue color channel density for pure black color.
    'reserved_ent1': 0,         # (u_char) Reserved for other uses.
}  # Total size = 8 bytes


# End of BMP format structures -----------------------------------------------------------------------------------------


def calc_x(rad):
    """Calc abscissa values"""
    return 16 * math.pow(math.sin(rad), 3)


def calc_y(rad):
    """Calc ordinate values"""
    return 13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)


def scale_and_shift(array, scale):
    """Scale and shift points of the picture"""

    new_array = []
    for el in array:
        new_array.append(round(el * scale))

    max_array_val = max(new_array) if max(new_array) > abs(min(new_array)) else abs(min(new_array))

    for i in range(len(array)):
        new_array[i] += max_array_val

    max_array_val = max(new_array)

    return new_array, max_array_val


def create_pixel_data(width, height, x, y, offset):
    """Create white background = width x height and then puts pixels values there"""

    array = []
    # paint the background white
    for i in range(height):
        array.append([0] * width)

    # put there black pixels
    for j in range(len(x)):
        array[int(y[j] + offset)][int(x[j] + offset)] = 1

    return array


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # ---> create figure points
    x = []
    y = []
    for deg in np.arange(0.0, 360.0, 0.1):
        x.append(calc_x(math.radians(deg)))
        y.append(calc_y(math.radians(deg)))

    # --->  scale point values and shift (0,0) point in left bottom angle
    x_pixels, x_width = scale_and_shift(x, 10)
    y_pixels, y_height = scale_and_shift(y, 10)

    # ---> create pixels matrix and pack it into byte array with paddings
    # add +20 white pixel horizontally and vertically and shift figure to the picture center
    offset = 20
    x_width += offset
    y_height += offset
    pixels_matrix = create_pixel_data(x_width, y_height, x_pixels, y_pixels, offset/2)

    padding = 0
    pixels_data = []
    for i in range(y_height):
        pixels_data.append(struct.pack(f'<{x_width}B', *pixels_matrix[i]))

        while (x_width + padding) % 4 != 0:
            padding += 1

        if padding != 0:
            pixels_data.append(struct.pack(f'<{padding}B', *(padding*[0])))

    # --->  create an BMP-image
    file = open('picture.bmp', 'wb')

    # fill empty lines in BMP structures
    bitmap_file_header['file_size'] = bitmap_file_header['pixel_data_offset'] + x_width * y_height + padding*y_height
    header = struct.pack('<HI2HI', bitmap_file_header['file_type'],
                         bitmap_file_header['file_size'],
                         bitmap_file_header['reserved_1'],
                         bitmap_file_header['reserved_2'],
                         bitmap_file_header['pixel_data_offset'])
    file.write(header)

    bitmap_info_header['image_width'] = x_width
    bitmap_info_header['image_height'] = y_height
    info = struct.pack('<3I2H6I', bitmap_info_header['header_size'],
                       bitmap_info_header['image_width'],
                       bitmap_info_header['image_height'],
                       bitmap_info_header['planes'],
                       bitmap_info_header['bits_per_pixel'],
                       bitmap_info_header['compression'],
                       bitmap_info_header['image_size'],
                       bitmap_info_header['x_pixels_per_meter'],
                       bitmap_info_header['y_pixels_per_meter'],
                       bitmap_info_header['total_colors'],
                       bitmap_info_header['important_colors'])
    file.write(info)

    pallet = struct.pack('<8B', color_table['red_ent0'],
                         color_table['green_ent0'],
                         color_table['blue_ent0'],
                         color_table['reserved_ent0'],
                         color_table['red_ent1'],
                         color_table['green_ent1'],
                         color_table['blue_ent1'],
                         color_table['reserved_ent1'])
    file.write(pallet)

    for el in pixels_data:
        file.write(el)
    file.close()

    # --->  plot the initial picture
    plt.plot(x, y)
    plt.xlabel(r'$f_1(t) = 16sin(t)^3$')
    plt.ylabel(r'$f_2(t) = 13cos(t)-5cos(2t)-2cos(3t)-cos(4t)$')
    plt.title(r'$f_1(t), f_2(t), t = [0; 2PI]$')
    plt.grid(True)
    plt.show()

    # --->  open picture
    os.system("picture.bmp")
