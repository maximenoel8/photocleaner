#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import distutils.file_util as utils
import logging
import os
from distutils import dir_util

FORMAT = '[%(levelname)s-%(asctime)-15s]-%(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-o', '--origin', dest='origin', required=True)
    parser.add_argument('-d', '--destination', dest='destination', required=True)
    parser.add_argument('--delete', choices=['yes', 'no'], help='Delete raw file not user', default='no')
    return parser.parse_args()


def get_destination_directory_backup(root, destination_root):
    path_element = root.split("/")
    path_element.pop(0)
    path_element.pop(0)
    for element in path_element:
        destination_directory = destination_root + "/" + element
    return destination_directory


def copy_raw_file(directory, pictures_list, root, destination_directory):
    file_path = root + '/' + directory
    pictures_name_list_with_ext = os.listdir(file_path)
    for row in pictures_name_list_with_ext:
        logging.info(row)
        if row.split(".")[1] != "jpg":
            picture_name = row.split(".")[0]
            if picture_name in pictures_list:
                utils.copy_file(file_path + "/" + row, destination_directory, update=1)


def delete_raw_file(directory, pictures_list, root):
    file_path = root + '/' + directory
    pictures_name_list_with_ext = os.listdir(file_path)
    for row in pictures_name_list_with_ext:
        logging.info(row)
        if row.split(".")[1] != "jpg":
            picture_name = row.split(".")[0]
            if picture_name not in pictures_list:
                logging.info("This row will be delete " + row + "\n")
                os.remove(file_path + "/"+row)


def main():
    parsed_args = parse_arguments()
    logging.info(parsed_args.origin)
    logging.info(parsed_args.destination)
    logging.info(parsed_args.delete)
    for root, dirs, files in os.walk(parsed_args.origin):
        logging.info("\nroot = " + root)
        delete = "no"
        if 'Lightroom' in dirs:
            destination_directory = get_destination_directory_backup(root, parsed_args.destination)
            dir_util.mkpath(destination_directory)
            pictures_name_list_with_ext = os.listdir(root + '/Lightroom')
            pictures_list = []
            for pictures_ext in pictures_name_list_with_ext:
                utils.copy_file(root + "/Lightroom/" + pictures_ext, destination_directory, update=1)
                pictures_list.append(pictures_ext.split(".")[0])
            for directory in dirs:
                if "oitier" in directory:
                    copy_raw_file(directory, pictures_list, root, destination_directory)
                    if delete == "yes":
                        delete_raw_file(directory, pictures_list, root)
            if len(files) != 0:
                for row in files:
                    if row.split(".")[1] != "jpg":
                        picture_name = row.split(".")[0]
                        if picture_name in pictures_list:
                            utils.copy_file(root + "/" + row, destination_directory, update=1)


if __name__ == "__main__":
    main()
