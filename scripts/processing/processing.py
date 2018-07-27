__author__ = 'andrew.H'
import sys,os,os.path,json,fnmatch,shutil,getopt,re
from fnmatch import fnmatch
from subprocess import *

inFolder,baseFile,clean = '','',''

def operations():#for creating jobLauncher.sh file
	if not os.path.exists('jobFiles/'+'jobLauncher.sh'):#if the jobLauncher.sh file doesn't exist, create one
		f = open('jobFiles/'+'jobLauncher.sh', 'w+')
		f.write('#!/bin/sh'+'\n')
		f.write('#SBATCH --job-name=jobLauncher'+'\n')
		f.write('#SBATCH --output OutJL.out'+'\n')
		f.write('#SBATCH --error ErrBN.err'+'\n')
		#f.write('#SBATCH -p all'+'\n')
		f.write('#SBATCH -n 10'+'\n')
		f.write('#SBATCH -N 1'+'\n\n')
		#f.write('source /share/apps/Modules/3.2.10/init/modules.sh'+'\n')
		f.write('module load intel'+'\n')
		f.write('module load python3/anaconda/5.0.1'+'\n')
		#f.write('module load bbmap/36.85'+'\n')
		#f.write('module load blast/2.2.29'+'\n')

		#before closing add operations to run
		for opt, arg in options:
			if opt in ('--cleanb'):
				f.write('python bbduk_job.py\n')
			if opt in ('--fqToFasta'):
				f.write('python fqToFasta_job.py\n')
			if opt in ('--fastaSplit'):
				f.write('python fastaSplit_job.py\n')
			if opt in ('--blastn'):
				f.write('python blastn_job.py')
		f.close()

def bbduk():#for creating bbduk_job file
	data = json.loads(open('Config.json').read())

	for opt, arg in options:#checking the options for input folder provided
		if opt in ('--input'):
			inFolder = str(arg)#input folder

	for path, subdirs, files in os.walk(inFolder):
		for name in files:
			if fnmatch(name, '*.fastq.gz*'):
				baseFile = name#baseFile is filename without extentions
				while fnmatch(baseFile, '*.*'):
					baseFile = os.path.splitext(baseFile)[0]

				#TRIM#
				#constructing completeArg
				print('TRIM: ' + str(baseFile))
				completeArg = data['bbduk']['bbdukPath']+' '+'in='+data['bbduk']['filesPath']+path[path.find('/SP'):]+'/'+name+' out='+data['bbduk']['filesPath']+path[path.find('/SP'):]+'/bbduk/'+baseFile+'_PE_good.fq outm='+data['bbduk']['filesPath']+path[path.find('/SP'):]+'/bbduk/'+baseFile+'_PE_fail.fq outs='+data['bbduk']['filesPath']+path[path.find('/SP'):]+'/bbduk/'+baseFile+'_SE_pass.fq ref='+data['bbduk']['adapterPWD']+' '+data['bbduk']['ktrim']+' '+data['bbduk']['k']+' '+data['bbduk']['mink']+' '+data['bbduk']['hdist']+' '+data['bbduk']['misc']+' '+data['bbduk']['qtrim']+' '+data['bbduk']['trimq']+' '+data['bbduk']['maq']+' '+data['bbduk']['entropy']+' '+data['bbduk']['minlen']

				#if the jobfile folder doesn't exist, create one
				if not os.path.exists('jobFiles/'):
					os.makedirs('jobFiles/')
				#if the jobfile doesn't exist, create one
				if not os.path.exists('jobFiles/bbduk_job.py'):
					f = open('jobFiles/bbduk_job.py', 'w+')
					f.write('from subprocess import *'+'\n\n')
					f.close()

				#open and append completeArg to the jobfile
				f = open('jobFiles/bbduk_job.py', 'a')
				f.write("call(['"+completeArg+"'],shell=True);"+'\n')
				f.close()

				#PHIX#
				#constructing completeArg
				print('PHIX: ' + str(baseFile))
				completeArg = data['bbduk']['bbdukPath']+' '+'in='+data['bbduk']['filesPath']+path[path.find('/SP'):]+'/bbduk/'+baseFile+'_SE_pass.fq out=' +data['bbduk']['filesPath']+path[path.find('/SP'):]+'/bbduk/'+baseFile+'_SE_final.fq ref='+data['bbduk']['phixPWD']+' '+'k=31 '+data['bbduk']['hdist']
				
				#open and append completeArg to the jobfile
				f = open('jobFiles/bbduk_job.py', 'a')
				f.write("call(['"+completeArg+"'],shell=True);"+'\n')
				f.close()

	print('\n*** BBDuk Cleanup Complete ***\n')

