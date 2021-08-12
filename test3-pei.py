from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mp
from skimage import morphology
from skimage import data
from skimage.exposure import histogram
import os

def get_img(path):
    file_list = []
    row = 0
    for a, b, c in os.walk(path):
        number = len(c)
        for i in range(int(number)):
            temp = c[i].split(".")
            if temp[-1] == "tif":
                names = "".join(c[i])
                names = str(a) + "\\" + str(names)
                file_list.append(names)
    return file_list


def img_segmentation(file_list):
    for each in file_list:
        print (each)
        img = io.imread(each)
        #coins = data.coins()
        hist, hist_centers = histogram(img[:,:,2])

        """
        fig, axes = plt.subplots(1, 2, figsize=(8, 3))
        axes[0].imshow(img, interpolation='nearest')
        axes[0].axis('off')
        axes[1].plot(hist_centers, hist, lw=2)
        axes[1].set_title('histogram of gray values')
        #plt.show()
        """
        '''
        fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
        
        axes[0].imshow(img[:,:,1] > 180, cmap=plt.cm.gray, interpolation='nearest')
        axes[0].set_title('> 150')
        
        axes[1].imshow(img[:,:,0] > 80, cmap=plt.cm.gray, interpolation='nearest')
        axes[1].set_title('> 80')
        
        for a in axes:
            a.axis('off')
        
        plt.tight_layout()
        plt.show()
        '''

        '''
        from skimage.feature import canny
        
        edges = canny(img[:,:,0])
        
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
        ax.set_title('Canny detector')
        ax.axis('off')
        
        
        from scipy import ndimage as ndi
        
        fill_corn = ndi.binary_fill_holes(edges)
        
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(fill_corn, cmap=plt.cm.gray, interpolation='nearest')
        ax.set_title('filling the holes')
        ax.axis('off')
        
        
        from skimage import morphology
        
        corn_cleaned = morphology.remove_small_objects(fill_corn, 21)
        
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(corn_cleaned, cmap=plt.cm.gray, interpolation='nearest')
        ax.set_title('removing small objects')
        ax.axis('off')
        '''

        from skimage.filters import sobel

        elevation_map = sobel(img[:,:,0])

        """
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(elevation_map, cmap=plt.cm.gray, interpolation='nearest')
        ax.set_title('elevation map')
        ax.axis('off')
        """

        markers = np.zeros_like(img[:,:,0])
        markers[img[:,:,0] < 25] = 1
        markers[img[:,:,0] > 130] = 2

        """
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(markers, cmap=plt.cm.nipy_spectral, interpolation='nearest')
        ax.set_title('markers')
        ax.axis('off')
        """

        segmentation = morphology.watershed(elevation_map, markers)
        """
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(segmentation, cmap=plt.cm.gray, interpolation='nearest')
        ax.set_title('segmentation')
        ax.axis('off')
        """
        mp.imsave(".".join(each.split(".")[:-1]) + ".out.png", segmentation)

        #plt.show()

if __name__ == "__main__":
    path = r"H:\2020BJ zili pei\7.19-7.29\B203214\pei"
    file_list = get_img(path)
    img_segmentation(file_list)