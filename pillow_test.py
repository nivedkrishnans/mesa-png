from PIL import Image

height = 400
width = 400
image = Image.new(mode='RGBA', size=(height, width), color=(0,0,0,255))

inlet = Image.new(mode='RGBA', size=(200, 400), color=(0,0,255,0))
image.paste((255,0,0,255),(0,120,400,240))

mask = Image.new(mode='RGBA', size=(200, 400), color=(255,255,255,157))

#image.paste(inlet,(0,0,200,400),)
image.paste((255,255,255,255),(200,0,400,400),mask)
#image.paste((0,0,255,255),(200,0,400,400),mask)

image.show()