import numpy as np
import re
from sklearn.decomposition import PCA
import scipy.io as scio


class SWCutil:
    swcdata = []

    # 返回一个双边的闭区间
    def __init__(self, path):
        self.swcdata = self.read_swc(path)

    @staticmethod
    def my_range(start, stop, step):
        list = []
        i = start
        if step > 0:
            while i <= stop:
                list.append(i)
                i = i + step
        elif step < 0:
            while i >= stop:
                list.append(i)
                i = i + step
        return list

    @staticmethod
    def my_pca(X):
        mean_X = np.mean(X, axis=0)
        X -= mean_X
        U, S, V = np.linalg.svd(X, full_matrices=False)
        U *= S
        # V = np.transpose(V)  #matlab 和 python中的SVD分解后，二者的V互为转置
        maxind = np.argmax(np.abs(np.transpose(V)), axis=0)
        d1 = V.shape[0]
        d2 = V.shape[1]
        colsign = np.sign(V.reshape(-1)[maxind + SWCutil.my_range(0, (d2 - 1) * d1, d1)])
        # U = U * colsign
        U = U * colsign
        return U

    def read_swc(self, path):
        file = open(path, 'r')
        j = 0
        r = file.readlines()
        swcFile = []
        for line in r:
            if line[0] == '#' or line == '\n' or line == '\r\n':
                continue
            else:
                line = line.strip('\n')
                point = line.split(" ")
                for p in point:
                    if p == '':
                        point.remove('')
                for i in range(0, len(point)):
                    point[i] = float(point[i])
                point = np.array(point)
                if j == 0:
                    swcFile = point
                else:
                    swcFile = np.vstack((swcFile, point))
                j = j + 1

        file.close()
        return swcFile

    def draw_point(self, im, pt1, radius, ntype):
        height = im.shape[0]
        width = im.shape[1]
        x = max(min(pt1[0], width), 1)
        y = max(min(pt1[1], height), 1)
        for i in SWCutil.my_range(-radius, radius, 1):
            for j in SWCutil.my_range(-radius, radius, 1):
                if (i * i + j * j) ** 0.5 <= radius:
                    xtmp = int(max(min(round(x + i), width), 1)) - 1
                    ytmp = int(max(min(round(y + j), height), 1)) - 1
                    # im[ytmp, xtmp] = 255
                    if im[ytmp, xtmp] < ntype:
                        im[ytmp, xtmp] = ntype
        return im

    def draw_line(self, im, pt1, pt2):
        height = im.shape[0]
        width = im.shape[1]
        startx = max(min(pt1[0], width), 1)
        starty = max(min(pt1[1], height), 1)
        endx = max(min(pt2[0], width), 1)
        endy = max(min(pt2[1], height), 1)

        stridex = endx - startx
        stridey = endy - starty

        if abs(stridex) > abs(stridey):
            vstep = np.sign(endx - startx)
            if vstep != 0:
                for i in SWCutil.my_range((startx + vstep), endx, vstep):
                    j = (i - startx) / stridex * stridey + starty
                    im[int(round(j)) - 1, int(round(i)) - 1] = 1
        elif abs(stridex) < abs(stridey):
            vstep = np.sign(endy - starty)
            if vstep != 0:
                for j in SWCutil.my_range(starty + vstep, endy, vstep):
                    i = (j - starty) / stridey * stridex + startx
                    im[int(round(j)) - 1, int(round(i)) - 1] = 1
        im[int(round(starty)) - 1, int(round(startx)) - 1] = 1
        im[int(round(endy)) - 1, int(round(endx)) - 1] = 1
        return im

    def draw_mat(self, height, width):
        # swcFile = self.read_swc(path)
        coordinate = self.swcdata[:, 2:5]
        pca_point = self.my_pca(coordinate)

        max_p = np.amax(pca_point, axis=0)
        min_p = np.amin(pca_point, axis=0)

        temp = (max_p + min_p) / 2
        new_point = np.array([pca_point[i] - temp for i in range(0, len(pca_point))])
        fw = width
        minv = np.amin(new_point, axis=0)
        maxv = np.amax(new_point, axis=0)
        w = np.amax(np.abs(maxv - minv))
        new_point = new_point * fw / w + fw / 2
        rads = np.maximum(np.round(self.swcdata[:, 5] * fw / w), 1)

        images = np.zeros((height, width, 3), dtype=np.double)

        for i in range(0, len(new_point)):
            images[:, :, 0] = self.draw_point(images[:, :, 0], new_point[i, [0, 1]], rads[i], self.swcdata[i][1])
            images[:, :, 1] = self.draw_point(images[:, :, 1], new_point[i, [0, 2]], rads[i], self.swcdata[i][1])
            images[:, :, 2] = self.draw_point(images[:, :, 2], new_point[i, [1, 2]], rads[i], self.swcdata[i][1])

        for i in range(1, len(new_point)):
            j = int(self.swcdata[i, 6])
            if j == -1:
                continue
            ii = int(i)
            j = j - 1
            images[:, :, 0] = self.draw_line(images[:, :, 0], new_point[j, [0, 1]], new_point[ii, [0, 1]])
            images[:, :, 1] = self.draw_line(images[:, :, 1], new_point[j, [0, 2]], new_point[ii, [0, 2]])
            images[:, :, 2] = self.draw_line(images[:, :, 2], new_point[j, [1, 2]], new_point[ii, [1, 2]])

        return images
