#tools and methods for alignment
#----------------------------------------------------------
import os
import pandas as pd
from pages.components.user_selection import species_lookup
#----------------------------------------------------------
def read_in_alignment(species_selected, busco_name_selector):
    #open busco file
    #retrieve data for that species by 3 letter code
    #TODO make lookup table for species->3 letter code
    species_l = species_lookup(species_selected)

    #TODO needs to be a dataframe, not a dict, we can have the same code with varying sequences

    sequences = []
    current_sequence = None
    with open(file=f"./data/testing_alignments/{busco_name_selector}.shortheaders.aln-gb") as busco_file:
        for line in busco_file:
            if line.startswith(">"):
                code = line.split("|")[1].strip()
                if current_sequence:
                    sequences.append(current_sequence)
                current_sequence = [code]
            elif current_sequence:
                current_sequence.append(line.strip())

    # Add the last sequence
    if current_sequence:
        sequences.append(current_sequence)

    code_data=[]
    sequence_data=[]
    for sequence in sequences:
        if sequence[0] in species_l:
            # print("Sequence for code: ", sequence[0])
            # print("Sequence: ", "".join(sequence[1:]))
            # print()
            code_data.append(sequence[0])
            sequence_data.append("".join(sequence[1:]))

    
    data={'code': code_data, 'sequence': sequence_data}
    out_df = pd.DataFrame(data)
    #print(out_df)

    return out_df
#----------------------------------------------------------