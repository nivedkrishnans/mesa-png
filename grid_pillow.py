'''
This program takes a database output of the MyxoColi model and exports images for each step.
Uses the Pillow package
'''
import os
from datetime import datetime
from sqlalchemy import create_engine, MetaData
import random
from PIL import Image
import sys
import math

initial_time = datetime.now() #recording initial time for benchmarking

current_dir = os.path.dirname(os.path.realpath(__file__)) #directory of this program
input_dir = os.path.join(current_dir,'input') #input directory for experimenting
input_file = os.path.join(input_dir, 'test9.sqlite3') #input sqlite3 database for experimenting




def create_output_dir(input_db):
    #this function creates the output directory and returns its name
    output_dir = os.path.splitext(input_db)[0]
    output_dir_exists = os.path.exists(output_dir)
    #Adds '_1' to the output directory name if it alreadt exists
    if output_dir_exists:
        while output_dir_exists:
            output_dir = output_dir + '_1'
            output_dir_exists = os.path.exists(output_dir)
    os.makedirs(output_dir)
    return output_dir


def visualise_grid(input_db, steps=1, patch_size=16,dimensions=(0,0), LBAPatch=True, Myxo=True, Coli=True):
    '''
    This function takes a database representing a myxocoli run and exports the steps
    as individual images.
    Parameters:
        input_db : path to sqlite3 database from a myxocoli run
        steps : The step number (integer) or a list of step numbers (integer list)
        patch_size : The number of pixels along each side of a patch
        dimensions : Tuple containing the width and height of the model.
                    If not provided, will be calculated assuming the model is a square.
        LBAPatch, Myxo, Coli : Whether or not these agents should appear in the output
    
    '''
    print('Started rendering image for database ', input_db)
    print('Steps to be rendered: ', steps)

    #Conncecting to the database
    try:
        engine = create_engine('sqlite:///' + input_db, echo=False)
        conn = engine.connect()
        meta = MetaData()
        meta.reflect(bind = engine)
    except Exception as e:
        print(e)

    tables = meta.tables #gets the tables from the databse as a dictionary
    table_names = tables.keys() #the keys of the dictionary stored in 'tables' are the table names
    patch_table_names = [table for table in table_names if 'Patch' in table] #chooses only the tables that have the word Patch in them, i.e., the LBAPatch tables
    myxo_table_names = [table for table in table_names if 'Myxo' in table] #chooses only the tables that have the word Patch in them, i.e., the LBAPatch tables
    coli_table_names = [table for table in table_names if 'Coli' in table] #chooses only the tables that have the word Patch in them, i.e., the LBAPatch tables
    total_steps = len(patch_table_names)

    #Making sure the steps parameter is valid
    #If the steps is an integer, it is converted to a single element integer list
    #If the steps is a list, all elements are tested whether they are integers of the right range
    if type(steps) == int:
        steps = [steps]
    if type(steps) == list:
        if max(steps) < total_steps and min(steps)>=0:
            for i in steps:
                if type(i) != int:
                    sys.exit("Invalid steps argument. Invalid element of type " + str(stype(i)))
        else:
            sys.exit("Invalid steps argument. Out of range.")
    else:
        sys.exit("Invalid steps argument. Invalid type." + str(type(steps)))

    #Creating the output directory with the same name as input_db
    output_dir = create_output_dir(input_db)
    print('Output directory created:',output_dir)


    #These masks will be used when overlaying all the grid cells onto the initial plain image
    solid_mask = Image.new(mode='RGBA', size=(patch_size, patch_size), color=(255,255,255,255))
    transparent_mask = Image.new(mode='RGBA', size=(patch_size, patch_size), color=(255,255,255,127))



    for step in steps:

        patch_table = tables[patch_table_names[step]]
        print(patch_table)
        s = patch_table.select()
        all_patches = conn.execute(s)
        all_patches = list(all_patches)
        total_patches = len(all_patches)
        
        if total_patches != dimensions[0]*dimensions[1]:
            if dimensions[0]*dimensions[1] == 0: #i.e. dimensions argument was not provided so default (0,0) used
                dimensions = (int(math.sqrt(total_patches)),int(math.sqrt(total_patches)))
                if total_patches != dimensions[0]*dimensions[1]:
                    sys.exit("Patch number not a perfect square for automatic dimensions calculation. Step ", step)
            else:
                sys.exit("Dimensions and patch number does not match. Step " + str(step))

        #Creating the image object
        width = dimensions[0] * patch_size
        height = dimensions[1] * patch_size
        image = Image.new(mode='RGBA', size=(width, height), color=(0,0,0,255))

        
        if LBAPatch:
            for patch in all_patches:
                patch_color = patch_color_generate(patch[3])
                position = (patch_size*patch[1],patch_size*patch[2],patch_size*(patch[1]+1),patch_size*(patch[2]+1))
                image.paste(patch_color,position,solid_mask)
        
        image.save(os.path.join(output_dir,'step_'+f'{step:06}'+'.png'))
            



def patch_color_generate(energy,default=10, extreme=40,alpha=False):
    #This function returns the color corresponding to the value (energy)
    #of a property of a patch, i.e., a grid box
    normal_color = (255,255,255,255)
    fractional_energy = energy/default
    if fractional_energy < 0:
        color =  (0,0,0,255)
    elif 0 <= fractional_energy <= 1:
        temp = int(fractional_energy*255)
        color = (temp,temp,temp,255)
    else:
        if extreme == default:
            color = (255,0,0,255)
        extra = (energy - default)/(extreme - default)
        if extra > 1 :
            color = (0,255,0,255)
        elif extra > 0:
            color = (int(255*(1-extra)),0,0,255)
        else: 
            color = (0,0,255,255)

    return color
    





final_time = datetime.now()

print('Total time for whole program ', (final_time - initial_time) )

