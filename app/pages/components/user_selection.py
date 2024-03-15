#What the user selects
#----------------------------------------------------------
#TODO prot_buscso ids need to match ids in TransPi/Trinity .tsv


def get_species_list():
    species_list = []
    with open("./data/prot_busco_df_numbers.csv") as f:
        species = [row.split(",")[0] for row in f]
        species=species[1:]
    return species
#----------------------------------------------------------