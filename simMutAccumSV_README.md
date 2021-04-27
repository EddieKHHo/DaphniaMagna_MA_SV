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
  -mut MUTTYPE      <Type of MA mutation to simulation (described below)> 

```

SimMutAccumSV will introduce structural variant mutations onto the genome fasta file (<em>c</em>).

First, pIRS (Hu et al. 2012) is used to generate a diploid ancestor (ANC) genome by duplicating the given genome fasta file and adding SNPs at a specified rate (<em>snp</em>); the fasta files of each homolog of ANC is stored in step1/ as ANC.H1.snp.fa and ANC.H2.snp.fa with the list of simualted SNPS recored in ANC.H1.snp.lst and ANC.H2.snp.lst.
pIRS requires that fasta file does not contain N's. 



After all mutations have been simulated, pIRS (Hu et al. 2012) is used to generate paired-end reads with read length <em>rlen</em> and insert size <em>insz</em> at a diploid coverage of <em>x</em>. Reads for the ancestral and <em>ncl</em> non-focal descendent lines are simulated using ANC.H1.4.fa and ANC.H2.4.fa while those for the focal MA line are simulated from MA.H1.4.fa and MA.H2.4.fa. Reads for all lines are stored as fastq format in step3/.

## References
- Hu X, Yuan J, Shi Y, Lu J, Liu B, Li Z, Chen Y, Mu D, Zhang H, Yue Z, Bai F, Li H, Fan W. pIRS: Profile-based illumine pair-end reads simulator. Bioinformatics. 2012;28(11):1533-35.

## Citation
If you used simMutAccumSV in you work, please cite:
