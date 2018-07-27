from __future__ import division
__author__ = 'andrew.H'
import sys,os,fnmatch,getopt,re,csv,xlsxwriter
from fnmatch import fnmatch
from subprocess import *
from collections import Counter
import numpy as np

def spreadSheet():

	#current row,col,layer and samplepoint
	row,col,layer,experiment,samplePoint=0,0,0,0,0

	#create excel file 
	workbook = xlsxwriter.Workbook('SampleReport.xlsx')
	worksheet = workbook.add_worksheet()		

	#generate all stat files required
	totalSubject = preAnalysis()

	#populate list of variants
	totalVariants=[]
	for i in range(0,len(totalSubject)):
		split = totalSubject[i].split(';')
		totalVariants.append(split[0])

	#get count and set of unique variants
	totalCount = Counter(totalVariants)
	#count = [Decimal(n) for n in count]
	totalUnique = set(totalVariants)

	#for each layers
	for i in range(1,6):
		layer += 1
		worksheet.write(col,0,'LAYER '+str(layer))
		
		#for all files in the current layer
		for path, subdirs, files in os.walk('.',topdown=False):#walk for files
			if fnmatch(path, '*-'+str(layer)+'*'):	
				for name in files: 
					if fnmatch(name, '*_result.hit.txt'):#catch result.hit files
						# Add output to Excel 
						#add all desired data to memory
						with open(os.path.join(path, name)) as tsv:
							for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):#grab tsv by column
								if column[0]=='subject_description':
									subject=[]

									for i in range(1,len(column)):
										subject.append(column[i])

									#populate list of variants in each file
									variants=[]
									for i in range(0,len(subject)):
										split = subject[i].split(';')
										variants.append(split[0])										

									#get count and set of unique variants
									count = Counter(variants)
									#count = [Decimal(n) for n in count]
									unique = set(variants)

									#for each unique organism
									for i in totalUnique:
										col += 1
										worksheet.write(col,0,i)

										for j in unique:
											if i == j:
												row+=1
												worksheet.write(col,row,i)



										#print count
										#print('YEET')



	# for obj in unique:
	# 	div=count[obj]
	# 	print '%s : %d : %f' % (obj, count[obj],(count[obj]/sum((count).values()))*100)

		#adding skip line between layers
		col += 2




def preAnalysis():
	remove()

	#GENERATE STAT FILES FOR ALL LAYERS

	#generate stat files for all layers
	for path, subdirs, files in os.walk('.',topdown=False):#walk for files
		if fnmatch(path, '*layer*'):
			for name in files: 
				if fnmatch(name, '*_result.hit.txt'):#catch result.hit files
					#create stat file
					if os.path.isfile(path+name[6:9]+'stat.txt'):
						f = open(path+name[6:9]+'stat.txt','a')
					else:
						f = open(path+name[6:9]+'stat.txt', 'w')	    
						f.write('query_name' + '	' + 'subject_description' + '	' + 'E value' + '	' + 'bit score' + '\n')#add header on creation
					#add all desired data to memory
					with open(os.path.join(path, name)) as tsv:
						for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):#grab tsv by column
							if column[0]=='query_name':
								query=[]

								for i in range(1,len(column)):
									query.append(column[i])

							if column[0]=='subject_description':
								subject=[]

								for i in range(1,len(column)):
									subject.append(column[i])

							if column[0]=='E value':
								eValue=[]

								for i in range(1,len(column)):
									eValue.append(column[i])

							if column[0]=='bit score':
								bitScore=[]

								for i in range(1,len(column)):
									bitScore.append(column[i])

					#Write to tsv
					for i in range(0,min(len(query),len(subject),len(eValue),len(bitScore))):
						f.write(query[i] + '	' + subject[i] + '	' + eValue[i] + '	' + bitScore[i] + '\n')
					f.close()

	#GENERATE STAT FILES FOR ALL EXPERIMENTS

	#find stat 
	for path, subdirs, files in os.walk('.',topdown=False):#walk for files
		if fnmatch(path, '*Experiment*'):
			#print files
			for name in files: 
				if fnmatch(name, '*stat*'):#catch stat files

					#create stat files
					if os.path.isfile(os.path.dirname(path)+'/'+os.path.basename(path)+'stat.txt'):#append if exist
						f = open(os.path.dirname(path)+'/'+os.path.basename(path)+'stat.txt', 'a')	
					else:
						f = open(os.path.dirname(path)+'/'+os.path.basename(path)+'stat.txt', 'w')#create if not exist
						f.write('query_name' + '	' + 'subject_description' + '	' + 'E value' + '	' + 'bit score' + '\n')#add header on creation

					#add all desired data to memory
					with open(os.path.join(path, name)) as tsv:
						for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):#grab tsv by column
							if column[0]=='query_name':
								query=[]

								for i in range(1,len(column)):
									query.append(column[i])

							if column[0]=='subject_description':
								subject=[]

								for i in range(1,len(column)):
									subject.append(column[i])

							if column[0]=='E value':
								eValue=[]

								for i in range(1,len(column)):
									eValue.append(column[i])

							if column[0]=='bit score':
								bitScore=[]

								for i in range(1,len(column)):
									bitScore.append(column[i])

					#Write to tsv
					for i in range(0,min(len(query),len(subject),len(eValue),len(bitScore))):
						f.write(query[i] + '	' + subject[i] + '	' + eValue[i] + '	' + bitScore[i] + '\n')
					f.close()

	#GENERATE STAT FILES FOR ALL SAMPLE DATES

	#find stat 
	for path, subdirs, files in os.walk('.',topdown=False):#walk for files
		if fnmatch(path, '*SP*'):
			#print files
			for name in files: 
				if fnmatch(name, '*Experiment*'):#catch stat files
					if fnmatch(name, '*stat*'):#catch stat files
						#create stat files

						if os.path.isfile(os.path.dirname(path)+'/'+os.path.basename(path)+'stat.txt'):#append if exist
							f = open(os.path.dirname(path)+'/'+os.path.basename(path)+'stat.txt', 'a')	
						else:
							f = open(os.path.dirname(path)+'/'+os.path.basename(path)+'stat.txt', 'w')#create if not exist
							f.write('query_name' + '	' + 'subject_description' + '	' + 'E value' + '	' + 'bit score' + '\n')#add header on creation

						#add all desired data to memory
						with open(os.path.join(path, name)) as tsv:
							for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):#grab tsv by column
								if column[0]=='query_name':
									query=[]

									for i in range(1,len(column)):
										query.append(column[i])

								if column[0]=='subject_description':
									subject=[]

									for i in range(1,len(column)):
										subject.append(column[i])

								if column[0]=='E value':
									eValue=[]

									for i in range(1,len(column)):
										eValue.append(column[i])

								if column[0]=='bit score':
									bitScore=[]

									for i in range(1,len(column)):
										bitScore.append(column[i])

						#Write to tsv
						for i in range(0,min(len(query),len(subject),len(eValue),len(bitScore))):
							f.write(query[i] + '	' + subject[i] + '	' + eValue[i] + '	' + bitScore[i] + '\n')
						f.close()

	#GENERATE SUBJECT LIST FOR RETURN ANALYSIS

	#Populate subject for analysis
	subject=[]

	#Retreive data from all hit files
	for path, subdirs, files in os.walk('.',topdown=False):#walk for files
		for name in files:
			if fnmatch(name, '*layer*'):
				if fnmatch(name, '*_result.hit.txt'):

					#add all desired data to memory
					with open(os.path.join(path, name)) as tsv:
						for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):#grab tsv by column
							if column[0]=='subject_description':
								for i in range(1,len(column)):
									subject.append(column[i])
	#return to funtions one, two, or three
	return subject

