#This is for all functions pertaining to generating the heatmap from busco data
#----------------------------------------------------------
import os

#----------------------------------------------------------
def get_species_list():
    species_list = []
    with open("./data/prot_busco_df.csv") as f:
        species = [row.split(",")[0] for row in f]
        species=species[1:]
    return species
#----------------------------------------------------------
