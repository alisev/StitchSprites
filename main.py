import os
from re import split

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

# takes a batch of sprites, crops them and stiches them into a single image
class ImageBatch():
    root = ""
    paths = []
    bg_color = ()

    def __init__(self, dir: str):
        self.root = dir
        self.paths = sorted(os.listdir(dir), key = self.__natural_sort_key)
        self.bg_color = self.__get_BG_color()

    def __natural_sort_key(self, s):
        """
        Sorts fielnames numerically.
        """
        return [int(text) if text.isdigit() else text.lower() for text in split('([0-9]+)', s)]
    
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
        return os.path.join(self.root, image_path)
    
    def load_image(self, image_path: str) -> Image:
        """
        Loads image as a PIL Image object.
        image_path - full path to image
        """
        return Image.open(image_path)
    
    def show_image(self, image: Image):
        """
        Show image on screen.
        """
        image_arr = np.array(image)
        plt.imshow(image_arr)
        plt.axis('off')
        plt.show()

    def __get_BG_color(self) -> tuple:
        """
        Returns the (probable) background color of image
        TODO: This is a trivial. It just works.
        """
        image_path = self.get_image_path(0)
        image = self.load_image(image_path).convert('RGB')
        color = image.getpixel((0, 0))
        image.close()
        return color
    
    def batch_process(self, image_fn, args: tuple = (), every: int = 50) -> list:
        """
        Does a batch processing on images.
        Returns a list of values from the process function.
        image_fn - Function that accepts Image object as an argument.
        args - Other arguments for the function.
        """
        values = []
        print("Processing images...")
        for i in range(len(self.paths)):
            full_path = self.get_image_path(self.paths[i])
            image = self.load_image(full_path)
            value = image_fn(*(image, *args))
            values.append(value)
            image.close()
            if i % every == 0:
                print(f"{i}/{len(self.paths)} images processed.")
        return values
    
    def find_borders(self, image: Image) -> tuple:
        """"
        Takes a single image and returns borders of the figure.
        Returns a tuple of bounding box or None if figure is not found.
        image - PIL image to find borders for.
        """
        # TODO needs some way to see previous values and compare
        # doesn't work correctly in Palette mode, so its changed to RGB
        mask = self.__get_pixel_mask(image)
        indices = np.argwhere(mask)
        if len(indices) > 0:
            min_y, min_x = indices.min(axis=0)
            max_y, max_x = indices.max(axis=0)
            return min_x, min_y, max_x, max_y
        return None
    
    def minmax_borders(self, borders: list) -> tuple:
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
        return mins[0], mins[1], maxs[2], maxs[3]
    
    def __get_pixel_mask(self, image: Image) -> np.ndarray:
        """
        For each pixel returns True if it belongs to the figure and False for background.
        image - PIL Image
        """
        rgb_image = image.convert('RGB')
        image_arr = np.array(rgb_image)
        return np.all(image_arr != self.bg_color, axis=-1)

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
        image_size = images[0].size
        canvas = image_size[0] * x, image_size[1] * y
        new_image = Image.new('RGB', canvas, self.bg_color)
        for i in range(x):
            for j in range(y):
                p = x * j + i
                if(p >= len(images)):
                    break
                images[p].convert('RGB')
                new_x, new_y = image_size[0] * i, image_size[1] * j
                new_image.paste(images[p], (new_x, new_y))
        return new_image
    
    def save_image(self, image: Image, name: str):
        """
        Saves image to drive.
        """
        save_dir = os.path.join(os.getcwd(), "output", name)
        image.save(save_dir)
        print(f"Image {name} saved!")

if __name__ == "__main__":
    # some parameters
    # TO DO add argparse, so the program can be used from CMD
    FOLDER = 'NecoStory'
    DIR = os.path.join(os.getcwd(), FOLDER)
    X_ROWS, Y_ROWS = 10, 10

    images = ImageBatch(DIR)
    all_borders = images.batch_process(images.find_borders)
    crop_borders = images.minmax_borders(all_borders)
    cropped_images = images.batch_process(images.crop_image, crop_borders)
    stitched_img = images.stitch(cropped_images, X_ROWS, Y_ROWS)
    images.save_image(stitched_img, "sprite_sheet.png")
        

