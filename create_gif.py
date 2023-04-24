import imageio
import os

imgs = []

path = 'imgs/vid_cat/'
filenames = os.listdir(path)
for fname in sorted(filenames, key=lambda name: int(name[:name.find('.')])):
    print(fname)
    imgs.append(imageio.imread(path + fname))
imageio.mimsave('imgs/cat.gif', imgs, fps=36)
