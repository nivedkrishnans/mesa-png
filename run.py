import png
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(current_dir,'output', str(datetime.now()))

def create_output_dir():
    condition = not os.path.exists(output_dir)
    if condition:
        os.makedirs(output_dir)
    return output_dir


f = open(os.path.join(create_output_dir() ,'ramp.png'), 'wb')

s = []
a = []
print(type(a))
bitdepth = 4
for i in range(2**bitdepth):
    for j in range(2**bitdepth):
        for k in range(2**bitdepth):
            for l in range(2**bitdepth):
                s.append(int(i/2))
                s.append(j)
                s.append(k)
                s.append(l)
        a.append((s))
        s=[]
        print('row ', (j+1), ' completed')

w = png.Writer(width = 4**bitdepth, height = 4**bitdepth, greyscale=False, alpha = True, bitdepth=bitdepth, )
print(a)
w.write(f, a)
f.close()
