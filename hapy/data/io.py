"""
Functions to read in genomics files.

Currently support:
- [Phased Beagle file](http://faculty.washington.edu/browning/beagle/b3.html) to process AA_ variant IDs.
- [SNP2HLA](https://software.broadinstitute.org/mpg/snp2hla/snp2hla_manual.html) dosage files.

Some of the data processing code adapted from [here](https://github.com/immunogenomics/HLA-TAPAS/blob/master/HLAassoc/run_omnibus_test_WS.R)
"""
__all__ = ["read_famfile", "read_bgl", "read_gprobs", "read_dosage"]
import pandas as pd
import numpy as np

def read_famfile(fileloc):
    """
    Reads PLINK fam file and gives it appropriate headers

    Parameters
    ------------
    fileloc: str,
        file location of the fam file
    Returns
    ------------
    df: pandas DataFrame
        processed beagle file ready for haplotype matrix generation
    """
    fam = pd.read_csv(fileloc,
                    sep=r"\s+", names=["FID", "IID", "FAT", "MOT", "SEX", "PHENO"] ,na_values = [-9,"-9"])
    return fam

def read_bgl(fileloc, simpleQC=True):
    """
    Processes Beagle (phased) file and store it as HLAdat object. This gives the hardcall of the variants.

    Parameters
    ------------
    fileloc: str,
        file location of the beagle (phased) file
    Returns
    ------------
    hladat: HLAdat
        HLAdat object that has dataframe of the genomic data files
    """
    df = pd.read_csv(fileloc, sep=r"\s+", header=0, index_col=1)#.drop(columns=["I"], axis=1)
    markers = df.columns[0]
    df = df[df[markers]=="M"]  #pylint: disable=E1136
    df = df.drop(markers, axis=1)

    df.index.name = "SNP"

    df["SNP"] = df.index
    df[['AA_ID', 'TYPE', 'GENE', 'AA_POS', 'POS']] = df.apply(lambda x: breakitup(x["SNP"]), axis=1,result_type="expand")

    df = df.drop(columns=["SNP"], axis=1)


    return df

def read_gprobs(fileloc, simpleQC=True):
    """
    Processes Beagle probability (phased) file, transform it into dosage file and store it as HLAdat object. Dosage is the probabilistic gene copy information.

    Parameters
    ------------
    fileloc: str,
        file location of the beagle probability (phased) file
    Returns
    ------------
    hladat: HLAdat
        HLAdat object that has dataframe of the genomic data files
    """

def read_dosage(fileloc, simpleQC=True):
    """
    Processes dosage file and store it as HLAdat object. Dosage is the probabilistic gene copy information.

    Parameters
    ------------
    fileloc: str,
        file location of the dosage file
    Returns
    ------------
    hladat: HLAdat
        HLAdat object that has dataframe of the genomic data files
    """


def breakitup(variantID):
    """
    Function called by processBGL() to break variant IDs to different columns for sorting purpose

    Parameters
    ------------
    variantID: str,
        variant ID from genotype files
    Returns
    ------------
    idname,variantype,genename,aapos,genepos : str
        idname - cleaned up id
        variantype - SNPS, HLA or AA
        genename - name of Gene if it is an amino acid variant
        aapos - amino acid position number
        genepos - genomic coordinate
    """
    tokens = variantID.split("_")
    if len(tokens) > 1:
        idname = ("_").join(tokens[:4])
        while len(tokens)<4:
            tokens.append(np.nan)
        variantype = tokens[0]
        genename = tokens[1]
        aapos = tokens[2]
        genepos = tokens[3]
    else:
        idname = variantID
        if variantID.startswith("rs"):
            variantype = "SNPS"
        else:
            variantype = variantID
        genename = np.nan
        aapos = np.nan
        genepos = np.nan

    return idname,variantype,genename,aapos,genepos
