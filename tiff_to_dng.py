import argparse
from PIL import Image
from pidng.core import RAW2DNG
from pidng.dng import DNGTags, Tag
from pidng.defs import DNGVersion, PhotometricInterpretation
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

    # Create DNG tags for a linear DNG
    tags = DNGTags()
    tags.set(Tag.NewSubfileType, 0) # 0 = Main image
    tags.set(Tag.PhotometricInterpretation, PhotometricInterpretation.Linear_Raw)

    tags.set(Tag.ImageWidth, [image.width])
    tags.set(Tag.ImageLength, [image.height])
    tags.set(Tag.BitsPerSample, [16] * len(image.getbands()))

    if len(image.getbands()) > 1:
        tags.set(Tag.SamplesPerPixel, [len(image.getbands())])

    tags.set(Tag.Software, "tiff-to-dng converter")
    tags.set(Tag.DateTime, "") # Set a default empty value, will be overwritten by XMP if available

    # Add metadata from TIFF info
    if 'xmp' in image.info:
        xmp_data = image.info['xmp']
        xmp_str = xmp_data.decode('utf-8', 'ignore')
        xml_start = xmp_str.find('<x:xmpmeta')
        if xml_start != -1:
            xmp_str = xmp_str[xml_start:]
            try:
                root = ET.fromstring(xmp_str)
                ns = {
                    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                    'xmp': 'http://ns.adobe.com/xap/1.0/',
                    'crs': 'http://ns.adobe.com/camera-raw-settings/1.0/',
                }

                create_date = root.find('.//xmp:CreateDate', ns)
                if create_date is not None:
                    tags.set(Tag.DateTimeOriginal, create_date.text)

                modify_date = root.find('.//xmp:ModifyDate', ns)
                if modify_date is not None:
                    tags.set(Tag.DateTime, modify_date.text)

                camera_profile = root.find('.//crs:CameraProfile', ns)
                if camera_profile is not None:
                    tags.set(Tag.ProfileName, camera_profile.text)

            except ET.ParseError as e:
                print(f"Error parsing XMP data: {e}")

    tags.set(Tag.DNGVersion, DNGVersion.V1_4)
    tags.set(Tag.DNGBackwardVersion, DNGVersion.V1_0)
    tags.set(Tag.UniqueCameraModel, "tiff-to-dng-converter")


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
