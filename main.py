from typing import List
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

# takes a batch of sprites, crops them and stiches them into a single image
class ImageBatch():
    root = ""
    paths = []

    def __init__(self, dir: str):
        self.root = dir
        self.paths = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    
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
    
    def show_image(self, image_arr):
        """
        Show image on screen.
        image_arr - Numpy array representation of image
        """
        plt.imshow(image_arr)
        plt.axis('off')
        plt.show()

    def get_BG_color(self, image: Image = None):
        """
        Returns the (probable) background color of image
        TODO: This is a trivial. It just works.
        """
        keepImageOpen = True
        if image == None:
            image_path = self.get_image_path(0)
            image = self.load_image(image_path)
            keepImageOpen = False
        color = image.getpixel((0, 0))

        if keepImageOpen == False:
            image.close()
        return color
    
    def batch_process(self, image_fn: function, args: tuple = ()) -> list:
        """
        Does a batch processing on images.
        Returns a list of values from the process function.
        image_fn - Function that accepts Image object as an argument.
        args - Other arguments for the function.
        """
        values = []
        for path in self.paths:
            full_path = self.get_image_path(path)
            image = self.load_image(full_path)
            values.append(image_fn(image), *args) # TODO run tests
            image.close()
        return values
    
    def find_borders(self, image: Image) -> tuple:
        """"
        Takes a single image and returns borders of the figure.
        image - PIL image to find borders for.
        """
        # doesn't work correctly in Palette mode, so its changed to RGB
        rgb_image = image.convert('RGB')
        bg_color = self.get_BG_color(rgb_image)
        image_arr = np.array(rgb_image)
        print(type(image_arr))
        mask = np.all(image_arr != bg_color, axis=-1)

        indices = np.argwhere(mask)
        print(indices)
        if len(indices) > 0:
            # Get the bounding box of the region
            min_x, min_y = indices.min(axis=0) # TODO not enough to unpack: expected 2, got 1
            max_x, max_y = indices.max(axis=0)
            # Return the coordinates of the rectangular region
            return min_x, min_y, max_x, max_y
        # Return None if no matching region is found
        return None
    
    def mask_pixels(self, image: Image, bg_color = tuple):
        pass

    def crop(self, x: int, y: int, x_len: int, y_len: int):
        # crops all images in region
        pass


    def find_borders_todo(self, bg_color) -> tuple:
        # goes through images
        # finds characters location

        # for each path
        # find first pixel with non-bg color
        # then find last pixel

        # compare with last results
        # update if x, y is closer to 0
        # update if x + w, y + h is bigger
        x, y, w, h = -1

        # TO DO without numpy this will be slow
        for path in self.paths:
            image = np.array(self.load_image(path))
            mask = np.all(image != bg_color, axis=-1)
            #w, h = image.size
            #for x in range(w):
            #    for y in range(h):
            #        color = self.get_BG_color()
            #image.close()
        return (1, 2, 3, 4)
    
    def stitch():
        pass

def test_img_show(images: ImageBatch):
    img_path = images.get_image_path(0)
    img = np.array(images.load_image(img_path))
    images.show_image(img)

def test_find_borders_in_one_image(images: ImageBatch):
    img_path = images.get_image_path(0)
    img =images.load_image(img_path)
    borders = images.find_borders(img)
    print(borders)

def main(dir: str):
    images = ImageBatch(dir)
    test_find_borders_in_one_image(images)
    #borders = images.batch_process(images.find_borders)
    #crop_region = images.find_borders(bg_color)
    #cropped_images = images.crop(*crop_region)

if __name__ == "__main__":
    # some parameters
    # TO DO add argparse, so the program can be used from CMD
    FOLDER = 'NecoStory'
    DIR = os.path.join(os.getcwd(), FOLDER)
    main(DIR)