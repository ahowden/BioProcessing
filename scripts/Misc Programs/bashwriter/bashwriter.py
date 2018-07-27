

__author__ = 'ben.Torkian'
from subprocess import call
import subprocess
import re
import json
import os

json_data = open("input.json")
data = json.load(json_data)
my_input = data['input']
path = os.path.dirname(os.path.realpath(__file__))



namePreFix =  data['job_PreFex']
numberOfFile = 40
for number in range(1, numberOfFile + 1):	
	filename = namePreFix + '-' + str(number) + '.sh'
	f = open(filename, 'w')
	f.write('#!/bin/sh\n')
	f.write('#Run blast USC by Norman\n')
	f.write('#1/14/2015\n')
	f.write('\n')
	f.write('#INPUT Sequences file\n')
	f.write('QUERY='+my_input + str(number) + '.fasta\n')
	f.write('COREU='+data['core']+'\n')
	f.write('\n')
	f.write('#SBATCH -J blast_' + str(number) + '\n')
	f.write('#SBATCH -A '+data['allocation']+'\n')
	f.write('#SBATCH -n '+data['core']+'\n')	
	f.write('#SBATCH -t 48:00:00\n')
	f.write('#SBATCH -p normal\n')
	f.write('#SBATCH --mail-user='+data['email']+'\n')
	f.write('#SBATCH --mail-type=begin  # email me when the job starts\n')
	f.write('#SBATCH --mail-type=end    # email me when the job finishes\n')
	f.write('\n')
	f.write('#BLAST DB\n')
	f.write('DB='+data['db_path']+'\n')
	f.write('#check for DB\n')
	f.write('#ls $DB.*\n')
	f.write('#check for Sequences file\n')
	f.write('OUTFMT='+data['OUTFMT']+'\n')
	f.write('MAX='+data['MAX']+'\n')
	f.write('\n')
	f.write('#OUTPUT file\n')
	f.write('OUTPUT=$QUERY.blast.xml\n')
	f.write('\n')
	f.write('# blast Command\n')
	f.write('#module load  blast/2.2.28\n')
	f.write('\n')
	f.write('# run blast\n')
	f.write('/opt/apps/blast/2.2.28/bin/blastx -query $QUERY -out $OUTPUT -db $DB/'+data['DB_PreFex']+' -max_target_seqs $MAX -outfmt $OUTFMT -num_threads $COREU\n')
	f.close()
	call(['/usr/bin/sbatch', filename])


