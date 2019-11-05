import numpy as np
from scipy.spatial.distance import cdist
import os
root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class searchNeuronServer:
    all_fea = np.array([])
    all_name = np.array([])
    mean = 0
    std = 0
    def __init__(self, all_name_path=root + '/data/feature/allname_sort.npy'):
        self.allname = np.load(all_name_path)
        self.length = np.load(root + '/data/feature/length.npy')
        self.mean = np.load(root + '/data/feature/mean.npy')
        self.std = np.load(root + '/data/feature/std.npy')

    def search(self, test_fea, top=20):
        test_fea = test_fea / self.length
        test_fea = test_fea - self.mean
        test_fea = test_fea / self.std
        all_fea = np.load(root + '/data/feature/feature1.npy')
        dist_matrix = cdist(test_fea, all_fea, metric='euclidean')
        for i in range(2, 7):
            all_fea = np.load(root + '/data/feature/feature'+str(i)+'.npy')
            temp = cdist(test_fea, all_fea, metric='euclidean')
            dist_matrix = np.concatenate((dist_matrix, temp), axis=1)
        del all_fea
        # dist_matrix = np.concatenate((dist_matrix1,dist_matrix2,dist_matrix3), axis=1)
        y = dist_matrix[0].argsort(axis=0)
        a = y[0:top]
        return a, self.allname[a]

