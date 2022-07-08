''' Module to Copy all files (of given extension if specified) or
	properties in the input directory to the output directory.
	(recursively or non recursively).
'''

import os
import time

def get_properties(filepath):
	''' Returns properties of given file
		as dictionary object.
	'''
	meta_data={}
	atim=time.localtime(os.path.getatime(filepath))
	mtim=time.localtime(os.path.getmtime(filepath))
	ctim=time.localtime(os.path.getctime(filepath))
	size=auto_convert_memory(os.path.getsize(filepath))
	permit=''
	if(os.access(filepath,os.R_OK)):
		permit+='R'
	if(os.access(filepath,os.W_OK)):
		permit+='W'
	if(os.access(filepath,os.X_OK)):
		permit+='X'
	permit='-'.join(permit)
	
	meta_data['Name']=os.path.basename(filepath)
	meta_data['Location']=os.path.abspath(filepath)
	filename,meta_data['Type']=os.path.splitext(meta_data['Name'])
	meta_data['Permissions']=permit;
	meta_data['Size']='{:.2f}'.format(size[0])+' '+size[1]
	meta_data['Access Time']=sftime(atim);
	meta_data['Modified Time']=sftime(mtim);
	meta_data['Change Time']=sftime(ctim);
	return meta_data

def get_exif(filepath):
	''' Returns exif of given image file
		as dictionary object.
	'''
	from PIL import Image
	from PIL.ExifTags import TAGS
	Exif={}
	image = Image.open(filepath)
	exifdata = image.getexif()
	
	# Looping through all the tags present in exifdata
	for tagid in exifdata:
		tagname = TAGS.get(tagid, tagid)
		value = exifdata.get(tagid)
		if isinstance(value, bytes):
			value = value.decode()
		Exif[tagname]=value
	if 'ImageWidth' in Exif and 'ImageLength' in Exif:
		wd=Exif.pop('ImageWidth')
		ht=Exif.pop('ImageLength')
		Exif['Resolution']=f'{wd}×{ht} ({wd*ht/10**6 :.1f} MP)'
	return Exif

def get_avMetadata(filepath):
	''' Returns metadata of given audio/video
		file as dictionary object.
	'''
	from tinytag import TinyTag
	av = TinyTag.get(filepath)
	meta_data={}
	meta_data['Title']=av.title
	meta_data['Title']=av.title
	meta_data['Album']=av.album
	meta_data['Album Artist']=av.albumartist
	meta_data['Composer']=av.composer
	meta_data['Genre']=av.genre
	meta_data['Comment']=av.comment
	meta_data['Year Released']=av.year
	meta_data['Duration']=auto_convert_time(av.duration)
	meta_data['Bit Rate']=str(av.bitrate)+' kBits/s'
	meta_data['Sample Rate']=str(av.samplerate)+' sample/s'
	meta_data['Audio Offset']=av.audio_offset
	meta_data['Channels']=av.channels
	meta_data['Track']=av.track
	meta_data['Track Total']=av.track_total
	return meta_data

def auto_convert_memory(size,Memory_Type=None):
	''' Convert memory size into appropriate
		Memory Unit and return it as a string.
	'''
	M=-1; P=0	# 1024^P
	p=1024; MU=['B','KB','MB','GB','TB','PB']
	
	if Memory_Type and Memory_Type.upper() in MU:
		M=MU.index(Memory_Type.upper())
		
	if M!=-1:
		size=size*(p**M)
	
	if(size>1024**5):
		return 'Too Large File',''
		
	while(size>=p):
		size=size/p
		P+=1
	return size,MU[P]

auto_convert_time= lambda seconds: time.strftime("%H:%M:%S", time.gmtime(seconds))
sftime= lambda tm_struct: time.strftime('%Y-%m-%d %H:%M:%S %a',tm_struct)

def getfiles(input_dir,extn='',recurse=False):
	''' Returns list of all files paths (or of given extension)
		from given input directory.
	'''
	import glob
	if recurse:
		filelist=glob.glob(os.path.join(input_dir,'**','*'+extn),recursive=True)
	else:
		filelist=glob.glob(os.path.join(input_dir,'*'+extn))
	return filelist

def copyinfo(in_dir,out_dir,extn='',recurse=False):
	''' Copy all files information/properties in the input directory
		to the output directory.
	'''
	if not os.path.exists(in_dir):
		print("Error: Input Directory doesn't exist.")
		return
	
	import shutil
	filepaths=getfiles(in_dir,extn,recurse)
	for fp in filepaths:
		os.system('clear')
		if not os.path.isfile(fp):
			continue
		prop=get_properties(fp)
		newfpath=prop['Location'].replace(os.path.abspath(in_dir),os.path.abspath(out_dir))
		
		newpath=newfpath.removesuffix(prop['Name'])
		
		if not os.path.exists(newpath):
			os.makedirs(newpath)
		
		newfpath=newfpath.removesuffix(prop['Type'])
		newfpath=newfpath+prop['Type']+'.info'
		
		print('From:',fp)
		print('To:',newfpath,'\n')
		file=open(newfpath,'w')
		if(prop['Type'].lower() in ['.mp3','.m4a','.mp4','.flac','.wav','.opus','.ogg','.mkv','.webm']):
			prop.update(get_avMetadata(fp))
		elif(prop['Type'].lower() in ['.jpg','.jpeg','.png','.gif']):
			prop.update(get_exif(fp))
		for k in prop:
			file.write(f'{k:20}: {prop[k]}\n')
		file.close()
		shutil.copystat(fp,newfpath)

def copydir(in_dir,out_dir,extn='',recurse=False):
	''' Copy all files (with same statistics) in the input directory
		to the output directory.
	'''
	if not os.path.exists(in_dir):
		print("Error: Input Directory doesn't exist.")
		return
	
	import shutil
	filepaths=getfiles(in_dir,extn,recurse)
	
	for fp in filepaths:
		os.system('clear')
		if not os.path.isfile(fp):
			continue
		newfpath=os.path.abspath(fp).replace(os.path.abspath(in_dir),os.path.abspath(out_dir))
		newpath=newfpath.removesuffix(prop['Name'])
		if not os.path.exists(newpath):
			os.makedirs(newpath)
		print('From:',fp)
		print('To:',newfpath,'\n')
		shutil.copy2(fp,newfpath)
