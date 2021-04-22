"""dip_hw1.py: Starter file to run howework 1"""
#Example Usage: ./dip_hw1_region_analysis -i imagename.jpg
import cv2
import sys

import matplotlib
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from region_analysis import binary_image as bi
from region_analysis import cell_counting as cc
from compression import run_length_encoding as rle

matplotlib.use('Agg')

__author__ = "Pranav Mantini"
__email__ = "pmantini@uh.edu"
__version__ = "1.0.0"


def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def main():
    """ The main funtion that parses input arguments, calls the approrpiate
     interpolation method and writes the output image"""

    parser = ArgumentParser()
    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")
    args = parser.parse_args()

    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        input_image = cv2.imread(args.image, 0)

    bin_img = bi.BinaryImage()
    hist = bin_img.compute_histogram(input_image)

    output_directory = 'output/cellct/'
    output_directory_compress = 'output/Compression/'

    plt.plot(hist)
    plt.savefig(output_directory+"hist.png")

    threshold = bin_img.find_otsu_threshold(hist)
    print("Optimal threshold: ", threshold)

    binary_img = bin_img.binarize(input_image)
    output_image_name = output_directory + "binary_image" + ".jpg"
    cv2.imwrite(output_image_name, binary_img)

    cell_count_obj = cc.CellCounting()
    regions = cell_count_obj.blob_coloring(binary_img)
    stats = cell_count_obj.compute_statistics(regions)
    cell_stats_img = cell_count_obj.mark_image_regions(binary_img, stats)
    output_image_name = output_directory + "cell_stats" + ".jpg"
    cv2.imwrite(output_image_name, cell_stats_img)

    rle_obj = rle.Rle()
    rle_code = rle_obj.encode_image(binary_img)
    print("-------------- Runlength Code -------------------")
    print(rle_code)

    [height, width] = binary_img.shape
    decoded_image = rle_obj.decode_image(rle_code, height, width)
    output_image_name = output_directory_compress + "decoded_image" + ".jpg"
    cv2.imwrite(output_image_name, decoded_image)


if __name__ == "__main__":
    main()







