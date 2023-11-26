# StitchSprites
Python program that takes a folder of separate sprites and packs them into a sprite sheet.

1. [Example process](#example-process)
2. [ImageBatch methods](#imagebatch-methods)
3. [Arguments](#arguments)

# Example process
In the given example.py this program completes the following process:

1) Loads images from user's specified folder into ImageBatch object. 

2) ImageBatch.batch_process(ImageBatch.find_borders) is used to find borders in each image.

![Resulting image](https://github.com/alisev/StitchSprites/blob/master/example%20images/borders.png)

3) ImageBatch.minmax_borders() is then used to find the most optimal borders, that will not cut off a part of a sprite.

![Resulting image](https://github.com/alisev/StitchSprites/blob/master/example%20images/optimal_border.png)

![Resulting image](https://github.com/alisev/StitchSprites/blob/master/example%20images/optimal_borders_2.png)

4) To crop images ImageBatch.crop_image along with the result from 3rd step is passed to ImageBatch.batch_process().

5) Finally, the cropped sprites are put together in a single file with ImageBatch.stitch(). The created image can be saved with ImageBatch.save().

![Resulting image](https://github.com/alisev/StitchSprites/blob/master/output/sprite_sheet.png)


# ImageBatch methods
## __init__
Initializes the object by assigning values to ImageBatch.root, ImageBatch.paths and ImageBatch.bg_color.

Parameters:
* dir: string
    - Path to folder of sprites.
* bg_color: {tuple, None}, optional
    - Background color used in sprites. If it is set as None, then program will find it on its own.
* sort_natural: bool, optional
    - Specifies if folder's contents need to be sorted.

## __load_filenames
Used during object initiation. Loads all filenames from given directory dir into a list. Will sort them, if argument natural_sort is set to True.

Parameters:
* 

## __set_bg_color
Used during object initiation. 
Picks background color from an image or uses the one passed by user.

## get_image_path
Combines ImageBatch.root with given identifier to image path into a single filepath.

## show_image
Shows image.

## batch_process
A function that accepts any other ImageBatch method as an argument and processes all images with it.

## find_borders
Finds borders of a sprite in a single image.

## minmax_borders
Takes a list of borders generated by find_borders and finds the largest space that can contain the sprite.

## crop_image
Crops image with given border values.

## stitch
Creates empty canvas and places all cropped sprites in it.

## save
Saves image.

## __progress_message
Shows how many images have been processed. Used by batch_process.

## __get_pixel_mask
Overlays ImageBtach.bg_color over image's pixels and creates a mask. Used by find_borders.

# Arguments
## to be added....
