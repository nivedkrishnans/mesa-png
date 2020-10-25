from PIL import Image
import random
from datetime import datetime
import os

initial_time = datetime.now() #recording initial time for benchmarking

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(current_dir,'output',)

#The side length of each grid cell
grid_size = 10

#The number of cells horizonally and vertically
x = 10
y = 10

#Pixel dimensions of the image
width = grid_size*x
height = grid_size*y

#The image object which will be manipulated as required. Initially plain black.
image = Image.new(mode='RGBA', size=(width, height), color=(0,0,0,255))

#This image will be overlayed on the grid
agent_image = Image.open(os.path.join(current_dir,'resources','1.png'))

#Adding some padding to the agent_image so that the patch is visible behind it
#First a transparent temp_image is created
#Then the agent_image is resized to 75% of height and width of a grid box, and pasted 12.5% from the edges of temp_image
#The resulting temp_image is stored back into agent_image
temp_image = Image.new(mode='RGBA', size=(grid_size, grid_size), color=(0,0,0,0))
temp_image.paste(agent_image.resize((int(grid_size*3/4),int(grid_size*3/4))),(int(grid_size/8),int(grid_size/8)))
agent_image = temp_image

agent_image.show()


#These masks will be used when overlaying all the grid cells onto the initial plain image
solid_mask = Image.new(mode='RGBA', size=(grid_size, grid_size), color=(255,255,255,255))
transparent_mask = Image.new(mode='RGBA', size=(grid_size, grid_size), color=(255,255,255,127))

for i in range(x):
    for j in range(y):
        inlet = (0,0,0,255)
        position = (grid_size*i,grid_size*j,grid_size*(i+1),grid_size*(j+1))
        #image.paste(inlet,position,transparent_mask)
        if random.choice([0,1]):
            image.paste(agent_image,position,agent_image)

image.save(os.path.join(output_dir,str(initial_time)+'.png'))

final_time = datetime.now()

print('Total time for whole program ', (final_time - initial_time) )

