# Main file (use of copydir module).

import copydir as cp

if __name__=='__main__':
	in_dir =input('Enter Input Directory: ')
	out_dir=input('Enter Output Directory: ')
	extn=''
	recurse=True
	cp.copyinfo(in_dir,out_dir,extn,recurse)
	#cp.copydir(in_dir,out_dir,extn,recurse)