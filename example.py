from ImageBatch import ImageBatch
import args

import os

if __name__ == "__main__":
    try:
        # some parameters
        # TO DO add argparse, so the program can be used from CMD
        FOLDER = 'NecoStory'
        DIR = os.path.join(os.getcwd(), FOLDER)
        X_ROWS, Y_ROWS = 10, 10

        images = ImageBatch(DIR)
        border_list = images.batch_process(images.find_borders)
        optimal_borders = images.minmax_borders(border_list)
        cropped_images = images.batch_process(images.crop_image, optimal_borders)
        stitched_img = images.stitch(cropped_images, X_ROWS, Y_ROWS)
        images.save_image(stitched_img, "sprite_sheet.png")
    except TypeError as e:
        print(e)
