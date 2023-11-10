from typing import List
from PIL import Image
import os

# takes a batch of sprites, crops them and stiches them into a single image

class ImageBatch():
    root = ""
    paths = []

    def __init__(self, dir: str):
        self.root = dir
        self.paths = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    
    def crop(self, x: int, y: int, x_len: int, y_len: int):
        # crops all images in region
        pass

    def find_borders(self):
        # goes through images
        # finds characters location
        for path in self.paths:
            image = self.load_image(path)
            w, h = image.size()
            for x in range(w):
                for y in range(h):
                    color = self.get_BG_color()
            image.close()

    def get_BG_color(self):
        # figures out the color of background
        # TO DO this is a trivial implementation
        image = self.load_image(0)
        color = image.getpixel((0, 0))
        image.close()
        return color

    def load_image(self, identifier: any) -> Image:
        if type(identifier) == int: # identifier is a index number
            image_path = self.get_path(identifier)
        elif type(identifier) == str: # identifier is path
            image_path = identifier
        return Image.open(image_path)
    
    def get_path(self, index: int) -> str:
        return os.path.join(self.root, self.paths[index])



def main(dir: str):
    images = ImageBatch(dir)
    bg_color = images.get_BG_color()


if __name__ == "__main__":
    # some parameters
    # TO DO add argparse, so the program can be used from CMD
    FOLDER = 'NecoStory'
    DIR = os.path.join(os.getcwd(), FOLDER)
    main(DIR)