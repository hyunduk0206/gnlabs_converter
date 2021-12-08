import os
from PIL import Image
import numpy as np
from pypcd import pypcd


def to_png(file):
    out = file.replace(".jpg", ".png")
    img = Image.open(file)
    png = img.save(out, format="PNG", compress_level=0, interlace=False)
    img.close()
    os.remove(file)


def to_bin(file):
    pc = pypcd.PointCloud.from_path(file)

    ## Get data from pcd (x, y, z, intensity)
    np_x = (np.array(pc.pc_data["x"], dtype=np.float32)).astype(np.float32)
    np_y = (np.array(pc.pc_data["y"], dtype=np.float32)).astype(np.float32)
    np_z = (np.array(pc.pc_data["z"], dtype=np.float32)).astype(np.float32)
    np_i = (np.array(pc.pc_data["intensity"], dtype=np.float32)).astype(
        np.float32
    ) / 256

    ## Stack all data
    points_32 = np.transpose(np.vstack((np_x, np_y, np_z, np_i)))

    ## Save bin file
    out = file.replace(".pcd", ".bin")
    points_32.tofile(out)

    os.remove(file)


def to_kitti():
    pass


dict = {"jpg": [to_png, "jpg"], "pcd": [to_bin, "pcd"], "json": [to_kitti, "json"]}
