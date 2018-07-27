__author__ = 'andrew.H'
import sys,os,os.path,json,fnmatch,shutil,getopt,re
from fnmatch import fnmatch
from subprocess import *

inFolder,baseFile,clean = '/data/userdata/ahowden/dataForPipelineOrganized','',''

for opt, arg in options:#checking the options for input folder provided
	if opt in ('--input'):
		inFolder = str(arg)#input folder


#find xml files by layer#_#
for path, subdirs, files in os.walk(inFolder):
	for name in files:
		if fnmatch(name,'*.xml'):
				baseFile = name #baseFile without pwd"+'\n')
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
				f.write('{"input":"'+adir+'_",\n')
				f.write('"output_parse":"c49am1",\n')
				f.write('"n":"1",\n')
				f.write('"b":"50",\n')
				f.write('"DB_type":"refseq",\n')
				f.write('"DB_PreFex":"refseq_protein",\n')
				f.write('"core":"16",\n')
				f.write('"job_PreFex":"c49am1_refseq",\n')
				f.write('"allocation":"TG-DEB140011",\n')
				f.write('"email":"rsnorman@sc.edu",\n')
				f.write('"db_path":"/work/01868/rsnorman/db/Refseq_2013",\n')
				f.write('"OUTFMT":"5",\n')
				f.write('"MAX":"1"}')
				f.close()

				shutil.copy('/data/userdata/ahowden/tools/parsemerge/parsemerge.py', path +'/'+ adir +'/parsemerge.py')
				shutil.copy('/data/userdata/ahowden/tools/parsemerge/xmlparse.pl', path +'/'+ adir +'/xmlparse.pl')

				call(['python ' + path +'/'+ adir +'/parsemerge.py'],shell=True);