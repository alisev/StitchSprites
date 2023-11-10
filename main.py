from typing import List
from PIL import Image
from os import listdir
from os.path import isfile, join

# takes a batch of sprites, crops them and stiches them into a single image

class ImageBatch():
    paths = []

    def __init__(self, dir):
        self.paths = [f for f in listdir(dir) if isfile(join(dir, f))]
        print(self.paths)


def main(dir):
    images = ImageBatch(dir)
    pass

if __name__ == "__main__":
    dir = '/NecoStory'
    main(dir)