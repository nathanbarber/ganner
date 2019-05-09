import cv2
import numpy as np

class Packer:
    def __init__(self, path):
        self.image = cv2.imread(path)

    def info(self):
        print(type(self.image))
        print(np.shape(self.image))

    def get_data(self):
        return self.image

    def get_shape(self):
        return np.shape(self.image)
    
    def provide_chunk(self, px, py, offsetx, offsety):
        shape = np.shape(self.image)
        y_limit = int(np.floor(py * shape[0]))
        x_limit = int(np.floor(px * shape[1]))

        _slice = []
        for y in range(y_limit):
            y_slice = self.image[offsety + y]
            xy_slice = []
            for x in range(x_limit):
                xy_slice.append(y_slice[offsetx + x])
            _slice.append(xy_slice)
        print(np.shape(y_slice))
        self.current_chunk = np.array(_slice)
        return self.current_chunk

    def provide_center_fixed(self, sl):
        shape = np.shape(self.image)
        # sl is in pixels
        y_st = int(np.floor((shape[0] / 2) - (sl / 2)))
        x_st = int(np.floor((shape[1] / 2) - (sl / 2)))
        _slice = []
        for y in range(sl):
            y_slice = self.image[y_st + y]
            xy_slice = []
            for x in range(sl):
                xy_slice.append(y_slice[x_st + x])
            _slice.append(xy_slice)
        print(np.shape(_slice))
        self.current_chunk = np.array(_slice)
        return self.current_chunk

    def get_chunk(self):
        return self.current_chunk

    def write_chunk(self, path):
        cv2.imwrite(path, self.current_chunk)
        return True

    def one_hot(self, rng, val):
        one_hot = [ 0 for x in range(rng)]
        one_hot[val - 1] = 1
        return one_hot

    def fract(self, sl):
        shape = np.shape(self.image)
        # sl is in pixels
        y_st = int(np.floor(np.random.randint(0, shape[0] - sl)))
        x_st = int(np.floor(np.random.randint(0, shape[1] - sl)))
        _slice = []
        for y in range(sl):
            y_slice = self.image[y_st + y]
            xy_slice = []
            for x in range(sl):
                xy_slice.append(y_slice[x_st + x])
            _slice.append(xy_slice)
        print(np.shape(_slice))
        self.current_chunk = np.array(_slice)
        return self.current_chunk