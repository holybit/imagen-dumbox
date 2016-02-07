#!/usr/bin/env python

import argparse
import dicom
from dicom.errors import InvalidDicomError
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
# from shutil import copy2
import sys
import tempfile


def dcm_attrs_select(dataset):
    """Dump select DICOM attributes/elements
    """

    print("Storage type.....:", dataset.SOPClassUID)

    pat_name = dataset.PatientName
    display_name = pat_name.family_name + ", " + pat_name.given_name
    print("Patient's name...:", display_name)
    print("Patient id.......:", dataset.PatientID)
    print("Modality.........:", dataset.Modality)
    print("Study Date.......:", dataset.StudyDate)


def dcm_attrs(args, dataset):
    """Dump DICOM attributes/elements
    """

    if args.all:
        print(dataset.file_meta)
        print(dataset)
    elif args.abbreviated:
        dcm_attrs_select(dataset)


def dcm_pixel_data(dataset):
    """Return DICOM pixel_data

       Currently, bit shifts 12 bit to 8 bit which causes a reduction
       in image quality as there seems no way for PIL to handle 16 bit
       numpy uint16 arrays.
    """
    pixel_data = dataset.pixel_array

    # np.set_printoptions(formatter={'int': hex}, edgeitems=10000)
    # np.set_printoptions(edgeitems=10)

    # Right shift bits, 12 -> 8
    # pixel_data >>= 4
    # pixel_data = np.array(pixel_data, dtype='uint8')
    # print pixel_data.dtype
    # print pixel_data.dtype.byteorder

    # Left shift bits, 12 -> 16
    # pixel_data <<= 4
    # pixel_data = np.array(pixel_data, dtype='uint8')

    return pixel_data


def mod_pixel_data(pixel_data):
    """Modify DICOM pixel_data

       Returns:
           im: modified image
    """
    im = Image.fromarray(pixel_data, 'I;16')
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("FreeSerif.ttf", 50)
    draw.text((200, 20), "Lorem Ipsum", (255, 255, 255), font=font)

    # Note, im.save(foo.jpg) will fail on uint16 numpy data. No work
    # around could be found which limits viewing modified image

    return im


def dcm_clone(dcm_file, dataset, pixel_data, image):
    """Clone DICOM file with pixel_data as PIL image

       Clones are nearly exact but some traits will differ. In this case
       the DICOM pixel_data will differ in addition to modifying some
       DICOM object attributes.

       Args:
           dcm: DICOM file name as passed CLI -f
           image: DICOM pixel_data modified
    """
    file_name = os.path.basename(dcm_file)
    tmp_file_name = file_name + '-'
    tf = tempfile.NamedTemporaryFile(prefix=tmp_file_name, delete=False)
    # copy2(dcm_file, tf.name)

    # dataset = dcm_read(tf.name)
    im_array = np.asarray(image, dtype='uint16')
    # print im_array.dtype
    # print im_array.dtype.byteorder
    dataset.PixelData = im_array.tobytes()
    dataset.save_as(tf.name)

    # If PixelData is bit modified set the following appropriatley
    # dataset.BitsAllocated = 8
    # dataset.BitsStored    = 8
    # dataset.HighBit       = 7


def dcm_read(dcm_file):
    """Read DICOM file

       Returns:
           pydicom dataset
    """

    if not os.path.isfile(dcm_file):
        print('No such file: ' + dcm_file)
        sys.exit(1)

    # Parse DICOM file
    try:
        dataset = dicom.read_file(dcm_file)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit(1)
    except InvalidDicomError:
        print "Not a valid DICOM file"
        sys.exit(1)

    return dataset


def main(argv):
    parser = argparse.ArgumentParser(
        prog='dumbox.py', description="Process DICOM file i.e., dcm/DCM")
    parser.add_argument('-a', '--all', action='store_true',
                        help='All DCM file object attributes')
    parser.add_argument('-b', '--abbreviated', action='store_true',
                        help='Select DCM file object attributes')
    parser.add_argument('-c', '--clone', action='store_true',
                        help='Clone DCM file')
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument(
        '-f', '--file', help='DICOM file', required=True)

    args = parser.parse_args()
    dataset = dcm_read(args.file)
    dcm_attrs(args, dataset)
    if args.clone:
        pixel_data = dcm_pixel_data(dataset)
        image = mod_pixel_data(pixel_data)
        dcm_clone(args.file, dataset, pixel_data, image)

if __name__ == "__main__":
    main(sys.argv)