def fqToFasta():#for creating fqToFasta_job file
	data = json.loads(open('Config.json').read())

	for opt, arg in options:#checking the options for input folder provided
		if opt in ('--input'):
			inFolder = str(arg)#input folder

	for path, subdirs, files in os.walk(inFolder):
		for name in files:
			if fnmatch(name, '*fastq.gz*'):
				baseFile = name#baseFile is filename without extentions
				while fnmatch(baseFile, '*.*'):
					baseFile = os.path.splitext(baseFile)[0]			

				#constructing completeArg
				print('fastq to fasta: ' + str(baseFile))
				completeArg = data['fastx']['fastxFormatterPath']+' -i '+data['bbduk']['filesPath']+path[path.find('/SP'):]+'/bbduk/'+str(baseFile)+'_SE_final.fq -o '+data['bbduk']['filesPath']+path[path.find('/SP'):]+'/bbduk/'+str(baseFile)+'_SE_final.fasta'
				
				#if the jobfile folder doesn't exist, create one
				if not os.path.exists('jobFiles/'):
					os.makedirs('jobFiles/')
				#if the jobfile doesn't exist, create one
				if not os.path.exists('jobFiles/fqToFasta_job.py'):
					f = open('jobFiles/fqToFasta_job.py', 'w+')
					f.write('from subprocess import *'+'\n\n')
					f.close()

				#open and append completeArg to the jobfile
				f = open('jobFiles/fqToFasta_job.py', 'a')
				f.write("call(['"+completeArg+"'],shell=True);"+'\n')
				f.close()
  
	print('\n*** Fastx Format Complete ***\n')

