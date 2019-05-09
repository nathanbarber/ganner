from net import Ganner
from im_proc import Packer
import tensorflow as tf
import os

source_files = os.listdir(".source")
packers = []
print(source_files)

for file in source_files:
    packers.append(
        Packer(".source/{}".format(file))
    )

num = 0
for p in packers:
    print(p.get_shape())
    if len(p.get_shape()) != 0:
        for i in range(5):
            p.fract(300)
            num += 1
            p.write_chunk(".gan_source/{}.JPG".format(num))

gn = Ganner(300, 10000, 1000, ".gan_source/")
print(gn.choose_batch(4))
gn.Generate()