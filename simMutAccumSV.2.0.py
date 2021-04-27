####################--------------------IMPORT 
import os, sys, argparse, random

##########----------use samtools faidx to index fasta file
def indexFasta(FILE):
	cmd='samtools faidx ' + FILE
	os.system(cmd)

####################--------------------MAIN
def main():
	####################--------------------IMPORT ARGUMENTS
	parser = argparse.ArgumentParser()
	parser.add_argument('-wd', dest='wd', help='Full path to working directory (include prefix for new folders)', required=True)
	parser.add_argument('-pirs', dest='pirsPATH', help='Full path to pIRS (including /pirs at the end)', required=True)
	parser.add_argument('-svsim', dest='svsimPATH', help='Full path to SVsim (including /SVsim at the end)', required=True)
	parser.add_argument('-c', dest='refChrom', help='Chromosome to simulate in fasta format (must contain only one sequence)', required=True)
	parser.add_argument('-ncl', dest='nCl', help='Number of non-focal MA lines to simulate (clones of Ancestor)', type=int, required=True)
	#####parameters specific to pIRS
	parser.add_argument('-het', dest='hetRate', help='Haploid rate of heterozygosity for pIRS to simulate in ANC', type=float, default=0.0005)
	parser.add_argument('-snp', dest='snpRate', help='Haploid rate of SNP mutations for pIRS to simulate in descendent lines', type=float, default=0.0005)
	parser.add_argument('-x', dest='cov', help='Coverage for pIRS to simulate', type=int, default=50)
	parser.add_argument('-rlen', dest='rLen', help='Read length for pIRS to simulate', type=int, default=150)
	parser.add_argument('-insz', dest='inSize', help='Insert size for pIRS to simulate', type=int,  default=350)
	#####parameters specific to SVsim
	parser.add_argument('-svs', dest='svSeed', help='SVsim random seed', type=int, required=True)

	parser.add_argument('-svfa', dest='svFileANC', help='SVsim .sim file containing arguments to simulate SV for ANC', required=True)
	parser.add_argument('-svna', dest='svNumANC', help='SVsim number of replicate SVs for ANC', type=int, required=True)
	
	parser.add_argument('-svfm', dest='svFileMA', help='SVsim .sim file containing arguments to simulate SV for MA line', required=True)
	parser.add_argument('-svnm', dest='svNumMA', help='SVsim number of replicate SVs for MA line',  type=int, required=True)
	
	parser.add_argument('-mut', dest='mutType', help='Type of MA mutation to simulation (1 for 0/0 to 0/1; 2 for 0/1 to 1/1)',  type=int, required=True)
	args = parser.parse_args()
	
	##########----------Assign variables
	cwd = os.path.realpath(args.wd)
	pirsPATH = args.pirsPATH
	svsimPATH = args.svsimPATH
	refChrom = args.refChrom
	nCl = args.nCl
	hetRate = args.hetRate
	snpRate = args.snpRate
	cov = args.cov
	rLen = args.rLen
	inSize = args.inSize
		
	svSeed = args.svSeed
	svFileANC = args.svFileANC
	svNumANC = args.svNumANC
	svFileMA = args.svFileMA
	svNumMA = args.svNumMA
	mutType = args.mutType
	
	##########----------Check parameters
	if mutType!=1 and mutType!=2 and mutType!=3 and mutType!=4:
		sys.exit('ERROR: -mut must be 1, 2, 3 or 4!')
	if svNumANC<0 or svNumMA<0:
		sys.exit('ERROR: -svna and -svnm must be equal or larger than 0!')

	####################--------------------PREPARE SIMULATION
	#########----------remove pre-existing folders
	if os.path.isdir(cwd+'step1'):
		os.system('rm -r '+cwd+'step1')
	if os.path.isdir(cwd+'step2'):
		os.system('rm -r '+cwd+'step2')
	if os.path.isdir(cwd+'step3'):
		os.system('rm -r '+cwd+'step3')
	##########----------Create new directories for output
	os.system('mkdir '+cwd+'step1')
	os.system('mkdir '+cwd+'step2')
	os.system('mkdir '+cwd+'step3')
	##########----------setup output directories
	out1 = cwd+'step1/'
	out2 = cwd+'step2/'
	out3 = cwd+'step3/'
	
	##########----------Create random seeds for later
	#####-----for adding SV in ANC
	seed1 = svSeed*1
	seed2 = svSeed*2
	#####-----for adding SV to MA
	seed3 = svSeed*3
	seed4 = svSeed*4
	seed5 = svSeed*5
	
	##########----------Output parameters as newline separated file
	listFlag = ['c','ncl','het','snp','x','rlen','insz','svs','svfa','svna','svfm','svnm','mut']
	listValue = [refChrom, nCl, hetRate, snpRate, cov, rLen, inSize, svSeed, svFileANC, svNumANC, svFileMA, svNumMA, mutType]
	with open(cwd+'param.txt', 'w') as fOUT:
		fOUT.write('FLAG\tVALUE\n')
		for FLAG, VALUE in zip(listFlag, listValue):
			fOUT.write(FLAG+'\t'+str(VALUE)+'\n')
	
	####################--------------------PIRS: GENERATE A DIPLOID ANCESTRAL SEQUENCE CONTAINING SNPS AND SVs
	####################	Generates two refChrom containing SNPs to represent a diploid individual (with heterozygosity)
	print ('\nSimulating SNPs for ANC...\n')
	cmd=pirsPATH +' diploid -q'+ ' -s ' +str(hetRate)+ ' -d 0.0 -v 0.0 -o ' + out1 + 'ANC.H1.1 '+ refChrom
	os.system(cmd)
	cmd=pirsPATH +' diploid -q'+ ' -s ' +str(hetRate)+ ' -d 0.0 -v 0.0 -o ' + out1 + 'ANC.H2.1 '+ refChrom
	os.system(cmd)
	
	####################--------------------SVsim: SIMLATE ANC STRUCTURAL VARIANTS
	####################	mutType = 1
	####################		add SV to H1 and H2 using seed1 and seed2, resepctively
	####################	mutType = 2
	####################		add SV to H1 and H2 using seed2 for both
	#####-----index
	ANCH1 = out1 + 'ANC.H1.1.snp.fa'
	ANCH2 = out1 + 'ANC.H2.1.snp.fa'
	indexFasta(ANCH1)
	indexFasta(ANCH2)
	if svNumANC == 0:
		###########----------No ANC mutations so just copy ANC.*.1 to make ANC.*.2
		cmd='cp ' +ANCH1+ ' ' + out1 + 'ANC.H1.2.fasta'
		os.system(cmd)
		cmd='cp ' +ANCH2+ ' ' + out1 + 'ANC.H2.2.fasta'
		os.system(cmd)
	elif mutType == 1 or mutType == 3:
		print ('\nSimulating heterozygous SVs for ANC...\n')
		#####-----add heterozygous SV (different seed for H1 and H2)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed1)+ ' -n ' +str(svNumANC)+ ' -i ' +svFileANC+ ' -r ' +ANCH1+ ' -o ' + out1 + 'ANC.H1.2'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed2)+ ' -n ' +str(svNumANC)+ ' -i ' +svFileANC+ ' -r ' +ANCH2+ ' -o ' + out1 + 'ANC.H2.2'
		os.system(cmd)
	elif mutType == 2 or mutType == 4:
		print ('\nSimulating homozygous SVs for ANC...\n')
		#####-----add homozygous SV (same seed for H1 and H2)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed2)+ ' -n ' +str(svNumANC)+ ' -i ' +svFileANC+ ' -r ' +ANCH1+ ' -o ' + out1 + 'ANC.H1.2'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed2)+ ' -n ' +str(svNumANC)+ ' -i ' +svFileANC+ ' -r ' +ANCH2+ ' -o ' + out1 + 'ANC.H2.2'
		os.system(cmd)
	
	####################--------------------SVsim: SIMLATE MA STRUCTURAL VARIANTS
	####################	Not affected by ANC HOMOZYGOUS SVs because H1 and H2 still the same length
	####################	mutType = 1 (homo ref to het)
	####################		ANC.H1.3 = ANC.H1.2, ANC.H2.3 = ANC.H2.2
	####################		MA.H1.3 = ANC.H1.2, MA.H2.3 = ANC.H2.2 + SV; seed3
	####################	mutType = 2 (het to homo alt)
	####################		ANC.H1.3 = ANC.H1.2, ANC.H2.3 = ANC.H2.2 + SV; seed3
	####################		MA.H1.3 = ANC.H1.2 + SV; seed4, MA.H2.3 = ANC.H2.2 + SV; seed3
	####################	mutType = 3 (het to homo ref)
	####################		ANC.H1.3 = ANC.H1.2, ANC.H2.3 = ANC.H2.2 + SV; seed3
	####################		MA.H1.3 = ANC.H1.2, MA.H2.3 = ANC.H2.2
	print ('\nSimulating SVs of mut type {} for MA line ...\n'.format(mutType))
	#####-----index
	ANCH1 = out1 + 'ANC.H1.2.fasta'
	ANCH2 = out1 + 'ANC.H2.2.fasta'
	indexFasta(ANCH1)
	indexFasta(ANCH2)
	##########----------add mutation based on mutType
	if svNumMA == 0:
		cmd='cp ' +ANCH1+ ' ' + out1 + 'ANC.H1.3.fasta'
		os.system(cmd)
		cmd='cp ' +ANCH2+ ' ' + out1 + 'ANC.H2.3.fasta'
		os.system(cmd)
		cmd='cp ' +ANCH1+ ' ' + out1 + 'MA.H1.3.fasta'
		os.system(cmd)
		cmd='cp ' +ANCH2+ ' ' + out1 + 'MA.H2.3.fasta'
		os.system(cmd)
	elif mutType == 1:
		cmd='cp ' +ANCH1+ ' ' + out1 + 'ANC.H1.3.fasta'
		os.system(cmd)
		cmd='cp ' +ANCH2+ ' ' + out1 + 'ANC.H2.3.fasta'
		os.system(cmd)
		cmd='cp ' +ANCH1+ ' ' + out1 + 'MA.H1.3.fasta'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'MA.H2.3'
		os.system(cmd)
	elif mutType == 2:
		cmd='cp ' +ANCH1+ ' ' + out1 + 'ANC.H1.3.fasta'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'ANC.H2.3'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH1+ ' -o ' + out1 + 'MA.H1.3'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'MA.H2.3'
		os.system(cmd)
	elif mutType == 3:
		cmd='cp ' +ANCH1+ ' ' + out1 + 'ANC.H1.3.fasta'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'ANC.H2.3'
		os.system(cmd)
		cmd='cp ' +ANCH1+ ' ' + out1 + 'MA.H1.3.fasta'
		os.system(cmd)
		cmd='cp ' +ANCH2+ ' ' + out1 + 'MA.H2.3.fasta'
		os.system(cmd)
	elif mutType == 4:
		#####-----add 0/1 to 1/1 mut
		cmd='cp ' +ANCH1+ ' ' + out1 + 'ANC.H1.3A.fasta'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'ANC.H2.3A'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH1+ ' -o ' + out1 + 'MA.H1.3A'
		os.system(cmd)
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed3)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'MA.H2.3A'
		os.system(cmd)
		#####-----Index ANC.H2.3A and MA.H2.3A
		ANCH2 = out1 + 'ANC.H2.3A.fasta'
		MAH2 = out1 + 'MA.H2.3A.fasta'
		indexFasta(ANCH2)
		indexFasta(MAH2)
		#####-----add 0/1 to 0/0 mut
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed4)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'ANC.H2.3B'
		os.system(cmd)
		#####-----add 0/0 to 0/1 mut
		cmd=svsimPATH + ' -W' + ' -s ' +str(seed5)+ ' -n ' +str(svNumMA)+ ' -i ' +svFileMA+ ' -r ' +ANCH2+ ' -o ' + out1 + 'MA.H2.3B'
		os.system(cmd)
		
	####################--------------------PIRS: GENERATE DIPLOID DESCENDANT LINES CONTAINING SNPS (NO INDELS)
	####################	for clones (CL{i}), input is ANC.H1.4 and ANC.H2.4
	####################		output as CL{i}.H1 and CL{i}.H2 to represents homolog 1 and 2 for unmutated clones
	####################	for MA lines, input is MA.H1.4 and MA.H1.4 
	####################		output as MA.H1 and MA.H2 to represents homolog 1 and 2 for single mutated line
	if mutType == 4:
		ANCH1 = out1 + 'ANC.H1.3A.fasta'
		ANCH2 = out1 + 'ANC.H2.3B.fasta'
		MAH1 = out1 + 'MA.H1.3A.fasta'
		MAH2 = out1 + 'MA.H2.3B.fasta'
	else:
		ANCH1 = out1 + 'ANC.H1.3.fasta'
		ANCH2 = out1 + 'ANC.H2.3.fasta'
		MAH1 = out1 + 'MA.H1.3.fasta'
		MAH2 = out1 + 'MA.H2.3.fasta'
	#####-----Generate unmutated lines
	listCL = ['CL'+str(i+1) for i in range(nCl)]
	for CLONE in listCL:
		print ('Simulating SNPs for unmutated line {}...\n'.format(CLONE))
		cmd=pirsPATH +' diploid -q'+ ' -s ' +str(snpRate)+ ' -d 0.0 -v 0.0 -o ' + out2 +CLONE+ '.H1.4 ' + ANCH1
		os.system(cmd)
		cmd=pirsPATH +' diploid -q'+ ' -s ' +str(snpRate)+ ' -d 0.0 -v 0.0 -o ' + out2 +CLONE+ '.H2.4 ' + ANCH2
		os.system(cmd)
	#####-----Generate mutant line
	print ('Simulating SNPs for MA line ...\n')
	cmd=pirsPATH +' diploid -q'+ ' -s ' +str(snpRate)+ ' -d 0.0 -v 0.0 -o ' + out2 + 'MA.H1.4 ' + MAH1
	os.system(cmd)
	cmd=pirsPATH +' diploid -q'+ ' -s ' +str(snpRate)+ ' -d 0.0 -v 0.0 -o ' + out2 + 'MA.H2.4 ' + MAH2
	os.system(cmd)
	
	####################--------------------PIRS: SIMULATE READS FROM DIPLOID ANC AND MA
	#####-----Simulate reads for ANC
	LINE = 'ANC'
	if mutType == 4:
		HOMOLOG1 = out1 +'ANC.H1.3A.fasta'
		HOMOLOG2 = out1 +'ANC.H2.3B.fasta'
	else:
		HOMOLOG1 = out1 +'ANC.H1.3.fasta'
		HOMOLOG2 = out1 +'ANC.H2.3.fasta'
	print('Simulating reads for {}\n'.format(LINE))
	cmd=(pirsPATH + ' simulate --diploid --no-substitution-errors --no-indel-errors --no-gc-content-bias -t 1 -q -z' +
		' -l '+str(rLen)+' -x '+str(cov)+' -m '+str(inSize)+
		' -s ' +LINE+ ' -o ' +out3+ ' '+HOMOLOG1+ ' '+HOMOLOG2)
	os.system(cmd)
	
	#####-----Simulate reads for unmutated CL
	for LINE in listCL:
		HOMOLOG1 = out2 +LINE+'.H1.4.snp.fa'
		HOMOLOG2 = out2 +LINE+'.H2.4.snp.fa'
		print('Simulating reads for {}\n'.format(LINE))
		cmd=(pirsPATH + ' simulate --diploid --no-substitution-errors --no-indel-errors --no-gc-content-bias -t 1 -q -z' +
			' -l '+str(rLen)+' -x '+str(cov)+' -m '+str(inSize)+
			' -s ' +LINE+ ' -o ' +out3+ ' '+HOMOLOG1+ ' '+HOMOLOG2)
		os.system(cmd)
	
	#####-----Simulate reads for MA
	LINE = 'MA'
	HOMOLOG1 = out2 +LINE+'.H1.4.snp.fa'
	HOMOLOG2 = out2 +LINE+'.H2.4.snp.fa'
	print('Simulating reads for {}\n'.format(LINE))
	cmd=(pirsPATH + ' simulate --diploid --no-substitution-errors --no-indel-errors --no-gc-content-bias -t 1 -q -z' +
		' -l '+str(rLen)+' -x '+str(cov)+' -m '+str(inSize)+
		' -s ' +LINE+ ' -o ' +out3+ ' '+HOMOLOG1+ ' '+HOMOLOG2)
	os.system(cmd)
	
	print('DONE!')
	
##########----------Run main()
if __name__ == "__main__":
    main()