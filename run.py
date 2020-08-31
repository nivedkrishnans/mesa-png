import png
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(current_dir,'output')

def create_output_dir():
    condition = not os.path.exists(output_dir)
    if condition:
        os.makedirs(output_dir)
    return output_dir

create_output_dir()
f = open(os.path.join(output_dir, 'ramp.png'), 'wb')
w = png.Writer(256, 1, greyscale=True)
w.write(f, [range(256)])
f.close()

