from skimage import io
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.image as mp
from skimage import morphology
from skimage import data
from skimage.exposure import histogram
import os


def get_img_tif(path):
	file_list = []
	row = 0
	for a, b, c in os.walk(path):
		number = len(c)
		for i in range(int(number)):
			temp = c[i].split(".")
			if temp[-1] == "jpg":
				names = "".join(c[i])
				names = str(a) + "\\" + str(names)
				file_list.append(names)
	return file_list


def img_segmentation(file_list):
	for each in file_list:
		print(each)
		img = io.imread(each)
		# coins = data.coins()
		hist, hist_centers = histogram(img[:, :, 2])

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

		elevation_map = sobel(img[:, :, 0])

		"""
		fig, ax = plt.subplots(figsize=(4, 3))
		ax.imshow(elevation_map, cmap=plt.cm.gray, interpolation='nearest')
		ax.set_title('elevation map')
		ax.axis('off')
		"""

		markers = np.zeros_like(img[:, :, 0])
		markers[img[:, :, 0] < 35] = 1
		markers[img[:, :, 0] > 100] = 2

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

	# plt.show()


def get_img(path):
    file_list = []
    row = 0
    for a, b, c in os.walk(path):
        number = len(c)

        for i in range(int(number)):
            temp = c[i].split(".")
            if temp[-1] == "png":
                names = "".join(c[i])
                names = str(a) + "\\" + str(names)
                file_list.append(names)
    return file_list

def get_folder(path):
    file_list = []
    row = 0
    for a, b, c in os.walk(path):
        number = len(c)
        if str(a).endswith('2x2xbar'):
	        file_list.append(a)
    return file_list

def areaCal(contour):
	area = []
	for i in range(len(contour)):
		area.append(cv2.contourArea(contour[i]))
	return area

def make_contours(file_list):
	img_dict = {}
	for each in file_list:
		print(each)
		img = cv2.imread(each)
		# 灰度图像
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# 二值化
		ret, binary = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)
		contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# 以圆形框出云朵
		# for i in range(len(contours)):
		# (x, y), radius = cv2.minEnclosingCircle(contours[i])
		# center = (int(x), int(y))
		# radius = int(radius)
		# img = cv2.circle(img, center, radius, (0, 255, 0), 2)

		# 以云朵边界轮廓框出云朵
		cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

		output = areaCal(contours)
		print (output)
		if output:
			img_dict[each] = str(max(output)) + "\t" + str(output)
		else:
			img_dict[each] = str(0) + "\t" + str(output)
		#cv2.imshow("img", img)
		#cv2.waitKey(0)
	return img_dict
if __name__ == "__main__":
	path = r'H:\2021BJ\tiqianpi18tian'

	file_list = get_folder(path)
	print(file_list)
	for each in file_list:
		files = get_img_tif(each)
		print (files)
		img_segmentation(files)

		fout = open(each + ".xls", 'w')
		file_list = get_img(each)
		print (file_list)
		img_dict = make_contours(file_list)
		for key in img_dict:
			fout.write (str(key) + "\t" + str(img_dict[key]) + "\n")
		fout.close()
