import vista
from tkinter.messagebox import *
from tkinter import *
from os import walk
from tkinter import filedialog
import os.path
import module_variable
from tkinter import ttk


def control_buscardocumentacion(ruta="."):
    import modulo as mod
    import module_variable as mod_var

    dir, subdirs, archivos = next(walk(ruta))

    anio_seleccionado = vista.anio_input.get()
    if anio_seleccionado != "":
        folder_selected = filedialog.askdirectory()

        dir, subdirs, archivos = next(walk(folder_selected))

        y = 0
        for x in subdirs:

            carpeta_sitio = subdirs[y]

            carpeta = folder_selected + "/" + carpeta_sitio + "/" + anio_seleccionado

            if os.path.exists(carpeta):
                dir, subdirs, archivos = next(walk(carpeta))

                vista.datos_carpetas.insert(INSERT, carpeta_sitio)
                vista.datos_carpetas.insert(INSERT, " ")

                if carpeta != "":

                    z = 0
                    n = 0
                    i = 0
                    print(carpeta_sitio)
                    for x in subdirs:
                        subcarpeta = subdirs[z]
                        carpeta2 = (
                            folder_selected
                            + "/"
                            + carpeta_sitio
                            + "/"
                            + anio_seleccionado
                            + "/"
                            + subcarpeta
                        )
                        dir, subdirs, archivos = next(walk(carpeta2))
                        # print("Actual: ", dir)
                        print(subcarpeta)
                        # vista.datos_carpetas.text = subcarpeta
                        vista.datos_carpetas.insert(INSERT, subcarpeta)
                        vista.datos_carpetas.insert(INSERT, " ")
                        print("Archivos: ", archivos)
                        archivos_aux = archivos
                        dir, subdirs, archivos = next(walk(carpeta))
                        z = z + 1

                        while n < len(mod_var.aeropuertos):
                            if carpeta_sitio == mod_var.aeropuertos[n]:
                                fir = mod_var.regionales[n]
                            n = n + 1

                        # aca cargaría en la base de datos (carpeta_sitio, subcarpeta,archivos)
                        mod.registro.cargar_doc(
                            carpeta_sitio,
                            subcarpeta,
                            archivos_aux,
                            anio_seleccionado,
                            fir,
                        )
                        i = i + 0.6
                        # vista.progressbar.step(i)
                    # vista.progressbar.step(i)
                    # root.update_idletasks()
                    # vista.progressbar.step(i)
                dir, subdirs, archivos = next(walk(folder_selected))
                vista.datos_carpetas.insert(INSERT, "Files OK\n")
                y = y + 1

            else:
                vista.datos_carpetas.insert(INSERT, carpeta_sitio + " ")
                vista.datos_carpetas.insert(INSERT, "No Files\n")

        vista.progressbar.step(50)

        mod.registro.separar_por_sitio()  # aca llama a la funcion que separa la documentación por region

        vista.progressbar.step(99)

    else:
        showinfo(
            "AÑO INGRESADO",
            "Ingrese año del periodo a analizar",
        )
    return archivos


def control_cargar_sitios():
    import modulo as mod

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

    # mod.registro.cargar_sitios(aeropuertos, regionales)


def control_exportar():

    """esta funcion se emplea para exportar la agenda en formatos csv, pdf, json, xml"""
    import modulo as mod

    mod.exportar()


def control_limpiar():
    vista.datos_carpetas.delete(1.0, END)
    vista.anio_input.delete(0, END)


def control_analizar_por_sitio():

    import modulo as mod
    from vista import combo_fir

    combo_seleccionado = combo_fir.get()

    """esta funcion busca un todo lo existente en las carpetas a analizar, y muestra en la pantalla cantidades y labels"""
    if combo_seleccionado != "":
        mod.registro.analizar_por_sitio()
    else:
        showinfo(
            "FIR no seleccionada",
            "Seleccione la FIR a analizar",
        )
