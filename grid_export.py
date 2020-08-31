import png
import os
from datetime import datetime
from sqlalchemy import create_engine, MetaData
import random

initial_time = datetime.now()

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(current_dir,'output', str(datetime.now()))

input_dir = os.path.join(current_dir,'input')

input_file = os.path.join(input_dir, 'test_big.sqlite3')

engine = create_engine('sqlite:///' + input_file, echo=False)
conn = engine.connect()
meta = MetaData()
meta.reflect(bind = engine)

tables = meta.tables
table_names = tables.keys()
grid_table_names = [table for table in table_names if 'Patch' in table]

step = 11
a_table = tables[grid_table_names[step]]




# #png part

# grid_size = (10,10,) # number of rows x columns
# pixel_size = 4
# bitdepth = 8
# channels = 3 #R,G,B

def export_png_grid(table, width, height, title='output', pixel_size=16, bitdepth=8, alpha=False):
    print('Started rendering image for table ', title)
    #Takes a table from the database, and exports it into a png
    #width and height are that of the model itself
    #pixel_size is how many pixels represent one side of a patch (i.e., one small grid box)

    #The tables are obtained from meta.tables (make use of keys() of this to get what you want)
    
    initial_time = datetime.now()

    #Getting all patched in the grid
    s = table.select()
    all_patches = conn.execute(s)

    #If the alpha channel is used, 4 channels will be used, otherwise 3
    channels = 4 if alpha else 3

    #this_grid is an array that shall be used for holding the color info
    #By default, it will hold rgb(0,0,0) values, that is, all pixels are black
    #The png file is stored as a list of lists
    #The inner lists represent rows in the image. They contain the channels of each pixel
    #For example, [[0,0,0, 255,102,16],[123,21,23, 12,69,147]] has 2 pixels only in the rgb mode
    this_grid = []
    for i in range(height):
        for j in range(pixel_size):
            row = [0]* width * channels * pixel_size
            this_grid.append(row)

    #Looping through the patches and changing the colors appropriately
    #The table here has 4 columns - id, x_coordinate, y_coordinate, energy (all are integers)
    for patch in all_patches:
        #Root condition for changing defaults (default values are rgb(0,0,0), i.e. black, everywhere)
        if patch[3]>5:
            #Nested for loops enables scaling a patch to multiple pixels as per 'pixel_size'
            for i in range(pixel_size):
                for j in range(pixel_size):
                    #If the right parameters were not entered, out of bounds exception may occur
                    try:
                        #x_pos and y_pos are the indices in this_grid that represents a patch
                        #The following code makes sure scaling to 'pixel_size' is made possible
                        #Also, depending on presence of an alpha channel, the length can vary
                        x_pos = pixel_size*channels*patch[1]
                        y_pos = pixel_size*patch[2]
                        this_grid[i+y_pos][j*channels + x_pos + 0] = 255
                        this_grid[i+y_pos][j*channels + x_pos + 1] = 0 
                        this_grid[i+y_pos][j*channels + x_pos + 2] = 0
                        #this_grid[i+y_pos][j*channels + x_pos + 3] = 255  #For alpha channel if used
                    except Exception as e:
                        print(e, patch)

    def create_output_dir():
        condition = not os.path.exists(output_dir)
        if condition:
            os.makedirs(output_dir)
        return output_dir


    w = png.Writer(width = pixel_size*width, height = pixel_size*height, greyscale=False, alpha = alpha, bitdepth=bitdepth, )
    f = open(os.path.join(create_output_dir() , title + '.png'), 'wb')

    w.write(f, this_grid)
    f.close()

    final_time = datetime.now()
    print('Time taken to render ', title, (final_time - initial_time), ' for total pixels ', height*width*(pixel_size**2))








for k in range(10):
    a_table = tables[grid_table_names[k]]
    export_png_grid(a_table, 1000, 1000 ,grid_table_names[k], pixel_size=1)


final_time = datetime.now()

print('Total time for whole program ', (final_time - initial_time) )