def fastaSplit():#for creating fastaSplit_job file
	data = json.loads(open('Config.json').read())

	if not os.path.exists('jobFiles/'):#if the jobfile doesn't exist, create one
		os.makedirs('jobFiles/')
	if not os.path.exists('jobFiles/'+'fastaSplit_job.py'):#if the fastaSplit_job.py doesn't exist, create one
		f = open('jobFiles/'+'fastaSplit_job.py', 'w+')
		f.write('import sys,os,os.path,json,fnmatch,glob,shutil,time,getopt'+'\n')
		f.write('from fnmatch import fnmatch'+'\n')
		f.write('from subprocess import *'+'\n')
		f.write(''+'\n')
		f.write("folder = "+data['bbduk']['filesPath']+'\n')
		f.write('look_for = ">M"'+'\n')
		f.write('counter = 0'+'\n')
		f.write(''+'\n')
		f.write("for path, subdirs, files in os.walk(folder):"+'\n')
		f.write("	for name in files:"+'\n')
		f.write("		if fnmatch(name, '*_SE_final.fasta*'):"+'\n')
		f.write("			baseFile = name #baseFile without pwd"+'\n')
		f.write("			while fnmatch(baseFile, '*.*'):"+'\n')
		f.write("				baseFile = os.path.splitext(baseFile)[0]"+'\n')
		f.write("			check = os.path.join(path,name)"+'\n')
		f.write("			with open(check, 'r') as file_to_read:"+'\n')
		f.write("				for line in file_to_read:"+'\n')
		f.write("					if look_for in line:"+'\n')
		f.write("						counter = counter + 1"+'\n')
		f.write("			splitterArgs = 'perl ./fastaSplitter.pl ' + os.path.join(path,baseFile) + ' ' + str(counter/25)"+'\n')
		f.write("			print('splitting: '+os.path.join(path,baseFile))"+'\n')
		f.write("			call([splitterArgs],shell=True)"+'\n')
		f.write("print('splitting complete')"+'\n') 
		f.close()

	if not os.path.exists('jobFiles/'+'fastaSplitter.pl'):#if the fasta_split_arg.pl doesn't exist, create one
		f = open('jobFiles/'+'fastaSplitter.pl', 'w+')
		f.write("#! /usr/bin/perl"+'\n')
		f.write("#!/usr/bin/perl -w"+'\n')
		f.write(""+'\n')
		f.write("#Created by Ben Torkian, modifications by Andrew Howden"+'\n')
		f.write(""+'\n')
		f.write("$input = $ARGV[0];"+'\n')
		f.write("chomp ($input);"+'\n')
		f.write(""+'\n')
		f.write("$upper_limit = $ARGV[1];"+'\n')
		f.write("chomp ($upper_limit);"+'\n')
		f.write(""+'\n')
		f.write("chomp_fasta();"+'\n')
		f.write("split_fasta();"+'\n')
		f.write(""+'\n')
		f.write("sub chomp_fasta {"+'\n')
		f.write('open (INFILE, "$input.fasta") or die "Cannot open infile!";'+'\n')
		f.write('open (OUT, ">"."$input"."_chomped.fasta") or die "Cannot open outfile!";'+'\n')
		f.write(""+'\n')
		f.write("while ($line=<INFILE>) { # Please remove the spaces"+'\n')
		f.write(""+'\n')
		f.write('if ($line=~/>/) {print OUT "$line";}'+'\n')
		f.write('else {chomp ($line);print OUT "$line";}'+'\n')
		f.write(""+'\n')
		f.write("}"+'\n')
		f.write("close OUT"+'\n')
		f.write("}"+'\n')
		f.write(""+'\n')
		f.write(""+'\n')
		f.write("sub split_fasta {"+'\n')
		f.write("$count = 0;"+'\n')
		f.write("$number = 1;"+'\n')
		f.write(""+'\n')
		f.write('open (INFILE, "$input"."_chomped.fasta") or die "Cannot open infile!";'+'\n')
		f.write('open (OUT, ">"."$input"."_"."$number".".fasta") or die "Cannot open outfile!";'+'\n')
		f.write(""+'\n')
		f.write("while ($line=<INFILE>) {"+'\n')
		f.write("if ($line=~/>/) {"+'\n')
		f.write("$count++;"+'\n')
		f.write(""+'\n')
		f.write('if ($count==1) {print OUT "$line";}'+'\n')
		f.write("elsif ($count<$upper_limit) { #change this value to change upper limit"+'\n')
		f.write('print OUT "$line";'+'\n')
		f.write("}"+'\n')
		f.write("}"+'\n')
		f.write(""+'\n')
		f.write('else {chomp ($line);print OUT "$line";}'+'\n')
		f.write(""+'\n')
		f.write("if ($count==$upper_limit) { #change this value to change upper limit"+'\n')
		f.write("close OUT;"+'\n')
		f.write("$number++;"+'\n')
		f.write(""+'\n')
		f.write('open (OUT, ">"."$input"."_"."$number".".fasta") or die "Cannot open outfile!";'+'\n')
		f.write('print OUT "$line";'+'\n')
		f.write("$count = 1;"+'\n')
		f.write("}"+'\n')
		f.write("}"+'\n')
		f.write("}"+'\n')
		f.close()

	print('\n*** fastaSplit Complete ***\n')

