#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
-----------------------------------------------------------------
说明:
将文件所在文件夹中的启动图片根据图片的大小命名为各平台真正需要的图片

示例:
./default.py 

备注:
需要依赖库Pillow: http://pillow.readthedocs.org/en/latest/
安装Pillow $: sudo pip install Pillow
安装pip:   $: sudo easy_install pip
-----------------------------------------------------------------
"""


import os
import re
from PIL import Image

rePatten = re.compile(r'\.?(png|jpg|jpeg|bmp)')

def start():
	# 读取当前文件夹
	curDir = os.getcwd()

	# 获取所有文件,存储图片到list
	fileNames = os.listdir(curDir)

	# 图片地址列表
	imgFilePaths = getImageFilesInFolder(curDir, fileNames)

	if len(imgFilePaths) > 0:
		 newFolder = newFolderInFolder(curDir, 'Default')

	# 轮询所有图片,查看size,将size图片重命名
	for imagePath in imgFilePaths:
		img = Image.open(imagePath)
		size = img.size

		width = size[0]
		height = size[1] 
		newName = getImageNameBySize(width, height)

		if newName:
			isPng = isFileNamePng(imagePath)
			if isPng:
				newPath = newFolder + '/' + newName
				os.rename(imagePath, newPath)

# 获取新文件夹
def newFolderInFolder(folderPath, folderName):
	index = 1
	while True:
		path = folderPath + '/' + folderName + str(index)
		if not os.path.exists(path):
			os.makedirs(path)
			print 'path:' + path
			return path	
		index += 1

# 获取文件夹中的图片,返回图片地址列表
def getImageFilesInFolder(folder, names):
	imageFiles = []
	for filename in names:
		tmpPath = folder + '/' + filename
		isTmpPathFile = os.path.isfile(tmpPath)
		
		if isTmpPathFile:
			# 判断是否图片
			isImg = isFileNameAImg(filename)
			if isImg:
				imageFiles.append(tmpPath)
	return imageFiles


# 判断文件名是否图片文件名
def isFileNameAImg(imageName):
	a, b = os.path.splitext(imageName)
	
	if b:
		result = rePatten.match(b)
		if result:
			return True
	return False

# 图片是否是否png
def isFileNamePng(imageName):
	a, b = os.path.splitext(imageName)
	if 'png' in b:
		return True
	return False

# 根据size获取文件名
def getImageNameBySize(width, height):
	name = 'Default'
	if width == 320 and height == 480:
		name = name + '.png'
	elif width == 640 and height == 960:
		name = name + '@2x.png'
	elif width == 640 and height == 1136:
		name = name + '-568h@2x.png'
	elif width == 750 and height == 1334:
		name = name + '-667h@2x.png'
	elif width == 1242 and height == 2208:
		name = name + '-736h@3x.png'
	elif width == 768 and height == 1024:
		name = name + '-Portrait~ipad.png'
	elif width == 1024 and height == 768:
		name = name + '-Landscape~ipad.png'
	else:
		return None
	return name
	
# 图片另存为png
def saveImgToPng(oldPath, newName):
	img = Image.open(oldPath)
	newImg = Image.new('RGB', img.size, (255, 255, 255))
	newImage.paster(img, img)

	folder, oldName = os.path.split(oldPath)
	newPath = folder + '/' + newName
	newImage.save(newPath)

# 图片重命名
def renameImage(oldPath, newName):
	folder, oldName = os.path.split(oldPath)
	newPath = folder + '/' + newName
	print "rename:" + oldPath + "---" + newName
	os.rename(oldPath, newPath)


# 开始处理
if __name__ == "__main__":
	start()