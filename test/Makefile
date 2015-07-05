SHELL := /bin/bash 

# Point this to the directory which has BWA
B = /Users/ratan/third-party/bwa-0.7.10
# Point this to the directory which has WGSIM
P = /Users/ratan/third-party/wgsim
# Point this to the directory which has SAMtools
S = /Users/ratan/third-party/samtools-0.1.19
# Point this to the jar file for Picard
Y = /Users/ratan/third-party/broadinstitute-picard-64637e8/dist/picard.jar

C = ../src
R = reference.fa

all: simulate run

simulate: 
	$S/samtools faidx $R
	java -jar $Y CreateSequenceDictionary R=$R O=reference.dict
	$P/wgsim -d 500 -s 30 -1 100 -2 100 -N 24000 reference.fa Illumina_100_500_1.fq Illumina_100_500_2.fq
	$B/bwa index -a bwtsw $R 

run:
	./../src/find_concordant_assignments reference.fa <($B/bwa mem -t 4 -R '@RG\tID:foo\tSM:bar' -a $R Illumina_100_500_1.fq | $S/samtools view -bST $R -) <($B/bwa mem -t 4 -R '@RG\tID:foo\tSM:bar' -a $R Illumina_100_500_2.fq | $S/samtools view -bST $R -)  > blast.out

clean:
	ls -1 | grep -v "Makefile\|reference.fa" | xargs rm
	rm reference.fa.*