def blastn():#for creating blastn_job file
	data = json.loads(open('Config.json').read())

	if not os.path.exists('jobFiles/'):#if the jobfile doesn't exist, create one
		os.makedirs('jobFiles/')
	if not os.path.exists('jobFiles/'+'blastn_job.py'):#if the blastn_job.py doesn't exist, create one
		f = open('jobFiles/'+'blastn_job.py', 'w+')
		f.write('import sys,os,os.path,json,fnmatch,glob,shutil,time,getopt'+'\n')
		f.write('from fnmatch import fnmatch'+'\n')
		f.write('from subprocess import *'+'\n')
		f.write(''+'\n')
		f.write("folder = '/data2/user_data/ahowden/dataForPipelineOrganized/'"+'\n')
		f.write(''+'\n')
		f.write('counter = 0'+'\n')
		f.write(''+'\n')		
		f.write("for path, subdirs, files in os.walk(folder):"+'\n')
		f.write("	for name in files:"+'\n')
		f.write("		if not fnmatch(name,'*chomped*'):"+'\n')
		f.write("			if fnmatch(name, '*_SE_final_*'):"+'\n')
		f.write("				counter = counter + 1"+'\n')
		f.write("				baseFile = name #baseFile without pwd"+'\n')
		f.write("				while fnmatch(baseFile, '*.*'):"+'\n')
		f.write("					baseFile = os.path.splitext(baseFile)[0]"+'\n')
		f.write("					filename = str(baseFile[:5]) + '-' + str(baseFile[-1:]) + '.sh'"+'\n')
		f.write("					f = open(filename, 'w')"+'\n')
		f.write("					f.write('#!/bin/sh'+'"+"\\n"+"')"+'\n')
		f.write("					f.write('#Run blast"+"\\n"+"')"+'\n')
		f.write("					f.write('"+"\\n"+"')"+'\n')
		f.write("					f.write('#INPUT Sequences file"+"\\n"+"')"+'\n')
		f.write("					f.write(")
		f.write("'QUERY='+os.path.join(path,name)"+"+'\\n"+"')"+'\n')
		f.write("					f.write('COREU=16'+'"+"\\n"+"')"+'\n')
		f.write("					f.write('"+"\\n"+"')"+'\n')
		f.write("					f.write('#SBATCH -J blast_' + str(counter) + '"+"\\n"+"')"+'\n')
		f.write("					f.write('#SBATCH -n 16'+'"+"\\n"+"')	"+'\n')
		f.write("					f.write('#SBATCH -t 48:00:00"+"\\n"+"')"+'\n')
		f.write("					f.write('"+"\\n"+"')"+'\n')
		f.write("					f.write('#BLAST DB"+"\\n"+"')"+'\n')
		f.write("					f.write('DB='+"+"'"+data['blastn']['database']+"'"+"+'"+"\\n"+"')"+'\n')
		f.write("					f.write('#check for DB"+"\\n"+"')"+'\n')
		f.write("					f.write('#ls $DB.*"+"\\n"+"')"+'\n')
		f.write("					f.write('#check for Sequences file"+"\\n"+"')"+'\n')
		f.write("					f.write('OUTFMT=5'+'"+"\\n"+"')"+'\n')
		f.write("					f.write('MAX=1'+'"+"\\n"+"')"+'\n')
		f.write("					f.write('"+"\\n"+"')"+'\n')
		f.write("					f.write('#OUTPUT file"+"\\n"+"')"+'\n')
		f.write("					f.write('OUTPUT=$QUERY.blast.xml"+"\\n"+"')"+'\n')
		f.write("					f.write('"+"\\n"+"')"+'\n')
		f.write("					f.write('# blast Command"+"\\n"+"')"+'\n')
		f.write("					f.write('#module load  blast/2.2.29"+"\\n"+"')"+'\n')
		f.write("					f.write('"+"\\n"+"')"+'\n')
		f.write("					f.write('# run blast"+"\\n"+"')"+'\n')
		f.write("					f.write('"+data['blastn']['blastnPath']+" -query $QUERY -out $OUTPUT -db $DB -max_target_seqs $MAX -outfmt $OUTFMT -num_threads $COREU"+"\\n"+"')"+'\n')
		f.write("					f.close()"+'\n')
		f.write("					call(['/usr/bin/sbatch', filename])"+'\n')
		f.close()		
  
	print('\n*** BlastN Complete ***\n')

