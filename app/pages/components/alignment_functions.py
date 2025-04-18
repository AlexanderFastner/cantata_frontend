#tools and methods for alignment
#----------------------------------------------------------
import os
import tempfile

from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment

from .user_selection import species_lookup
#----------------------------------------------------------
alignment_data = [">sp|Q9W678|P53_BARBU Cellular tumor antigen p53 OS=Barbus barbus GN=tp53 PE=2 SV=1MAESQEFAELWERNLISTQEAGTCWELINDEYLPSSFDPNIFDNVLTEQPQPSTSPPTASVPVATDYPGEHGFKLGFPQSGTAKSVTCTYSSDLNKLFCQLAKTCPVQMVVNVAPPQGSVIRATAIYKKSEHVAEVVRRCPHHERTPDGDGLAPAAHLIRVEGNSRALYREDDVNSRHSVVVPYEVPQLGSEFTTVLYNFMCNSSCMGGMNRRPILTIISLETHDGQLLGRRSFEVRVCACPGRDRKTEESNFRKDQETKTLDKIPSANKRSLTKDSTSSVPRPEGSKKAKLSGSSDEEIYTLQVRGKERYEMLKKINDSLELSDVVPPSEMDRYRQKLLTKGKKKDGQTPEPKRGKKLMVKDEKSDSD" ,
">sp|Q29537|P53_CANFA Cellular tumor antigen p53 OS=Canis familiaris GN=TP53 PE=2 SV=2MEESQSELNIDPPLSQETFSELWNLLPENNVLSSELCPAVDELLLPESVVNWLDEDSDDAPRMPATSAPTAPGPAPSWPLSSSVPSPKTYPGTYGFRLGFLHSGTAKSVTWTYSPLLNKLFCQLAKTCPVQLWVSSPPPPNTCVRAMAIYKKSEFVTEVVRRCPHHERCSDSSDGLAPPQHLIRVEGNLRAKYLDDRNTFRHSVVVPYEPPEVGSDYTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNVLGRNSFEVRVCACPGRDRRTEEENFHKKGEPCPEPPPGSTKRALPPSTSSSPPQKKKPLDGEYFTLQIRGRERYEMFRNLNEALELKDAQSGKEPGGSRAHSSHLKAKKGQSTSRHKKLMFKREGLDSD"]
#----------------------------------------------------------
def read_in_alignment(species_selected, busco_name_selector, type_selector):
    #filter based on type selected
    #if single -> make sure no duplicates
    #if duplicate selected only include dupllicate entries
    species_l = species_lookup(species_selected)

    #print(species_l)
    #print("species_selected ", species_selected)
    #print("busco_name_selector ", busco_name_selector)

    reduced_alignment = []
    alignment = AlignIO.read(f"/wd/gb/{busco_name_selector}.shortheaders.aln-gb", "fasta")
    filtered_alignment = [seq for seq in alignment if any(species in seq.id for species in species_l)]
    print("filtered_alignment", filtered_alignment)
    if type_selector == "single":
        # print("single selected")
        codes = []
        for record in filtered_alignment:
            #print(record)
            codes.append(record.id[-3:])
            print(record.id[-3:])
        dups = find_duplicates(codes)
        # print("dups", dups)
        for record in filtered_alignment:
            if record.id[-3:] in dups:
                # print("duplicate")
                # print(record)
                # print()
                record = None
            else:
                reduced_alignment.append(record)
    #remove duplicates
    if type_selector == "duplicated":
        # print("duplicated")
        # print(filtered_alignment)
        codes = []
        for record in filtered_alignment:
            codes.append(record.id[-3:])
            #print(record.id[-3:])
        dups = find_duplicates(codes)
        #print("dups", dups)
        for record in filtered_alignment:
            if record.id[-3:] in dups:
                reduced_alignment.append(record)
            else:
                record = None

    print("new alignment", reduced_alignment)

    alignment = MultipleSeqAlignment(reduced_alignment)
    fasta_string=""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "temp_file.txt")
        with open(temp_file_path, "w") as temp_file:
            AlignIO.write(alignment, temp_file, "fasta")
        with open(temp_file_path, "r") as temp_file:
            fasta_string = temp_file.read()

    #print("string: ", fasta_string)
    return fasta_string
#----------------------------------------------------------
def find_duplicates(lst):
    unique_items = set()
    duplicate_items = set()
    for item in lst:
        if item in unique_items:
            duplicate_items.add(item)
        else:
            unique_items.add(item)
    return list(duplicate_items)
#----------------------------------------------------------