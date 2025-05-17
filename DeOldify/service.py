from colorizer import colorizer

source_url = 'https://images.pexels.com/photos/12014080/pexels-photo-12014080.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=279.825&fit=crop&h=453.05' #@param {type:"string"}
render_factor = 35  #@param {type: "slider", min: 7, max: 40}
watermarked = True #@param {type:"boolean"}
def transform_from_url(source_url: str):
    if source_url is not None and source_url !='':
        image_path = colorizer.plot_transformed_image_from_url(url=source_url, render_factor=render_factor, compare=True, watermarked=watermarked)
        print(image_path)
    else:
        print('Provide an image url and try again.')

import os
def transform_from_filepath(filepath: str):
    if filepath is not None and os.path.exists(filepath):
        image_path = colorizer.plot_transformed_image(filepath)
        return image_path
    else:
        print('filepath does not exist')
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# print(ROOT_DIR)
# transform_from_filepath(os.path.join(ROOT_DIR, 'test_images', 'image.png'))
    