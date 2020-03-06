"""Find all png image files within a top level directory"""
import os
import logging
# import pathlib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def find_all_png(parent_directory):
    """Finds all image files under top level directory
        Returns a list of the directory path following
        a list of .png files the directory contains

    [“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]
    list of paths ,[files], path, [files]
    """

    parent_path = os.path.abspath(parent_directory)
    directory_items = os.listdir(parent_directory)

    logger.debug(f"Current Dir: {parent_path}")
    logger.debug(f"directory_items: {directory_items}")

    png_files = [item for item in directory_items
                 if os.path.isfile(os.path.join(parent_path, item))
                 and ".png" in item]

    subdirectories = [os.path.join(parent_path, item) for item in directory_items
                      if os.path.isdir(os.path.join(parent_path, item))]

    logger.debug(f"png_items: {png_files}")
    logger.debug(f"directories: {subdirectories}")

    # NOTE
    # Could try os.walk()

    result = [parent_path, png_files]
    for directory in subdirectories:
        result += find_all_png(directory)

    return result


if __name__ == "__main__":
    print(find_all_png(r"picture_data"))
