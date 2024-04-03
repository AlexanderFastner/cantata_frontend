#What the user selects/can select
#----------------------------------------------------------
#TODO prot_buscso ids need to match ids in TransPi/Trinity .tsv

def get_species_list():
    species_list = []
    with open("./data/busco5_full_table_Proteome_df_numbers.csv") as f:
        species = [row.split(",")[0] for row in f]
        species=sorted(species[1:])
    return species
#----------------------------------------------------------
def get_busco_genes():
    #print("activated get_busco_genes")
    #return a list of all the busco genes
    #TODO get this and functions list from sergio
    #add that too data and query here
    busco_genes = ["55162at33208"]

    return busco_genes
#----------------------------------------------------------
def get_busco_functions():
    #print("activated get_busco_functions")
    #return a list of the various busco functions

    busco_function = ["do something"]
    return busco_function
#----------------------------------------------------------
#contain the various selecatble groups
group_options=[
    {"label": "None","value": "None"},
    {"label": "All","value": "All"},
    {"label": "Annelida-Polychaeta","value": "Platynereis_dumerilii"},
    {"label": "Arthropoda-Branchiopoda","value": "Daphnia_pulex"},
    {"label": "Choanozoa-Choanoflagellatea","value": "Acanthoeca_spectabilis,Helgoeca_nana,Salpingoeca_infusionum"},
    {"label": "Chordata-Leptocardii","value": "Branchiostoma_floridae"},
    {"label": "Chordata-Teleostei","value": "Danio_rerio"},
    {"label": "Cnidaria-Anthozoa","value": "Actinia_tenebrosa,Anemonia_sulcata,Anemonia_viridis,Anthopleura_dowii,Anthopleura_elegantissima,Aulactinia_veratra,Calliactis_polypus,Condylactis_gigantea,Edwardsiella_carnea,Entacmaea_quadricolor,Heteractis_crispa,Megalactis_griffithsi,Nematostella_vectensis,Stichodactyla_haddoni,Stichodactyla_helianthus,Antipathes_caribbeana,Plumapathes_pennacea,Corynactis_australis,Rhodactis_indosinensis,Alcyonium_palmatum,Clavularia_sp,Dendronephthya_gigantea,Eunicea_calyculata,Eunicella_cavolini,Gorgonia_ventalina,Muricea_laxa,Phenganax_sp,Sarcothelia_edmonsoni,Sinularia_cruciata,Tubipora_musica,Xenia_sp,Acropora_aculeus,Acropora_cervicornis,Acropora_digitifera,Acropora_millepora,Acropora_tenuis,Agaricia_lamarcki,Alveopora_japonica,Coelastrea_aspera,Ctenactis_echinata,Cyphastrea_serailia,Dendrophyllia_sp,Dipsastraea_rotumana,Favites_acuticollis,Fungia_fungites,Galaxea_astreata,Goniastrea_retiformis,Goniopora_columna,Lobactis_scutaria,Montastraea_cavernosa,Montipora_aequituberculata,Montipora_capitata,Montipora_digitata,Plesiastrea_versipora,Pocillopora_damicornis,Porites_astreoides,Porites_australiensis,Porites_lobata,Porites_lutea,Pseudodiploria_strigosa,Seriatopora_hystrix,Siderastrea_siderea,Tubastraea_coccinea,Corallium_rubrum,Heliopora_coerulea,Palythoa_caribaeorum,Palythoa_variabilis,Protopalythoa_variabilis"},
    {"label": "Cnidaria-Cubozoa","value": "Copula_sivickisi,Tripedalia_cystophora,Chironex_fleckeri"},
    {"label": "Cnidaria-Hydrozoa","value": "Hydractinia_symbiolongicarpus,Hydra_oligactis,Hydra_viridissima,Hydra_vulgaris,Millepora_alcicornis,Turritopsis_sp,Liriope_tetraphylla,Aegina_citrea,Apolemia_lanosa,Bargmannia_amoena,Bargmannia_elongata,Bargmannia_lata,Chelophyes_appendiculata,Chuniphyes_multidentata,Craseoa_lathetica,Desmophyes_sp,Erenna_richardi,Forskalia_asymmetrica,Hippopodius_hippopus,Lilyopsis_fluoracantha,Lychnagalma_utricularia,Marrus_claudanielis,Nanomia_bijuga,Physalia_physalis,Resomia_ornicephala,Rhizophysa_filiformis,Stephalia_dilata,Stephalia_sp"},
    {"label": "Cnidaria-Scyphozoa","value": "Atolla_vanhoeffeni,Nemopilema_nomurai,Stomolophus_meleagris,Aurelia_aurita,Chrysaora_fuscescens,Cyanea_capillata,Cyanea_nozakii,Pelagia_noctiluca"},
    {"label": "Cnidaria-Staurozoa","value": "Calvadosia_campanulata,Calvadosia_cruxmelitensis,Craterolophus_convolvulus,Haliclystus_auricula"},
    {"label": "Ctenophora-Nuda","value": "Beroe_abyssicola,Beroe_forskalii,Beroe_ovata"},
    {"label": "Ctenophora-Tentaculata","value": "Cestum_veneris,Velamen_paralellum,Aulacoctena_acuminata,Bathyctena_chuni,Charistephane_fugiens,Dryodora_glandiformis,Euplokamis_dunlapae,Haeckelia_beehleri,Haeckelia_rubra,Hormiphora_californensis,Lampea_lactea,Lampea_sp,Bathocyroe_fosteri,Bolinopsis_microptera,Deiopea_kaloktenota,Kiyohimea_sp_WRF2015,Lampocteis_cruentiventer,Leucothea_pulchra,Lobata_sp_VWRF2014,Ocyropsis_maculata,Thalassocalyce_inconstans"},
    {"label": "Ctenophora-Indet","value": "Ctenophora_sp_BWRF2014,Ctenophora_sp_CWRF2014,Ctenophora_sp_KWRF2015,Ctenophora_sp_L1WRF2015,Ctenophora_sp_L2WRF2015,Ctenophora_sp_MWRF2015,Ctenophora_sp_N1WRF2014,Ctenophora_sp_N2WRF2014,Ctenophora_sp_PWRF2015,Ctenophora_sp_TWRF2014,Ctenophora_sp_WWRF2014,Ctenophora_sp_XWRF2015"},
    {"label": "Echinodermata-Crinoidea","value": "Oligometra_serripinna"},
    {"label": "Echinodermata-Echinoidea","value": "Strongylocentrotus_purpuratus,Eucidaris_tribuloides"},
    {"label": "Hemichordata-Enteropneusta","value": "Ptychodera_flava"},
    {"label": "Nemertea-Palaeonemertea","value": "Tubulanus_polymorphus"},
    {"label": "Placozoa-Uniplacotomia","value": "Hoilungia_hongkongensis,Trichoplax_adherens"},
    {"label": "Porifera-Calcarea","value": "Leuconia_nivea,Clathrina_coriacea,Leucetta_chagosensis,Grantia_compresa,Sycon_cyliatum,Sycon_ciliatum,Sycon_coactum,Janusya_sp"},
    {"label": "Porifera-Demospongiae","value": "Cymbastella_concentrica,Halisarca_dujardinii,Chondrosia_reniformis,Cliona_varians,Dendrilla_antarctica,Dysidea_avara,Lendenfeldia_chondrodes,Pleraplysilla_spinifera,Sarcotragus_fasciculatus,Spongia_officinalis,Vaceletia_crypta,Amphimedon_queenslandica,Haliclona_amboinensis,Haliclona_tubifera,Neopetrosia_compacta,Petrosia_ficiformis,Xestospongia_testudinaria,Crella_elegans,Latrunculia_apicalis,Mycale_cecilia,Mycale_phylophylla,Tedania_anhelans,Baikalospongia_bacillifera,Ephydatia_muelleri,Lubomirskia_abietina,Lubomirskia_baikalensis,Spongilla_lacustris,Halichondria_panicea,Pseudospongosorites_suberitoides,Tethya_wilhelma,Cinachyrella_alloclada,Geodia_atlantica,Geodia_hentscheli,Geodia_macandrewii,Geodia_phlegraei,Aplysina_aerophoba,Scopalina_sp,Isodyctia_sp,Poecilosclerida_sp"},
    {"label": "Porifera-Hexactinellida","value": "Amphidiscella_abyssalis,Aulocalyx_serialis,Bolosoma_cyanae,Caulophacus_discohexaster,Chaunoplectella_NIWA126325,Corbitella_NIWA126123,Regadrella_okinoseana,Rossellidae_NIWA126310,Saccocalyx_tetractinus,Trychella_NIWA126306,Walteria_leuckarti,Eurete_NIWA126276,Farrea_occa,Farrea_similaris"},
    {"label": "Porifera-Homoscleromorpha","value": "Corticium_candelabrum,Oscarella_lobularis,Oscarella_pearsei,Plakina_jani"},
    {"label": "Priapulida-Indet","value": "Priapulus_caudatus"},
    {"label": "Xenacoelomorpha-Indet","value": "Symsagittifera_roscoffensis,Xenoturbella_bocki"},
    {"label": "Indet-Filasterea","value": "Capsaspora_owczarzaki"},
    {"label": "Indet-Ichthyosporea","value": "Amoebidium_parasiticum,Abeoforma_whisleri,Ichthyosporea_XGB-2017a"},
]
#----------------------------------------------------------
#TODO add dictionary lookup for species codes
#sergio mde a .csv in Cantata
species_codes = {"Platynereis_dumerilii": "PDU",
"Daphnia_pulex": "DPU",
"Acanthoeca_spectabilis": "ASP",
"Helgoeca_nana": "HNA",
"Salpingoeca_infusionum": "SIN",
"Branchiostoma_floridae": "BFL",
"Danio_rerio": "DRE",
"Actinia_tenebrosa": "ATN",
"Anemonia_sulcata": "ASU",
"Anemonia_viridis": "AVI",
"Anthopleura_dowii": "ADO",
"Anthopleura_elegantissima": "AEL",
"Aulactinia_veratra": "AVE",
"Calliactis_polypus": "CPO",
"Condylactis_gigantea": "CGI",
"Edwardsiella_carnea": "ECA",
"Entacmaea_quadricolor": "EQU",
"Heteractis_crispa": "HCR",
"Megalactis_griffithsi": "MGR",
"Nematostella_vectensis": "NVE",
"Stichodactyla_haddoni": "SHA",
"Stichodactyla_helianthus": "SHE",
"Antipathes_caribbeana": "ACA",
"Plumapathes_pennacea": "PPE",
"Corynactis_australis": "CAU",
"Rhodactis_indosinensis": "RIN",
"Alcyonium_palmatum": "APA",
"Clavularia_sp": "CN1",
"Dendronephthya_gigantea": "DGI",
"Eunicea_calyculata": "ECL",
"Eunicella_cavolini": "ECV",
"Gorgonia_ventalina": "GVE",
"Muricea_laxa": "MLA",
"Phenganax_sp": "CN2",
"Sarcothelia_edmonsoni": "SED",
"Sinularia_cruciata": "SCR",
"Tubipora_musica": "TMU",
"Xenia_sp": "CN3",
"Acropora_aculeus": "ACU",
"Acropora_cervicornis": "ACE",
"Acropora_digitifera": "ADI",
"Acropora_millepora": "AMI",
"Acropora_tenuis": "ATE",
"Agaricia_lamarcki": "ALM",
"Alveopora_japonica": "AJA",
"Coelastrea_aspera": "CAS",
"Ctenactis_echinata": "CEC",
"Cyphastrea_serailia": "CSE",
"Dendrophyllia_sp": "CN4",
"Dipsastraea_rotumana": "DRO",
"Favites_acuticollis": "FAC",
"Fungia_fungites": "FFU",
"Galaxea_astreata": "GAS",
"Goniastrea_retiformis": "GRE",
"Goniopora_columna": "GCO",
"Lobactis_scutaria": "LSC",
"Montastraea_cavernosa": "MCA",
"Montipora_aequituberculata": "MAE",
"Montipora_capitata": "MCP",
"Montipora_digitata": "MDI",
"Plesiastrea_versipora": "PVE",
"Pocillopora_damicornis": "PDA",
"Porites_astreoides": "PAS",
"Porites_australiensis": "PAU",
"Porites_lobata": "PLO",
"Porites_lutea": "PLU",
"Pseudodiploria_strigosa": "PST",
"Seriatopora_hystrix": "SHY",
"Siderastrea_siderea": "SSI",
"Tubastraea_coccinea": "TCO",
"Corallium_rubrum": "CRU",
"Heliopora_coerulea": "HCO",
"Palythoa_caribaeorum": "PCA",
"Palythoa_variabilis": "PVA",
"Protopalythoa_variabilis": "PVR",
"Copula_sivickisi": "CSI",
"Tripedalia_cystophora": "TCY",
"Chironex_fleckeri": "CFL",
"Hydractinia_symbiolongicarpus": "HSY",
"Hydra_oligactis": "HOL",
"Hydra_viridissima": "HVI",
"Hydra_vulgaris": "HVU",
"Millepora_alcicornis": "MAL",
"Turritopsis_sp": "CN5",
"Liriope_tetraphylla": "LTE",
"Aegina_citrea": "ACI",
"Apolemia_lanosa": "ALA",
"Bargmannia_amoena": "BAM",
"Bargmannia_elongata": "BEL",
"Bargmannia_lata": "BLA",
"Chelophyes_appendiculata": "CAP",
"Chuniphyes_multidentata": "CMU",
"Craseoa_lathetica": "CLA",
"Desmophyes_sp": "CN6",
"Erenna_richardi": "ERI",
"Forskalia_asymmetrica": "FAS",
"Hippopodius_hippopus": "HHI",
"Lilyopsis_fluoracantha": "LFL",
"Lychnagalma_utricularia": "LUT",
"Marrus_claudanielis": "MCL",
"Nanomia_bijuga": "NBI",
"Physalia_physalis": "PPH",
"Resomia_ornicephala": "ROR",
"Rhizophysa_filiformis": "RFI",
"Stephalia_dilata": "SDI",
"Stephalia_sp": "CN7",
"Atolla_vanhoeffeni": "AVA",
"Nemopilema_nomurai": "NNO",
"Stomolophus_meleagris": "SME",
"Aurelia_aurita": "AAU",
"Chrysaora_fuscescens": "CFS",
"Cyanea_capillata": "CCP",
"Cyanea_nozakii": "CNO",
"Pelagia_noctiluca": "PNO",
"Calvadosia_campanulata": "CCM",
"Calvadosia_cruxmelitensis": "CCR",
"Craterolophus_convolvulus": "CCN",
"Haliclystus_auricula": "HAU",
"Beroe_abyssicola": "BAB",
"Beroe_forskalii": "BFR",
"Beroe_ovata": "BOV",
"Cestum_veneris": "CVE",
"Velamen_paralellum": "VPA",
"Aulacoctena_acuminata": "AAC",
"Bathyctena_chuni": "BCH",
"Charistephane_fugiens": "CFU",
"Dryodora_glandiformis": "DGL",
"Euplokamis_dunlapae": "EDU",
"Haeckelia_beehleri": "HBE",
"Haeckelia_rubra": "HRU",
"Hormiphora_californensis": "HCA",
"Lampea_lactea": "LLA",
"Lampea_sp": "CT1",
"Bathocyroe_fosteri": "BFO",
"Bolinopsis_microptera": "BMI",
"Deiopea_kaloktenota": "DKA",
"Kiyohimea_sp_WRF2015": "CT2",
"Lampocteis_cruentiventer": "LCR",
"Leucothea_pulchra": "LPU",
"Lobata_sp_VWRF2014": "CT3",
"Ocyropsis_maculata": "OMA",
"Thalassocalyce_inconstans": "TIN",
"Ctenophora_sp_BWRF2014": "CT4",
"Ctenophora_sp_CWRF2014": "CT5",
"Ctenophora_sp_KWRF2015": "CT6",
"Ctenophora_sp_L1WRF2015": "CT7",
"Ctenophora_sp_L2WRF2015": "CT8",
"Ctenophora_sp_MWRF2015": "CT9",
"Ctenophora_sp_N1WRF2014": "CT10",
"Ctenophora_sp_N2WRF2014": "CT11",
"Ctenophora_sp_PWRF2015": "CT12",
"Ctenophora_sp_TWRF2014": "CT13",
"Ctenophora_sp_WWRF2014": "CT14",
"Ctenophora_sp_XWRF2015": "CT15",
"Oligometra_serripinna": "OSE",
"Strongylocentrotus_purpuratus": "SPU",
"Eucidaris_tribuloides": "ETR",
"Ptychodera_flava": "PFL",
"Tubulanus_polymorphus": "TPO",
"Hoilungia_hongkongensis": "HHO",
"Trichoplax_adherens": "TAD",
"Leuconia_nivea": "LNI",
"Clathrina_coriacea": "CCI",
"Leucetta_chagosensis": "LCA",
"Grantia_compresa": "GCM",
"Sycon_ciliatum": "SCI",
"Sycon_coactum": "SCO",
"Cymbastella_concentrica": "CCO",
"Halisarca_dujardinii": "HDU",
"Chondrosia_reniformis": "CRE",
"Cliona_varians": "CVA",
"Dendrilla_antarctica": "DAN",
"Dysidea_avara": "DAV",
"Lendenfeldia_chondrodes": "LCH",
"Pleraplysilla_spinifera": "PSP",
"Sarcotragus_fasciculatus": "SFA",
"Spongia_officinalis": "SOF",
"Vaceletia_crypta": "VCR",
"Amphimedon_queenslandica": "AQU",
"Haliclona_amboinensis": "HAM",
"Haliclona_tubifera": "HTU",
"Neopetrosia_compacta": "NCO",
"Petrosia_ficiformis": "PFI",
"Xestospongia_testudinaria": "XTE",
"Crella_elegans": "CEL",
"Latrunculia_apicalis": "LAP",
"Mycale_cecilia": "MCE",
"Mycale_phylophylla": "MPH",
"Tedania_anhelans": "TAN",
"Baikalospongia_bacillifera": "BBA",
"Ephydatia_muelleri": "EMU",
"Lubomirskia_abietina": "LAB",
"Lubomirskia_baikalensis": "LBA",
"Spongilla_lacustris": "SLA",
"Halichondria_panicea": "HPA",
"Pseudospongosorites_suberitoides": "PSU",
"Tethya_wilhelma": "TWI",
"Cinachyrella_alloclada": "CAL",
"Geodia_atlantica": "GAT",
"Geodia_hentscheli": "GHE",
"Geodia_macandrewii": "GMA",
"Geodia_phlegraei": "GPH",
"Aplysina_aerophoba": "AAE",
"Amphidiscella_abyssalis": "AAB",
"Aulocalyx_serialis": "ASE",
"Bolosoma_cyanae": "BCY",
"Caulophacus_discohexaster": "CDI",
"Chaunoplectella_NIWA126325": "PO1",
"Corbitella_NIWA126123": "PO2",
"Regadrella_okinoseana": "ROK",
"Rossellidae_NIWA126310": "PO3",
"Saccocalyx_tetractinus": "STE",
"Trychella_NIWA126306": "PO4",
"Walteria_leuckarti": "WLE",
"Eurete_NIWA126276": "PO5",
"Farrea_occa": "FOC",
"Farrea_similaris": "FSI",
"Corticium_candelabrum": "CCA",
"Oscarella_lobularis": "OLO",
"Oscarella_pearsei": "OPE",
"Plakina_jani": "PJA",
"Priapulus_caudatus": "PCU",
"Symsagittifera_roscoffensis": "SRO",
"Xenoturbella_bocki": "XBO",
"Capsaspora_owczarzaki": "COW",
"Amoebidium_parasiticum": "APR",
"Abeoforma_whisleri": "AWH",
"Scopalina_sp": "PO6",
"Isodyctia_sp": "PO7",
"Poecilosclerida_sp": "PO8",
"Janusya_sp": "PO9",
"Ichthyosporea_XGB-2017a": "OU1",
"Axinella_polypoides": "APO",
"Ephydatia_fluviatilis": "EFL",
}
#----------------------------------------------------------
def species_lookup(species_list):
    species_c = []
    #get dict of species : species name
    # with open("./data/CANTATA_species_WoRMS_matched.csv","r") as t:
    #     for line in t:
    #         line=line.split(",")
    #         print(f'"{line[0]}": "{line[1]}",')

    for item in species_list:
        species_c.append(str(species_codes.get(item)))

    return species_c
#----------------------------------------------------------