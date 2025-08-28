# TIFF to DNG Converter

## Name

`tiff_to_dng.py` - Converts a TIFF file to a DNG file.

## Synopsis

`python tiff_to_dng.py <input_file> <output_file>`

## Description

This script converts a TIFF image file to a Digital Negative (DNG) file. It preserves the image data and attempts to carry over metadata from the original TIFF file, including date/time information and color profile information.

The script uses the `Pillow` library to read the TIFF file and the `pidng` library to create the DNG file.

## Options

*   `<input_file>`: The path to the input TIFF file.
*   `<output_file>`: The path to the output DNG file.

## Examples

### Basic Conversion

```bash
python tiff_to_dng.py my_image.tif my_image.dng
```

This will convert `my_image.tif` to `my_image.dng` in the same directory.

### Specifying a different output directory

```bash
python tiff_to_dng.py images/my_image.tif converted/my_image.dng
```

This will convert `images/my_image.tif` and save the resulting DNG file to the `converted` directory.

## Dependencies

The script requires the following Python libraries:

*   Pillow
*   pidng
*   numpy

You can install them using pip:

```bash
pip install -r requirements.txt
```
