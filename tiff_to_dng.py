#!/usr/bin/env python3

import argparse
from PIL import Image
import numpy as np
import pidng

def main():
    """
    This script converts a TIFF file to a DNG file.
    """
    parser = argparse.ArgumentParser(
        description='Convert a TIFF file to a DNG file.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-i', '--input', required=True, help='Path to the input TIFF file.')
    parser.add_argument('-o', '--output', required=True, help='Path to the output DNG file.')

    # Example of how to add more options in the future
    # parser.add_argument('--compress', action='store_true', help='Enable lossless compression in the DNG file.')

    args = parser.parse_args()

    print(f"Reading TIFF file: {args.input}")

    try:
        img = Image.open(args.input)
        raw_data = np.array(img)
        exif_data = img.info.get('exif')

        print("TIFF file read successfully.")
        print(f"Image shape: {raw_data.shape}")
        if exif_data:
            print("EXIF data found.")
        else:
            print("No EXIF data found.")

    except Exception as e:
        print(f"Error reading TIFF file: {e}")
        return

    print("Creating DNG file...")

    try:
        dng = pidng.DNG()
        dng.write(args.output, raw_data, exif=exif_data)
        print("DNG file created successfully.")

    except Exception as e:
        print(f"Error creating DNG file: {e}")
        return

if __name__ == "__main__":
    main()
