""" este modulo se emplea para emplear variables globales """

db_conectado = False
regex_numero = "[0-9]"
image_64_encode = ""
var1 = False
var2 = False
global contador_vor_par_2
contador_vor_par_2 = 0
global db_table_aep
global archivos_aux
db_table_aep = False
analizar_doc = False

aeropuertos = (
    "AEP",
    "BAR",
    "BCA",
    "CAT",
    "CBA",
    "CHP",
    "CRR",
    "CRV",
    "DIL",
    "DOZ",
    "DRY",
    "ECA",
    "ERE",
    "ESQ",
    "EZE RWY 11 29",  # 2-1-23
    "EZE RWY 17 35",  # 2-1-23
    "EZE VOR",  # 2-1-23
    "FDO",
    "FSA",
    "GAL",
    "GBE",
    "GNR",
    "GPI",
    "GRA",
    "GUA",
    "IGU",
    "JUA",
    "JUJ",
    "LAR",
    "LYE",
    "MDP",
    "MJZ",
    "MLG",
    "NEU",
    "NIN",
    "OEL",
    "OSA",
    "PAL",
    "PAR",
    "POS",
    "PTA",
    "ROS",
    "RTA",
    "RYD",
    "SAL",
    "SDE",
    "SIS",
    "SJU",
    "SNT",
    "SRA",
    "SVO",
    "TRC",
    "TRE",
    "TRH",
    "TUC",
    "UIS",
    "USH",
    "VIE",
)

regionales = (
    "EZE",
    "EZE",
    "EZE",
    "CBA",
    "CBA",
    "EZE",
    "SIS",
    "CRV",
    "EZE",
    "DOZ",
    "CRV",
    "CRV",
    "CBA",
    "CRV",
    "EZE",
    "EZE",
    "EZE",
    "EZE",
    "SIS",
    "CRV",
    "EZE",
    "EZE",
    "EZE",
    "CRV",
    "EZE",
    "SIS",
    "DOZ",
    "CBA",
    "CBA",
    "EZE",
    "EZE",
    "CBA",
    "DOZ",
    "EZE",
    "EZE",
    "EZE",
    "EZE",
    "EZE",
    "EZE",
    "SIS",
    "EZE",
    "EZE",
    "SIS",
    "DOZ",
    "CBA",
    "CBA",
    "SIS",
    "CRV",
    "EZE",
    "DOZ",
    "EZE",
    "CBA",
    "CRV",
    "CBA",
    "CBA",
    "DOZ",
    "CRV",
    "CRV",
)


