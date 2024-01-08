import sys

import os
from re import split
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from progress.bar import Bar

# Adapted from https://github.com/alisev/StitchSprites by alisev

class ImageBatch():
    root = ""
    paths = []

    def __init__(self, dir: str, sort_natural: bool = True):
        self.root = dir
        self.paths = self.__load_filenames(dir, sort_natural)

    def __is_png(self, file : str) -> bool:
        """
        Checks if a file is a png. This allows non-png
        files in the given directory without causing
        the program to crash.
        """
        return file.endswith(".png")
    
    def __load_filenames(self, dir: str, sort_natural: bool = True) -> list:
        """
        Loads all filenames found in directory dir.
        Natural sorting takes number order into account, 
        e.g. 1_000.bmp, 2_000.bmp, 10_000.bmp instead of 
        1_000.bmp, 10_000.bmp, 2_000.bmp.
        """
        paths = filter(self.__is_png, os.listdir(dir))
        if sort_natural:
            natural_sort_key = lambda s: [int(text) if text.isdigit() else text.lower() for text in split('([0-9]+)', s)]
            return sorted(paths, key = natural_sort_key)
        return paths

    def get_image_path(self, identifier: any) -> str:
        """
        Returns full image path from given identifier.
        identifier - some value that represents a specific path
        - if int is given, then function assumes its a index of self.paths element
        - str is path itself
        """
        if type(identifier) == int:
            image_path = self.paths[identifier]
        elif type(identifier) == str:
            image_path = identifier
        else:
            raise TypeError(self.__err_TypeError_message(identifier, [int, str]))
        return os.path.join(self.root, image_path)
    
    def show_image(self, image: Image):
        """
        Show image on screen.
        """
        image_arr = np.array(image)
        plt.imshow(image_arr)
        plt.axis('off')
        plt.show()
    
    def batch_process(self, image_fn, args: tuple = ()) -> list:
        """
        Does a batch processing on images.
        Returns a list of values from the process function.
        image_fn - Function that accepts Image object as an argument.
        args - Other arguments for the function.
        """
        values = []
        bar = Bar(f"{image_fn.__name__}", max = len(self.paths))
        for i in range(len(self.paths)):
            full_path = self.get_image_path(self.paths[i])
            image = Image.open(full_path)
            value = image_fn(*(image, *args))
            values.append(value)
            image.close()
            bar.next()
        bar.finish()
        return values

    def __scoot(self, A, rev=False):
        """
        Takes an array A and returns the index of the first non-trivial
        enty. If rev is True, instead returns the index of the last
        non-trivial entry.
        A - a list
        rev - True reverses direction of search
        """
        if rev:
            direction = -1
            index = len(A) - 1
        else:
            direction = 1
            index = 0
        if not A:
            return float('inf') * direction

        while not A[index]:
            index += direction
        return index
    
    def find_borders(self, image: Image) -> tuple:
        """"
        Takes a single image and returns borders of the sprite.
        Returns a tuple of bounding box or None if sprite is not found.
        image - PIL image to find borders for.
        """
        proj =  image.getchannel("A").getprojection()
        minx, maxx = self.__scoot(proj[0]), self.__scoot(proj[0], rev = True)
        miny, maxy = self.__scoot(proj[1]), self.__scoot(proj[1], rev = True)
        return (minx, miny, maxx, maxy)
    
    def minmax_borders(self, borders: list, ideal: bool=False) -> tuple:
        """
        Takes a list of borders (tuples) and finds the largest area they cover.
        Requirements:
        - lowest min_x and min_y values,
        - and highest max_x and max_y
        borders - list of found borders.
        """
        borders_arr = np.array(borders)
        mins = np.min(borders_arr, axis=0)
        maxs = np.max(borders_arr, axis=0)

        if not ideal:
            return mins[0], mins[1], maxs[2], maxs[3]

        # Ideally, width and height will be powers of two
        width = maxs[2] - mins[0]
        height = maxs[3] - mins[1]
        niceWidth = 1
        niceHeight = 1
        while niceWidth < width:
            niceWidth *= 2
        while niceHeight < height:
            niceHeight *= 2
        minx = mins[0] - (niceWidth - width)//2
        miny = mins[1] - (niceHeight - height)//2
        maxx = minx + niceWidth
        maxy = miny + niceHeight
            
        return minx, miny, maxx, maxy
    
    def crop_image(self, image: Image, min_x: int, min_y: int, max_x: int, max_y: int) -> Image:
        """
        Crops image with given parameters
        """
        return image.crop([min_x, min_y, max_x, max_y])

    def stitch(self, images: list, x: int, y: int) -> Image:
        """
        Combines images into single file.
        images - List of images to be stitched together
        x, y - Describes how many images there should be along x and y axis.
        """
        # Make the system smarter. Perhaps save multiple files
        # if x and y are too small.
        image_size = images[0].size
        canvas = image_size[0] * x, image_size[1] * y
        new_image = Image.new('RGBA', canvas, 0)
        for i in range(x):
            for j in range(y):
                p = x * j + i
                if(p >= len(images)):
                    break
                new_x, new_y = image_size[0] * i, image_size[1] * j
                new_image.paste(images[p], (new_x, new_y))
        return new_image
    
    def save_image(self, image: Image, name: str):
        """
        Saves image to drive.
        """
        save_dir = os.path.join(os.getcwd(), name)
        image.save(save_dir)
        print(f"Image {name} saved!")

    def __err_TypeError_message(self, var: any, fn, expected_types: list) -> str:
        """
        Returns text for TypeError message.
        """
        return f"Wrong value type for variable in {fn.__name__}! Expected {expected_types}, got {type(var)}."


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Usage: ImageBatch directory [out] [cols] [rows]")
            sys.exit(1)

        FOLDER = sys.argv[1]
        DIR = os.path.join(os.getcwd(), FOLDER)

        COLS, ROWS = 8, 1
        OUTPUT = "spriteSheet.png"

        if len(sys.argv) >= 3:
            OUTPUT = sys.argv[2]

        if len(sys.argv) >= 4:
            if sys.argv[3].isdigit():
                COLS = int(sys.argv[3])
            else:
                print("cols must be an integer")
                sys.exit(1)

        if len(sys.argv) >= 5:
            if sys.argv[4].isdigit():
                ROWS = int(sys.argv[4])
            else:
                print("rows must be an integer")
                sys.exit(1)

        images = ImageBatch(DIR)
        border_list = images.batch_process(images.find_borders)
        optimal_borders = images.minmax_borders(border_list)
        cropped_images = images.batch_process(images.crop_image, optimal_borders)
        stitched_img = images.stitch(cropped_images, COLS, ROWS)
        images.save_image(stitched_img, OUTPUT)
    except TypeError as e:
        print(e)
