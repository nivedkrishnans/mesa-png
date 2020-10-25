from grid_pillow import *
import os

current_dir = os.path.dirname(os.path.realpath(__file__)) #directory of this program
input_dir = os.path.join(current_dir,'input') #input directory for experimenting
input_file = os.path.join(input_dir, 'test7.sqlite3') #input sqlite3 database for experimenting


visualise_grid(input_file, steps=list(range(80)), patch_size=16,dimensions=(0,0), LBAPatch=True, Myxo=True, Coli=True)