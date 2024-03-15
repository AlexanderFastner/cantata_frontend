#What the user selects
#----------------------------------------------------------
#TODO prot_buscso ids need to match ids in TransPi/Trinity .tsv

def get_species_list():
    species_list = []
    with open("./data/prot_busco_df_numbers.csv") as f:
        species = [row.split(",")[0] for row in f]
        species=sorted(species[1:])
        with open("./data/TransPi.tsv") as t:
            s = [r.split("\t")[0] for r in t]
            #n = (set(species) - set(s)).union(set(s) - set(species))
            n = len(set(species) - set(s))
            print(n)
            print(len(set(s)))
            #print("Difference between prot and TransPi: ",n)
    return species
#----------------------------------------------------------
def get_busco_genes():
    print("activated get_busco_genes")
    return None
#----------------------------------------------------------
def get_busco_functions():
    print("activated get_busco_functions")
    return None
#----------------------------------------------------------
#contain the various selecatble groups
group_options=[
    {"label": "None", "value": "None"},
    {"label": "All", "value": "All"},
    {"label": "Annelida-Polychaeta", "value": "Platynereis_dumerilii"},
    {"label": "Arthropoda-Branchiopoda", "value": "Daphnia_pulex"},
    {"label": "Choanozoa-Choanoflagellatea", "value": "Acanthoeca_spectabilis, Helgoeca_nana, Salpingoeca_infusionum"},
    {"label": "Chordata-Leptocardii", "value": "Branchiostoma_floridae"},
    {"label": "Chordata-Teleostei", "value": "Danio_rerio"},
    {"label": "Cnidaria-Anthozoa", "value": "Actinia_tenebrosa, Anemonia_sulcata, Anemonia_viridis, Anthopleura_dowii, Anthopleura_elegantissima, Aulactinia_veratra, Calliactis_polypus, Condylactis_gigantea, Edwardsiella_carnea, Entacmaea_quadricolor, Heteractis_crispa, Megalactis_griffithsi, Nematostella_vectensis, Stichodactyla_haddoni, Stichodactyla_helianthus, Antipathes_caribbeana, Plumapathes_pennacea, Corynactis_australis, Rhodactis_indosinensis, Alcyonium_palmatum, Clavularia_sp, Dendronephthya_gigantea, Eunicea_calyculata, Eunicella_cavolini, Gorgonia_ventalina, Muricea_laxa, Phenganax_sp, Sarcothelia_edmonsoni, Sinularia_cruciata, Tubipora_musica, Xenia_sp, Acropora_aculeus, Acropora_cervicornis, Acropora_digitifera, Acropora_millepora, Acropora_tenuis, Agaricia_lamarcki, Alveopora_japonica, Coelastrea_aspera, Ctenactis_echinata, Cyphastrea_serailia, Dendrophyllia_sp, Dipsastraea_rotumana, Favites_acuticollis, Fungia_fungites, Galaxea_astreata, Goniastrea_retiformis, Goniopora_columna, Lobactis_scutaria, Montastraea_cavernosa, Montipora_aequituberculata, Montipora_capitata, Montipora_digitata, Plesiastrea_versipora, Pocillopora_damicornis, Porites_astreoides, Porites_australiensis, Porites_lobata, Porites_lutea, Pseudodiploria_strigosa, Seriatopora_hystrix, Siderastrea_siderea, Tubastraea_coccinea, Corallium_rubrum, Heliopora_coerulea, Palythoa_caribaeorum, Palythoa_variabilis, Protopalythoa_variabilis"},
    {"label": "Cnidaria-Cubozoa", "value": "Copula_sivickisi, Tripedalia_cystophora, Chironex_fleckeri"},
    {"label": "Cnidaria-Hydrozoa", "value": "Hydractinia_symbiolongicarpus, Hydra_oligactis, Hydra_viridissima, Hydra_vulgaris, Millepora_alcicornis, Turritopsis_sp, Liriope_tetraphylla, Aegina_citrea, Apolemia_lanosa, Bargmannia_amoena, Bargmannia_elongata, Bargmannia_lata, Chelophyes_appendiculata, Chuniphyes_multidentata, Craseoa_lathetica, Desmophyes_sp, Erenna_richardi, Forskalia_asymmetrica, Hippopodius_hippopus, Lilyopsis_fluoracantha, Lychnagalma_utricularia, Marrus_claudanielis, Nanomia_bijuga, Physalia_physalis, Resomia_ornicephala, Rhizophysa_filiformis, Stephalia_dilata, Stephalia_sp"},
    {"label": "Cnidaria-Scyphozoa", "value": "Atolla_vanhoeffeni, Nemopilema_nomurai, Stomolophus_meleagris, Aurelia_aurita, Chrysaora_fuscescens, Cyanea_capillata, Cyanea_nozakii, Pelagia_noctiluca"},
    {"label": "Cnidaria-Staurozoa", "value": "Calvadosia_campanulata, Calvadosia_cruxmelitensis, Craterolophus_convolvulus, Haliclystus_auricula"},
    {"label": "Ctenophora-Nuda", "value": "Beroe_abyssicola, Beroe_forskalii, Beroe_ovata"},
    {"label": "Ctenophora-Tentaculata", "value": "Cestum_veneris, Velamen_paralellum, Aulacoctena_acuminata, Bathyctena_chuni, Charistephane_fugiens, Dryodora_glandiformis, Euplokamis_dunlapae, Haeckelia_beehleri, Haeckelia_rubra, Hormiphora_californensis, Lampea_lactea, Lampea_sp, Bathocyroe_fosteri, Bolinopsis_microptera, Deiopea_kaloktenota, Kiyohimea_sp_WRF2015, Lampocteis_cruentiventer, Leucothea_pulchra, Lobata_sp_VWRF2014, Ocyropsis_maculata, Thalassocalyce_inconstans"},
    {"label": "Ctenophora-nan", "value": "Ctenophora_sp_BWRF2014, Ctenophora_sp_CWRF2014, Ctenophora_sp_KWRF2015, Ctenophora_sp_L1WRF2015, Ctenophora_sp_L2WRF2015, Ctenophora_sp_MWRF2015, Ctenophora_sp_N1WRF2014, Ctenophora_sp_N2WRF2014, Ctenophora_sp_PWRF2015, Ctenophora_sp_TWRF2014, Ctenophora_sp_WWRF2014, Ctenophora_sp_XWRF2015"},
    {"label": "Echinodermata-Crinoidea", "value": "Oligometra_serripinna"},
    {"label": "Echinodermata-Echinoidea", "value": "Strongylocentrotus_purpuratus, Eucidaris_tribuloides"},
    {"label": "Hemichordata-Enteropneusta", "value": "Ptychodera_flava"},
    {"label": "Nemertea-Palaeonemertea", "value": "Tubulanus_polymorphus"},
    {"label": "Placozoa-Uniplacotomia", "value": "Hoilungia_hongkongensis, Trichoplax_adherens"},
    {"label": "Porifera-Calcarea", "value": "Leuconia_nivea, Clathrina_coriacea, Leucetta_chagosensis, Grantia_compresa, Sycon_cyliatum, Sycon_ciliatum, Sycon_coactum, Janusya_sp"},
    {"label": "Porifera-Demospongiae", "value": "Cymbastella_concentrica, Halisarca_dujardinii, Chondrosia_reniformis, Cliona_varians, Dendrilla_antarctica, Dysidea_avara, Lendenfeldia_chondrodes, Pleraplysilla_spinifera, Sarcotragus_fasciculatus, Spongia_officinalis, Vaceletia_crypta, Amphimedon_queenslandica, Haliclona_amboinensis, Haliclona_tubifera, Neopetrosia_compacta, Petrosia_ficiformis, Xestospongia_testudinaria, Crella_elegans, Latrunculia_apicalis, Mycale_cecilia, Mycale_phylophylla, Tedania_anhelans, Baikalospongia_bacillifera, Ephydatia_muelleri, Lubomirskia_abietina, Lubomirskia_baikalensis, Spongilla_lacustris, Halichondria_panicea, Pseudospongosorites_suberitoides, Tethya_wilhelma, Cinachyrella_alloclada, Geodia_atlantica, Geodia_hentscheli, Geodia_macandrewii, Geodia_phlegraei, Aplysina_aerophoba, Scopalina_sp, Isodyctia_sp, Poecilosclerida_sp"},
    {"label": "Porifera-Hexactinellida", "value": "Amphidiscella_abyssalis, Aulocalyx_serialis, Bolosoma_cyanae, Caulophacus_discohexaster, Chaunoplectella_NIWA126325, Corbitella_NIWA126123, Regadrella_okinoseana, Rossellidae_NIWA126310, Saccocalyx_tetractinus, Trychella_NIWA126306, Walteria_leuckarti, Eurete_NIWA126276, Farrea_occa, Farrea_similaris"},
    {"label": "Porifera-Homoscleromorpha", "value": "Corticium_candelabrum, Oscarella_lobularis, Oscarella_pearsei, Plakina_jani"},
    {"label": "Priapulida-nan", "value": "Priapulus_caudatus"},
    {"label": "Xenacoelomorpha-nan", "value": "Symsagittifera_roscoffensis, Xenoturbella_bocki"},
    {"label": "nan-Filasterea", "value": "Capsaspora_owczarzaki"},
    {"label": "nan-Ichthyosporea", "value": "Amoebidium_parasiticum, Abeoforma_whisleri, Ichthyosporea_XGB-2017a"},
]
#----------------------------------------------------------
