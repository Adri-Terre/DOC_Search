# global func_modificar
# global func_eliminar
# global no_encontrado
# global total_encontrados
# global encontrado
# global actualizar_imagen
# global codigo
# global my_cursor
# global image_64_encode
# global render
# global var1, var2
# global var_eliminar
# global ventana_open
# global ventana_open_editar
# global dato_ingresado
# global contacto_encontrado

# dato_ingresado = ""
# ventana_open_editar = False
# codigo = 0
# ventana_open = False
# func_modificar = False
# func_eliminar = False
# actualizar_imagen = False
db_conectado = False

# buscartodos_boton = True
# contacto_search = []
# contacto_encontrado = []
# image_64_encode = ""
# var1 = False
# var2 = False
global db_table_aep
global archivos_aux
db_table_aep = False


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
    "EZE",
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
    "SIS",
    "CRV",
    "EZE",
    "EZE",
    "EZE",
    "CRV",
    "EZE",
    "EZE",
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
    "DOZ",
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

""" este modulo se emplea para emplear variables globales """
