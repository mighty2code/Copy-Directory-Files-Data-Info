# Copy-Directory-Files-Data-Info

To Copy all files (of given extension if specified) or only
properties of the files in the input directory to the output directory.
(recursively or non recursively).

copydir.copydir():
> You can copy all files in the input directory using copydir.copydir() function.
> 1. It can copy files recursively or non recursively in the directory tree.
> 2. It copies exact copy of files including its meta data information.

copydir.copyinfo():
> You can copy only meta data information of all files in the input directory using
  copydir.copyinfo() function.
> 1. It can copy files metadata recursively or non recursively in the directory tree.
> 2. A file's metadata (like: file properties, exif data and audio/video metadata) is copied into file.info.
> 3. It is useful for backup purposes.
> 4. Size of .info file is very small ≤ 1 KB
