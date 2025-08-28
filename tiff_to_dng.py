import argparse
from PIL import Image
from pidng.core import RAW2DNG
from pidng.dng import DNGTags, Tag
from pidng.defs import DNGVersion
import numpy as np
import os
import xml.etree.ElementTree as ET

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

    # Convert image to numpy array and ensure it's uint16
    image_data = np.asarray(image).astype(np.uint16)

    # Create DNG tags
    tags = DNGTags()
    tags.set(Tag.ImageWidth, [image.width])
    tags.set(Tag.ImageLength, [image.height])

    # Determine bits per sample from the image mode
    mode_to_bpp = {
        '1': 1, 'L': 8, 'P': 8, 'RGB': 8, 'RGBA': 8, 'CMYK': 8, 'YCbCr': 8,
        'I': 32, 'F': 32, 'I;16': 16, 'I;16B': 16, 'I;16L': 16,
    }
    bpp = 16 # default to 16 bit
    if image.mode in mode_to_bpp:
        bpp = mode_to_bpp[image.mode]
    tags.set(Tag.BitsPerSample, [bpp] * len(image.getbands()))
    if len(image.getbands()) > 1:
        tags.set(Tag.SamplesPerPixel, [len(image.getbands())])


    # Add metadata from TIFF info
    if 'xmp' in image.info:
        xmp_data = image.info['xmp']
        # The XMP data is a byte string, decode it to string
        xmp_str = xmp_data.decode('utf-8', 'ignore')
        # Find the start of the XML
        xml_start = xmp_str.find('<x:xmpmeta')
        if xml_start != -1:
            xmp_str = xmp_str[xml_start:]
            try:
                root = ET.fromstring(xmp_str)
                ns = {
                    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                    'xmp': 'http://ns.adobe.com/xap/1.0/',
                    'crs': 'http://ns.adobe.com/camera-raw-settings/1.0/',
                    'photoshop': 'http://ns.adobe.com/photoshop/1.0/',
                }

                create_date = root.find('.//xmp:CreateDate', ns)
                if create_date is not None:
                    tags.set(Tag.DateTimeOriginal, create_date.text)

                modify_date = root.find('.//xmp:ModifyDate', ns)
                if modify_date is not None:
                    tags.set(Tag.DateTime, modify_date.text)

                raw_file_name = root.find('.//crs:RawFileName', ns)
                if raw_file_name is not None:
                    tags.set(Tag.OriginalRawFileName, os.path.basename(raw_file_name.text))

                camera_profile = root.find('.//crs:CameraProfile', ns)
                if camera_profile is not None:
                    tags.set(Tag.ProfileName, camera_profile.text)

            except ET.ParseError as e:
                print(f"Error parsing XMP data: {e}")

    # Add some default tags
    tags.set(Tag.Software, "tiff-to-dng converter")
    tags.set(Tag.DNGVersion, DNGVersion.V1_4)
    tags.set(Tag.DNGBackwardVersion, DNGVersion.V1_0)


    # Use pidng to convert to DNG
    try:
        dng = RAW2DNG()
        output_dir = os.path.dirname(args.output_file)
        if not output_dir:
            output_dir = "."
        dng.options(tags, output_dir)
        output_filename = os.path.basename(args.output_file)
        dng.convert(image_data, filename=output_filename)
        print(f"Successfully converted {args.input_file} to {args.output_file}")
    except Exception as e:
        print(f"Error converting to DNG: {e}")


if __name__ == '__main__':
    main()