def remove():
	for path, subdirs, files in os.walk('.',topdown=False):#walk for files
		#print files
		for name in files: 
			if fnmatch(name, '*stat*'):#catch stat files
					os.remove(os.path.join(path, name))	

def one():
	#generate all stat files required
	subject = preAnalysis()

	#populate list of variants
	variants=[]
	for i in range(0,len(subject)):
		split = subject[i].split(';')
		variants.append(split[0])

	#get count and set of unique variants
	count = Counter(variants)
	#count = [Decimal(n) for n in count]
	unique = set(variants)


	#dataSet is the set of counts of samples
	dataSet=[]
	#print
	for obj in unique:
		div=count[obj]
		print '%s : %d : %f' % (obj, count[obj],(count[obj]/sum((count).values()))*100)
		dataSet.append(count[obj])


	print '\nsum = ' + str(sum(dataSet))
	print 'mean = ' + str(sum(dataSet)/len(dataSet))
	print 'var = ' + str(np.var([dataSet]))
	print 'stdev = ' + str(np.std([dataSet]))


def two():
	#generate all stat files required
	subject = preAnalysis()

	#populate list of variants	
	variants=[]
	for i in range(0,len(subject)):
		split = subject[i].split(';')
		variants.append(split[0]+';'+split[1])

	#get count and set of unique variants
	count = Counter(variants)
	unique = set(variants)

	#dataSet is the set of counts of samples
	dataSet=[]
	#print
	for obj in unique:
		div=count[obj]
		print '%s : %d : %f' % (obj, count[obj],(count[obj]/sum((count).values()))*100)
		dataSet.append(count[obj])


	print '\nsum = ' + str(sum(dataSet))
	print 'mean = ' + str(sum(dataSet)/len(dataSet))
	print 'var = ' + str(np.var([dataSet]))
	print 'stdev = ' + str(np.std([dataSet]))


def three():
	#generate all stat files required
	subject = preAnalysis()

	#populate list of variants
	variants=[]
	for i in range(0,len(subject)):
		split = subject[i].split(';')
		variants.append(split[0]+';'+split[1]+';'+split[2])

	#get count and set of unique variants
	count = Counter(variants)
	unique = set(variants)

	#dataSet is the set of counts of samples
	dataSet=[]
	#print
	for obj in unique:
		div=count[obj]
		print '%s : %d : %f' % (obj, count[obj],(count[obj]/sum((count).values()))*100)
		dataSet.append(count[obj])


	print '\nsum = ' + str(sum(dataSet))
	print 'mean = ' + str(sum(dataSet)/len(dataSet))
	print 'var = ' + str(np.var([dataSet]))
	print 'stdev = ' + str(np.std([dataSet]))

def help():

	#print instructions for use
	#maybe i should just point to a help file to save space here
	print('-h or --help for help')
	print('-r or --remove to remove all stat files')	
	print('--one option preforms std. deviation, avg, and other analytics on lowest layer')
	print('--two option preforms std. deviation, avg, and other analytics on second lowest layer')
	print('--three option preforms std. deviation, avg, and other analytics on third lowest layer')
	
#available options
options, remainder = getopt.getopt(sys.argv[1:], ':hr', [ 'help',
														 'remove',
														 'one',
														 'two',
														 'three',
														 'spreadsheet'
														 ])

for opt, arg in options:#each operation checks for its required parameters inside it's on function
	if opt in ('-h','--help'):
		help()
	if opt in ('-r','--remove'):
		remove()
	if opt in ('--one'):
		one()
	if opt in ('--two'):
		two()
	if opt in ('--three'):
		three()
	if opt in ('--spreadsheet'):
		spreadSheet()