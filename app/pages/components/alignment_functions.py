#tools and methods for alignment
#----------------------------------------------------------
import os
from pages.components.user_selection import species_lookup
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
import tempfile
import shutil
#----------------------------------------------------------
alignment_data = """>Example
MEEADLTLPLSQDTFHDLWNNVFLSTENESLAPPEGLLSQNMDFWEDPETMQETKNVPTA
PTVPAISNYAGEHGFNLEFNDSGTAKSVTSTYSVKLGKLFCQLAKTTPIGVLVKEEPPQG
>Example2
MEEADLTLPLSQDTFHDLWNNVFLSTENESLAPPEGLLSQNMDFWEDPETMQETKNVPTA
PTVPAISNYAGEHGFNLEFNDSGTAKSVTSTYSVKLGKLFCQLAKTTPIGVLVKEEPPQG"""

#----------------------------------------------------------
def read_in_alignment(species_selected, busco_name_selector):
    #TODO change this to read in data from a repo somewhere not local
    #TODO for now just read from cantata_data
    species_l = species_lookup(species_selected)
    #print(species_l)
    #print("species_selected ", species_selected)
    #print("busco_name_selector ", busco_name_selector)

    if species_selected != None and species_selected != "None":
        if busco_name_selector != None and busco_name_selector != "None":
            alignment = AlignIO.read(f"../../cantata_data/gb/{busco_name_selector}.shortheaders.aln-gb", "fasta")
            filtered_alignment = [seq for seq in alignment if any(species in seq.id for species in species_l)]
            alignment = MultipleSeqAlignment(filtered_alignment)
            fasta_string=""
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, "temp_file.txt")
                with open(temp_file_path, "w") as temp_file:
                    AlignIO.write(alignment, temp_file, "fasta")
                with open(temp_file_path, "r") as temp_file:
                    fasta_string = temp_file.read()

            #print("string: ", fasta_string)

            return fasta_string
    else:  
        return None
#----------------------------------------------------------

#----------------------------------------------------------