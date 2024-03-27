#tools and methods for alignment
#----------------------------------------------------------
import os
import pandas as pd
from pages.components.user_selection import species_lookup
import dash_bio as dashbio
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from io import StringIO
import urllib.request as urlreq
#----------------------------------------------------------
alignment_data = """>Example
MEEADLTLPLSQDTFHDLWNNVFLSTENESLAPPEGLLSQNMDFWEDPETMQETKNVPTA
PTVPAISNYAGEHGFNLEFNDSGTAKSVTSTYSVKLGKLFCQLAKTTPIGVLVKEEPPQG
>Example2
MEEADLTLPLSQDTFHDLWNNVFLSTENESLAPPEGLLSQNMDFWEDPETMQETKNVPTA
PTVPAISNYAGEHGFNLEFNDSGTAKSVTSTYSVKLGKLFCQLAKTTPIGVLVKEEPPQG"""

#----------------------------------------------------------
def read_in_alignment(species_selected, busco_name_selector):
    #TODO make lookup table for species->3 letter code
    species_l = species_lookup(species_selected)
    #print("species_selected ", species_selected)
    #print("busco_name_selector ", busco_name_selector)

    if species_selected != None and species_selected != "None":
        if busco_name_selector != None and busco_name_selector != "None":
            alignment = AlignIO.read(f"./data/testing_alignments/{busco_name_selector}.shortheaders.aln-gb", "fasta")
            filtered_alignment = [seq for seq in alignment if any(species in seq.id for species in species_l)]
            alignment = MultipleSeqAlignment(filtered_alignment)
            fasta_string=""
            with open("temp_alignment.fasta", "w") as handle:
                AlignIO.write(alignment, handle, "fasta")
            with open("temp_alignment.fasta", "r") as handle:
                fasta_string = handle.read()

            #print("string: ", fasta_string)

            return fasta_string
    else:  
        return None
#----------------------------------------------------------

#----------------------------------------------------------