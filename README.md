# *simMutAccumSV*

## Description
SimMutAccumSV simulates a mutation accumulation (MA) experiment by introducing structural variants into a diploid genome using SVsim (https://github.com/GregoryFaust/SVsim). After mutations are simulated in the given genome, pIRS (Hu et al. 2012) is used to generate paired-end reads for all lines.

## Requirements
- Python v3.7
- pIRS (https://github.com/galaxy001/pirs)
- SVsim (https://github.com/GregoryFaust/SVsim)


## Usage

```
usage: simMutAccumSV.2.0.py <required> [optional] 
  -wd WD            <Full path to working directory (include prefix for new folders)>
  -pirs PIRSPATH    <Full path to pIRS (including /pirs at the end)>
  -svsim SVSIMPATH  <Full path to SVsim (including /SVsim at the end)>
  -c REFCHROM       <Chromosome to simulate in fasta format (must contain only one sequence)>
  -ncl NCL          <Number of non-focal MA lines to simulate (clones of Ancestor)>
  -nhet NHET        <Number of shared heterozygous TE sites to simulate>
  -snp SNPRATE      [pIRS: Rate of heterozygosity for haploid genome]
  -x COV            [pIRS: Coverage for pIRS to simulate]
  -rlen RLEN        [pIRS: Read length for pIRS to simulate]
  -insz INSIZE      [pIRS: Insert size for pIRS to simulate]
  -svs SVSEED       <SVsim: Seed for random number generator>
  -svfa SVFILEANC   <SVsim: .sim file containing arguments to simulate SV for Ancestral line>
  -svna SVNUMANC    <SVsim: number of replicate SVs for Ancestral line>
  -svfm SVFILEMA    <SVsim: .sim file containing arguments to simulate SV for MA line>
  -svnm SVFILEMA    <SVsim: number of replicate SVs for MA line>
  -mut MUTTYPE      <Regime of mutations to simulation (described below)> 

```
## Description
All the output will be place in the working directory specified by <em>wd</em>.  
The output will be placed into three subdirectories in the working directory: step1/, step2/, step3/

### Step 1
SimMutAccumSV will introduce structural variant mutations onto the genome fasta file (<em>c</em>).

First, pIRS (Hu et al. 2012) is used to generate a diploid ancestor (ANC) genome by duplicating the given genome fasta file and adding SNPs at a specified rate (<em>snp</em>); the fasta files of each homolog of ANC is ouput as ANC.H1.1.snp.fa and ANC.H2.1.snp.fa with the list of simualted SNPS recored in ANC.H1.1.lst and ANC.H2.1.lst.
pIRS requires that fasta file does not contain N's. 


Next, <em>svna</em> "ancestral" SVs as specified by <em>svfa</em> are added to all lines and <em>svnm</em> "MA" SVs as specified by <em>svfm</em> are added to one MA line. <em>svfa</em> and <em>svfm</em> are used for the -i argument in SVsim and must follow the specified format. <em>svna</em> and <em>svnm</em> are used for the -n argument in SVsim. The random seed <em>svs</em> is used for the -s argument in SVsim.  
Note: This program has only been tested for introducting DEL, DUP, and INV mutation types in SVsim.


Argument <em>mut</em> determines the form of SV mutation that is introduced: 
* <em>mut</em> = 1 will introduce heterozygous SVs in all lines and homozygous reference -> heterozygous SV mutations in the MA line.
* <em>mut</em> = 2 will introduce homozygous SVs in all lines and heterozygous SVs -> homozygous SVs in the MA line.
* <em>mut</em> = 3 will introduce heterozygous SVs in all lines and heterozygous SVs -> homozygous reference in the MA line.
* <em>mut</em> = 4 will introduce homozygous SVs in all lines and SVs mutations of all three types in the MA line.


Fasta files of the ANC genome with SV mutations will be output as ANC.H1.3.fasta and ANC.H1.3.fasta (if <em>mut</em> = 4, then it will be ANC.H1.3B.fasta and ANC.H2.3B.fasta).  
Fasta files of the MA genome with SV mutations will be output as MA.H1.3.fasta and MA.H1.3.fasta (if <em>mut</em> = 4, then it will be MA.H1.3B.fasta and MA.H2.3B.fasta).


### Step 2
After adding the SV mutations into the genome, pIRS (Hu et al. 2012) is used to generate <em>ncl</em> unmutated descendant lines using the ANC genome as reference and adding SNPs at a specified rate (<em>snp</em>). Fasta files of these descendant lines are output as CL{i}.H1.4.snp.fa and CL{i}.H2.4.snp.fa, where {i} goes from 1 to <em>ncl</em>.


Similarly, SNPs will be added to the focal MA line at a specified rate (<em>snp</em>). Fasta files of these MA line is output as MA.H1.4.snp.fa and MA.H2.4.snp.fa.

### Step 3
After all mutations have been simulated, pIRS (Hu et al. 2012) is used to generate paired-end reads with read length <em>rlen</em> and insert size <em>insz</em> at a diploid coverage of <em>x</em>.
* Reads for the ANC line is simulated using ANC.H1.3.fasta and ANC.H2.3.fasta (ANC.H1.3B.fasta and ANC.H2.3B.fasta, if <em>mut</em> = 4) and output as ANC_1.fq.gz and ANC_2.fq.gz.
* Reads for the CL lines are simulated using CL{i}.H1.4.snp..fa and CL{i}.H2.4.snp.fa and output as CL{i}_1.fq.gz and CL{i}_2.fq.gz.
* Reads for the MA line is simulated using MA.H1.4.snp.fa and MA.H2.4.snp.fa and output as MA_1.fq.gz and MA_2.fq.gz.

## References
- Hu X, Yuan J, Shi Y, Lu J, Liu B, Li Z, Chen Y, Mu D, Zhang H, Yue Z, Bai F, Li H, Fan W. pIRS: Profile-based illumine pair-end reads simulator. Bioinformatics. 2012;28(11):1533-35.

## Citation
If you used simMutAccumSV in you work, please cite:
