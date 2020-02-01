import os
import errno
import argparse

import numpy as np
import matplotlib.pyplot as plt
from mtcnn import MTCNN

from window_method import crop

def main():
    parser = argparse.ArgumentParser(
        description="Crop image of desired -dim (width, height) at -src path and save to -dst path with face centered"
    )
    parser.add_argument("src", help="input jpg image path")
    parser.add_argument("-dst", help="cropped output image path, default: src path with _cropped tag", default='')
    parser.add_argument("aspect_ratio", help="aspect ratio to maintain for cropping, format-> eg. 1:2")

    args = parser.parse_args()

    input_file_path = args.src
    output_file_path = args.dst
    aspect_ratio = args.aspect_ratio
    aspect_ratio = aspect_ratio.strip().split(':')
    m, n = int(aspect_ratio[0]), int(aspect_ratio[1])

    if output_file_path == '':
        output_file_path = input_file_path[:-4]+'_cropped.jpg'


    aspect_ratio = m/float(n)

    if os.path.exists(args.src) is False:
        raise FileNotFoundError(
    errno.ENOENT, os.strerror(errno.ENOENT), args.src)
    else:
        image  = plt.imread(input_file_path)

    detector = MTCNN()
    results = detector.detect_faces(image)
    confidences = [result['confidence'] for result in results]
    index = np.argmax(confidences)
    x1, y1, ww, hh = results[index]['box']
    h, k = x1+ww//2, y1+hh//2
    image = crop(image, (h, k), aspect_ratio)

    plt.imsave(output_file_path, image)

    print("Job Completed")

if __name__ == '__main__':
    main()