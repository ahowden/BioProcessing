import sys,os,os.path,json,fnmatch,shutil,getopt,re
from fnmatch import fnmatch
from subprocess import *
inFolder,baseFile,clean ='/data/userdata/ahowden/dataForPipelineOrganized','','' 
for opt, arg in options:#checking the options for input folder provided
	if opt in ('--input'):
		inFolder = str(arg)#input folder
#find xml files by layer#_#
for path, subdirs, files in os.walk(inFolder):
	for name in files:
		if fnmatch(name,'*.xml'):
				baseFile = name #baseFile without pwd
				while fnmatch(baseFile, '*.*'):
					baseFile = os.path.splitext(baseFile)[0]
				filename = str(baseFile[:8])
				#create folder layer#_# in same location as file if not already created
				if not os.path.exists(os.path.join(path,filename)):
					os.makedirs(os.path.join(path,filename))
					#move file to created folder
					os.rename(path +'/'+ name,path +'/'+ filename +'/'+ name)
				else:
					#move file to existing folder
					os.rename(path +'/'+ name,path +'/'+ filename +'/'+ name)
#deploy parsemerge, input.json, xmlparser.pl
for path, subdirs, files in os.walk(inFolder):
	for adir in subdirs:
		if fnmatch(adir,'*layer*'):
			#add input.json. json is currently hardoded, probably best to change that.
			if not os.path.exists(path +'/'+ adir +'/input.json'):#if the fasta_split_arg.pl doesn't exist, create one
				f = open(path +'/'+ adir +'/input.json', 'w+')
			f.write('{"input":"+adir+_",\n')






