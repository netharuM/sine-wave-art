from draw_image import ImageDrawer

IMAGE_FILE_NAME = 'buddha3.jpg'

img = ImageDrawer(f'images/{IMAGE_FILE_NAME}',
                  wave_height=10,
                  search_box_padding=10
                  )
img.draw()
img.save(f'{IMAGE_FILE_NAME}.ps')
img.done()