def parseMerge():
	data = json.loads(open('Config.json').read())

	if not os.path.exists('jobFiles/'):#if the jobfile doesn't exist, create one
		os.makedirs('jobFiles/')
	if not os.path.exists('jobFiles/'+'parseMerge_job.py'):#if the blastn_job.py doesn't exist, create one
			f = open('jobFiles/'+'parseMerge_job.py', 'w+')
			f.write("import sys,os,os.path,json,fnmatch,shutil,getopt,re"+'\n')
			f.write("from fnmatch import fnmatch"+'\n')
			f.write("from subprocess import *"+'\n')
			f.write("inFolder,baseFile,clean ='/data/userdata/ahowden/dataForPipelineOrganized','','' "+'\n')
			f.write("for opt, arg in options:#checking the options for input folder provided"+'\n')
			f.write("	if opt in ('--input'):"+'\n')
			f.write("		inFolder = str(arg)#input folder"+'\n')
			f.write("#find xml files by layer#_#"+'\n')
			f.write("for path, subdirs, files in os.walk(inFolder):"+'\n')
			f.write("	for name in files:"+'\n')
			f.write("		if fnmatch(name,'*.xml'):"+'\n')
			f.write("				baseFile = name #baseFile without pwd"+'\n')
			f.write("				while fnmatch(baseFile, '*.*'):"+'\n')
			f.write("					baseFile = os.path.splitext(baseFile)[0]"+'\n')
			f.write("				filename = str(baseFile[:8])"+'\n')
			f.write("				#create folder layer#_# in same location as file if not already created"+'\n')
			f.write("				if not os.path.exists(os.path.join(path,filename)):"+'\n')
			f.write("					os.makedirs(os.path.join(path,filename))"+'\n')
			f.write("					#move file to created folder"+'\n')
			f.write("					os.rename(path +'/'+ name,path +'/'+ filename +'/'+ name)"+'\n')
			f.write("				else:"+'\n')
			f.write("					#move file to existing folder"+'\n')
			f.write("					os.rename(path +'/'+ name,path +'/'+ filename +'/'+ name)"+'\n')
			f.write("#deploy parsemerge, input.json, xmlparser.pl"+'\n')
			f.write("for path, subdirs, files in os.walk(inFolder):"+'\n')
			f.write("	for adir in subdirs:"+'\n')
			f.write("		if fnmatch(adir,'*layer*'):"+'\n')
			f.write("			#add input.json. json is currently hardoded, probably best to change that."+'\n')
			f.write("			if not os.path.exists(path +'/'+ adir +'/input.json'):#if the fasta_split_arg.pl doesn't exist, create one"+'\n')
			f.write("				f = open(path +'/'+ adir +'/input.json', 'w+')"+'\n')


			f.write("			f.write('{"'"input"'":"'"+adir+''_"'",\\n')"+'\n')


			f.write(""+'\n')
			f.write(""+'\n')
			f.write(""+'\n')
			f.write(""+'\n')
			f.write(""+'\n')
			f.write(""+'\n')




				#f.write('{"input":"'+adir+'_",\\n')
				# f.write('"output_parse":"c49am1",\\n')
				# f.write('"n":"1",\\n')
				# f.write('"b":"50",\\n')
				# f.write('"DB_type":"refseq",\\n')
				# f.write('"DB_PreFex":"refseq_protein",\\n')
				# f.write('"core":"16",\\n')
				# f.write('"job_PreFex":"c49am1_refseq",\\n')
				# f.write('"allocation":"TG-DEB140011",\\n')
				# f.write('"email":"rsnorman@sc.edu",\\n')
				# f.write('"db_path":"/work/01868/rsnorman/db/Refseq_2013",\\n')
				# f.write('"OUTFMT":"5",\\n')
				# f.write('"MAX":"1"}')
				# f.close()

				# shutil.copy('/data/userdata/ahowden/tools/parsemerge/parsemerge.py', path +'/'+ adir +'/parsemerge.py')
				# shutil.copy('/data/userdata/ahowden/tools/parsemerge/xmlparse.pl', path +'/'+ adir +'/xmlparse.pl')

				# call(['python ' + path +'/'+ adir +'/parsemerge.py'],shell=True);



def formatter():
	pass
	#Gather step 1(Original) material

	#Gather step 2(BBduk) material
	
	#Gather step 3(FQtoFasta) material
	
	#Gather step 4(FastaSplit) material
	
	#Gather step 5(Bashwriter/Blast) material
	
	#Gather step 6(Parsemerge) material
	
	#Gather step 7(Analysis) material


def help():

	#print instructions for use
	print('-h or --help for helpful helping help')
	print('--cleanf or --cleanb with cleaning with fastx or bbduk')
	print('--fqToFasta to convert .fq files to .fasta files')
	print('--fastaSplit to split fasta files prior to blasting')
	print('--blastn for using blastn')

#if the jobfile folder exist, delete it
if os.path.exists('jobFiles/'):
	shutil.rmtree('jobFiles/')

#available options
options, remainder = getopt.getopt(sys.argv[1:], ':h', [ 'help',
														 'input=',
														 'cleanb',
														 'fqToFasta',
														 'blastn',
														 'fastaSplit',
														 'parsemerge'
														 ])

for opt, arg in options:#calling functions desired by user
	if opt in ('-h','--help'):
		help()
	if opt in ('--cleanb'):
		bbduk()
	if opt in ('--fqtofasta'):
		fqToFasta()
	if opt in ('--fastasplit'):
		fastaSplit()
	if opt in ('--blastn'):
		blastn()
	elif opt in ('--parsemerge'):
		parseMerge()

operations()