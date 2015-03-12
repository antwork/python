#! /usr/bin/env python
# -- coding:utf-8 --
"""
-----------------------------------------------------------------
使用说明:
示例:
./icon.py             转化iphone ios6及以上版本icon
./icon.py iphone 6    转化iphone ios6及以上版本icon
./icon.py iphone 7    转化iphone ios7及以上版本icon
./icon.py ipad        转化ipad ios6及以上版本icon
./icon.py ipad 6      转化ipad ios6及以上版本icon
./icon.py ipad 7      转化ipad ios7及以上版本icon
./icon.py all         转化iphone,ipad ios6及以上版本icon
./icon.py all 6       转化iphone,ipad ios6及以上版本icon
./icon.py all 7       转化iphone,ipad ios7及以上版本icon
-----------------------------------------------------------------
"""
import os, sys
import imghdr
import re

from PIL import Image

def startIphone(iosVer=6):
	start(True, False, iosVer)
def startIpad(iosVer=6):
	start(False, True, iosVer)
def startAll(iosVer=6):
	start(True, True, iosVer)

def start(hasIphone, hasIpad,iosVer = 6):
	img = get1024Img()
	curDir = os.getcwd()

	if iosVer < 5:
		print "[Error]系统版本过低"
		return

	if iosVer >= 5 and img:
		publicDict = {'iTunesArtwork@2x.png':1024, 'iTunesArtwork.png':512}

		iphone6OrSmallerDict = {'Icon.png':57, 'Icon@2x.png':114, 'Icon-Small.png':29, 'Icon-Small@2x.png':58,'Icon-Small-40.png':40,'Icon-Small-40@2x.png':80}
		iphone7OrBiggerDict = {'Icon-60.png':60, 'Icon-60@2x.png':120, 'Icon-Small.png':29, 'Icon-Small@2x.png':58}
		
		ipad6OrSmallerDict = {'Icon-72.png':72, 'Icon-72@2x.png':144,'Icon-Small.png':29, 'Icon-Small@2x.png':58, 'Icon-Small-50.png':50,'Icon-Small-50@2x.png':100}
		ipad7OrBiggerDict = {'Icon-60.png':60, 'Icon-60@2x.png':120,'Icon-60@3x.png':180,'Icon-Small.png':29, 'Icon-Small@2x.png':58, 'Icon-Small-40.png':40,'Icon-Small-40@2x.png':80}
		
		dict = publicDict
		if iosVer <= 6:
			if hasIphone:
				dict.update(iphone6OrSmallerDict)
			if hasIpad:
				dict.update(ipad6OrSmallerDict)
		
		if iosVer <= 7:
			if hasIphone:
				dict.update(iphone7OrBiggerDict)
			if hasIpad:
				dict.update(ipad7OrBiggerDict)
		if dict:
			newFolder = newFolderInFolder(curDir, 'Icon')
			for name, size in dict.items():
				try:
					theSize = size, size
				except Exception, e:
					print("[Error]cannot create thumbnail for", infile)
				else:
					out = img.resize(theSize, Image.LANCZOS)
					outPath = newFolder + '/' + name
					out.save(outPath)
				finally:
					pass
			# 重命名 iTunesArtwork
			renameImage(newFolder + '/iTunesArtwork.png', 'iTunesArtwork')
			renameImage(newFolder + '/iTunesArtwork@2x.png', 'iTunesArtwork@2x')

			keys = dict.keys()
			keys.remove('iTunesArtwork@2x.png')
			keys.remove('iTunesArtwork.png')
			func = lambda s: (s.split('.')[0]).split('@2x')[0]
			keys = map(func, keys)
			keys = list(set(keys))
			print """
### 请将以下字段复制到info.plist中 ### 
==========================================
<key>CFBundleIcons</key>
<dict>
	<key>CFBundlePrimaryIcon</key>
	<dict>
		<key>CFBundleIconFiles</key>
		<array>"""
			for name in keys:
				print "				<string>%s</string>" % name
			print """		</array>
		<key>UIPrerenderedIcon</key>
		<true/>
	</dict>
</dict>
==========================================
"""
		else:
			print "[Error]未选择设备"
	else:
		print "[Error]未能找到图片,请检查是否放入1024x1024图片是否放入正确!"

def save(img, folder, name):
	newPath = folder + '/' + name
	img.save(newPath)

# 查询1024x1024图片
def get1024Img():
	curDir = os.getcwd()

	# 获取所有文件,存储图片到list
	fileNames = os.listdir(curDir)

	for fileName in fileNames:
		path = curDir + '/' + fileName
		if not os.path.isfile(path):
			continue
		imgType = imghdr.what(path)
		if imgType == 'png':
			img = Image.open(path)
			size = img.size
			if size[0] == 1024 and size[1] == 1024:
				return img

	return None

# 图片重命名
def renameImage(oldPath, newName):
	folder, oldName = os.path.split(oldPath)
	newPath = folder + '/' + newName
	os.rename(oldPath, newPath)

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

if __name__ == "__main__":
	print __doc__
	argv = sys.argv
	count = len(argv)

	if count == 1:
		print "[Info]开始处理iphone iOS 6及以上的icon"
		startIphone()
	elif count >= 2:
		argv1 = argv[1]
		m = re.match(r'[0-9]+', argv1)
		if m:
			print "[Info]开始处理iphone iOS %s及以上的icon" % argv1
			startIphone(int(argv1))
		else:
			lowerArgv = argv1.lower()
			isIphone= False
			isIpad = False
			if lowerArgv == 'iphone':
				isIphone = True
			elif lowerArgv == 'ipad':
				isIpad = True
				isIphone = True
			elif lowerArgv == 'all':
				isIphone = True
				isIpad = True
			else:
				print "[Error]请输入正确的平台,格式请参考使用说明 "

			if isIphone or isIpad:
				if count == 3:
					argv2 = argv[2]
					m = re.match(r'[0-9]+', argv2)
					if m:
						ver = int(argv2)
						if isIphone and isIpad:
							startAll(ver)
						elif isIphone:
							startIphone(ver)
						elif isIpad:
							startIpad(ver)
					else:
						print "[Error]请输入正确的平台,格式请参考使用说明  "
						
				elif count == 2:
					if isIphone and isIpad:
							startAll()
					elif isIphone:
						startIphone()
					elif isIpad:
						startIpad()
