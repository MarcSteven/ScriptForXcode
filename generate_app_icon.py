import argparse
import sys
import os
import cv2
import json


# default resized icon imag format
# could be changed to jpg
RESIZED_ICON_IMAGE_FORMAT = "png"


# utility function to parse scale or scale property of an icon
# for example, size of 20x20 or scale of 2x
def parse_size_or_scale(line):
    end_index = line.rfind('x')
    return float(line[0: end_index])


# main function to generate icon images and update Contents.json
def generate_app_icon(image_file, json_file):
    # extract image basename (without directory path)
    image_file_basename = os.path.splitext(os.path.basename(image_file))[0]

    # extract the directory path of json file to store resized image files
    json_file_dir = os.path.dirname(json_file)

    # read image by OpenCV library
    image = cv2.imread(image_file)
    image_height, image_width, image_channels = image.shape

    # import json file
    with open(json_file, 'r') as in_file:
        json_data = json.load(in_file)

    # get icon images array from json data
    icon_images = json_data['images']

    # use a dictionary to store resized images info to avoid resize again
    resized_image_dict = dict()

    for icon_image in icon_images:
        icon_size = parse_size_or_scale(icon_image['size'])
        icon_scale = parse_size_or_scale(icon_image['scale'])
        actual_icon_size = int(icon_size * icon_scale)
        print("icon size = {}, scale = {}".format(icon_size, icon_scale, actual_icon_size))

        if actual_icon_size in resized_image_dict:
            # if the actual size of icon exists, reuse the same resized image file
            resized_image_filename = resized_image_dict[actual_icon_size]
        else:
            # resize the image file to icon size
            resized_image = cv2.resize(image, (int(actual_icon_size), int(actual_icon_size)))
            resized_image_filename = "{:s}_{:d}.{}".format(image_file_basename, actual_icon_size, RESIZED_ICON_IMAGE_FORMAT)
            # save resized image file to the same directory of json file
            cv2.imwrite(os.path.join(json_file_dir, resized_image_filename), resized_image)
            resized_image_dict[actual_icon_size] = resized_image_filename
            print("Generate icon image: {}".format(resized_image_filename))

        # update filename of icon image data in json file
        icon_image['filename'] = resized_image_filename

    # update json file
    with open(json_file, 'w') as out_file:
        json.dump(json_data, out_file, indent=2)


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='Generate iOS app icon images.')
    parser.add_argument('source_image_file', help='path to source image file')
    parser.add_argument('app_icon_json_file',help='path to Contents.json of Assets.xcassets/AppIcon.appiconset')
    parser.add_argument('--clean', action='store_true', help='delete existing images in Assets.xcassets/AppIcon.appiconset/')
    args = parser.parse_args()

    # check whether files exist or not
    if not os.path.exists(args.source_image_file):
        sys.exit("ERROR: image file {} does not exist !!".format(args.source_image_file))

    if not os.path.exists(args.app_icon_json_file):
        sys.exit("ERROR: json file {} does not exist !!".format(args.app_icon_json_file))

    # delete existing images if needed
    if args.clean:
        json_file_dir = os.path.dirname(args.app_icon_json_file)
        image_files = [filename for filename in os.listdir(json_file_dir)
                        if os.path.splitext(filename)[1] == ".{}".format(RESIZED_ICON_IMAGE_FORMAT)]
        for image_file in image_files:
            os.remove(os.path.join(json_file_dir, image_file))

    # generate app icon images and update json file
    generate_app_icon(args.source_image_file, args.app_icon_json_file)

    print("done.")
