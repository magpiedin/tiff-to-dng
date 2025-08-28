import argparse
from PIL import Image
import tifffile
import numpy as np
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Convert a TIFF file to a DNG file.')
    parser.add_argument('input_file', type=str, help='The input TIFF file.')
    parser.add_argument('output_file', type=str, help='The output DNG file.')
    args = parser.parse_args()

    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")

    # Open the TIFF image
    try:
        image = Image.open(args.input_file)
    except IOError:
        print(f"Error: Unable to open file {args.input_file}")
        return

    # Get image data as numpy array
    image_data = np.asarray(image)

    # Get ICC profile
    icc_profile = image.info.get('icc_profile')

    # Get XMP metadata
    xmp_metadata = image.info.get('xmp')

    # Prepare DNG tags
    tags = []
    if xmp_metadata:
        tags.append((700, 's', 0, xmp_metadata, True))

    # Use TiffWriter to write the DNG file
    try:
        with tifffile.TiffWriter(args.output_file) as tif:
            tif.write(
                image_data,
                dng=True,
                iccprofile=icc_profile,
                photometric='rgb',
                extratags=tags
            )
        print(f"Successfully converted {args.input_file} to {args.output_file}")
    except Exception as e:
        print(f"Error converting to DNG: {e}")

if __name__ == '__main__':
    main()
