# StitchSprites
Python program that takes a folder of separate sprites and packs them into a sprite sheet.

# Process
In the given example.py this program completes the following process:

1) Loads images from user's specified folder into ImageBatch object. 

2) ImageBatch.batch_process(ImageBatch.find_borders) is used to find borders in each image.
3) ImageBatch.minmax_borders() is then used to find the most optimal borders, that will not cut off a part of a sprite.

4) To crop images ImageBatch.crop_image along with the result from 3rd step is passed to ImageBatch.batch_process().

5) Finally, the cropped sprites are put together in a single file with ImageBatch.stitch(). The created image can be saved with ImageBatch.save().
![Resulting image]()
