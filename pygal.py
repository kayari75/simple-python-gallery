#!/opt/bin/python
""" PYGAL Python Gallery Generator """

import os
import glob
import sqlite3
import time
import hashlib
import logging


def dirwalk(rootfolder):
    filelist=[];
    extList = [".JPG", ".jpg"]
    for root, dirs, files in os.walk(rootfolder,topdown=False):
	for name in files:
		file=os.path.join(root, name)
		if ( os.path.splitext(file)[1] in extList):
			filelist.append(file);
    return filelist



def sha1file(file):
	try:
		f = open(file,'rb')
		h = hashlib.md5()
		h.update(f.read())
		hash = h.hexdigest()
		f.close()
	except:
		hash = "File Error"

	return hash

def get_exif(fn):
	from PIL import Image
	from PIL.ExifTags import TAGS
	ret = {}
	logging.info('Open file : %s' % fn)
	try:
		i = Image.open(fn)
		info = i._getexif()
		for tag, value in info.items():
     			decoded = TAGS.get(tag, tag)
			ret[decoded] = value
	except:
		#ret['Model']="UNKNOWN"
		#ret['DateTimeOriginal']="UNKNOWN"
		logging.warning('Exif Error : %s'  % fn)
	
	logging.info('Closing file : %s' % fn)
	return ret	


if __name__ == "__main__":
	default='UNKNOWN'
	logging.basicConfig(filename='/home/kayari/MesFichiers/MesPhotos/pygal/pygal.log',level=logging.DEBUG)
	filelist=dirwalk("/home/kayari/MesFichiers/MesPhotos/")
	for file in filelist:
		exif = get_exif(file)
		print ("%s : %s : %s" % (file, exif.get('Model'), exif.get('DateTimeOriginal',default)))
