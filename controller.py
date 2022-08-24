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

        mod.registro.separar_por_sitio()

        vista.progressbar.step(99)

    else:
        showinfo(
            "AÑO INGRESADO", "Ingrese año del periodo a analizar",
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


def control_analizar_los_sitios():

    import modulo as mod

    """esta funcion busca un todo lo existente en las carpetas a analizar, y muestra en la pantalla cantidades y labels"""

    # import module_variable as mod_var

    # contacto_a_buscar = vista.e1_input.get()
    # vista.datos_contacto.delete(1.0, END)

    # mod_var.func_modificar = False
    # vista.w8.destroy()
    # mod_var.contacto_search.clear()
    # mod_var.buscartodos_boton = False
    # texto = contacto_a_buscar
    # texto = texto.upper()
    mod.analizar_por_sitio("EZE")

    # if mod_var.no_encontrado == 0:
    #    vista.datos_contacto.insert(INSERT, "---*---*---<>---*---*---\n")
    #    vista.datos_contacto.insert(INSERT, "CONTACTO NO ENCONTRADO\n")
    # else:
    #    n = 0
    #    while n < 6:
    #        mod_var.contacto_search.append(contacto[n])
    #        n += 1

    #    if mod_var.buscartodos_boton == False:
    #        mod_var.image_64_encode = contacto[6]
    #        if mod_var.image_64_encode != b"":
    #            modulo.foto_perfil_decode()
    #    n = 0
    #    x = 0
    #    ready = False
    #    a = len(mod_var.contacto_search)
    #    while n < a:
    #        vista.datos_contacto.insert(
    #            INSERT, "Codigo: {}\n".format(mod_var.contacto_search[n])
    #        )
    #        n += 1
    #        x += 1
    #        vista.datos_contacto.insert(
    #            INSERT, "Nombre: {}\n".format(mod_var.contacto_search[n])
    #        )
    #        n += 1
    #        x += 1
    #        vista.datos_contacto.insert(
    #            INSERT, "Apellido: {}\n".format(mod_var.contacto_search[n])
    #        )
    #        n += 1
    #        x += 1
    #        vista.datos_contacto.insert(
    #            INSERT, "Empresa: {}\n".format(mod_var.contacto_search[n])
    #        )
    #        n += 1
    #        x += 1
    #        vista.datos_contacto.insert(
    #            INSERT, "Email: {}\n".format(mod_var.contacto_search[n])
    #        )
    #        n += 1
    #        x += 1
    #        vista.datos_contacto.insert(
    #            INSERT, "Teléfono: {}\n".format(mod_var.contacto_search[n])
    #        )
    #        n += 1
    #        x += 1
    #        if x == 6:
    #            vista.datos_contacto.insert(INSERT, "---*---*---<>---*---*---\n")
    #        x = 0
    # if (
    #    (mod_var.func_modificar == False)
    #    & (mod_var.no_encontrado == 1)
    #    & (mod_var.image_64_encode != b"")
    #    & (mod_var.encontrado < 2)
    # ):
    #    vista.w8 = Label(vista.master, image=mod_var.render)
    #    vista.w8.image = mod_var.render
    #    vista.w8.place(x=180, y=60)
    #    mod_var.contacto_search.clear()
    # else:
    #    vista.w8 = Label(vista.master, text="> FOTO DE PERFIL: NO DISPONIBLE <")
    #    vista.w8.place(x=165, y=100)
