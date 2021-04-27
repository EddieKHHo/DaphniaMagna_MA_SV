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
  -svfa SVFILEANC   <SVsim: .sim file containing arguments to simulate SV for ancestral line>
  -svna SVNUMANC    <SVsim: number of replicate SVs for ancestral line>
  -svfm SVFILEMA    <SVsim: .sim file containing arguments to simulate SV for MA line>
  -svnm SVFILEMA    <SVsim: number of replicate SVs for MA line>
  -mut MUTTYPE      <Type of MA mutation to simulation (described below)> 

```


## References
- Hu X, Yuan J, Shi Y, Lu J, Liu B, Li Z, Chen Y, Mu D, Zhang H, Yue Z, Bai F, Li H, Fan W. pIRS: Profile-based illumine pair-end reads simulator. Bioinformatics. 2012;28(11):1533-35.

## Citation
If you used simMutAccumSV in you work, please cite:
