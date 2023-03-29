# auto-py-to-exe

import vista
from tkinter.messagebox import *
from tkinter import *
from os import walk
from tkinter import filedialog
import os.path


def control_buscardocumentacion(ruta="."):

    """esta funcion descarga y va analizando toda la información del sharepoint"""

    import modulo as mod
    import module_variable as mod_var
    import re

    #from alive_progress import alive_bar
    from time import sleep

    mod_var.contador_vor_par_2 = 0
    cant_archivos = 0
    re_match = None
    dir, subdirs, archivos = next(walk(ruta))
    max = 600
    p = 0
    anio_seleccionado = vista.anio_input.get()

    if re.match(mod_var.regex_numero, anio_seleccionado):
        re_match = True
    else:
        re_match = False

    if (anio_seleccionado != "") & (re_match == True):
        folder_selected = filedialog.askdirectory()

        dir, subdirs, archivos = next(walk(folder_selected))

        y = 0
        p_len = int(len(folder_selected))
        p = max / p_len

        for x in subdirs:
            print(subdirs)
            carpeta_sitio = subdirs[y]
            carpeta = folder_selected + "/" + carpeta_sitio + "/" + anio_seleccionado
            p_len = int(len(carpeta))
            if os.path.exists(carpeta):
                dir, subdirs, archivos = next(walk(carpeta))

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

                        print(subcarpeta)

                        print("Archivos: ", archivos)
                        cant_archivos = cant_archivos + len(archivos)

                        archivos_aux = archivos
                        if archivos_aux == []:
                            crear_archivo_pend = (
                                anio_seleccionado
                                + str(".01.01 ")
                                + carpeta_sitio
                                + " "
                                + subcarpeta
                                + " "
                                + "INFORMACION PENDIENTE"
                            )
                            archivos_aux.append(crear_archivo_pend)
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
                        p = p + (max / p_len)

                dir, subdirs, archivos = next(walk(folder_selected))

                vista.w9.destroy()
                vista.w9 = Label(vista.master, text=cant_archivos, foreground="green")
                vista.w9.place(x=530, y=30)

                y = y + 1

            else:
                y += 1
                pass

        print("cantidad de archivos descargados: ", cant_archivos)
        mod.registro.separar_por_sitio()  # aca llama a la funcion que separa la documentación por region

        vista.w10.destroy()
        vista.w10 = Label(vista.master, text="OK", foreground="green")
        vista.w10.place(x=530, y=60)

    else:

        if (re_match == False) & (anio_seleccionado != ""):
            showinfo(
                "AÑO INGRESADO",
                "Ingrese solo números",
            )
        else:
            showinfo(
                "AÑO INGRESADO",
                "Ingrese año del periodo a analizar",
            )
    return archivos


def control_exportar(doc_airport):

    """esta funcion se emplea para exportar la agenda en formatos csv, pdf"""

    import modulo as mod

    mod.exportar(doc_airport)


def control_reset():

    """esta funcion se emplea para eliminar las tablas analizadas"""

    from module_base_de_datos import eliminar_tabla_fir

    vista.mes_desde_input.delete(0, END)
    vista.mes_hasta_input.delete(0, END)
    vista.anio_input.delete(0, END)
    vista.combo_fir.delete(0, END)

    text_w11 = vista.w11.cget("text")
    text_w13 = vista.w13.cget("text")

    if text_w11 == "OK":
        vista.w11.destroy()
        vista.w11 = Label(vista.master, text="-", foreground="red")
        vista.w11.place(x=530, y=90)

    if text_w13 == "OK":

        vista.w13.destroy()
        vista.w13 = Label(vista.master, text="-", foreground="red")
        vista.w13.place(x=530, y=90)

    a = eliminar_tabla_fir()
    if a == True:
        showinfo(
            "Mensaje Reset",
            "Base de datos reseteada",
        )


def control_analizar_por_sitio():

    """esta funcion busca un todo lo existente en las carpetas a analizar, y muestra en la pantalla cantidades y labels"""

    import modulo as mod
    from vista import combo_fir, mes_desde_input, mes_hasta_input
    #from alive_progress import alive_bar
    import module_variable as mod_var
    import re

    combo_seleccionado = combo_fir.get()
    anio_seleccionado = vista.anio_input.get()
    periodo_desde = vista.mes_desde_input.get()
    periodo_hasta = vista.mes_hasta_input.get()

    if re.match(mod_var.regex_numero, periodo_desde):
        re_match = True
    else:
        re_match = False
    if re.match(mod_var.regex_numero, periodo_hasta):
        re_match_2 = True
    else:
        re_match_2 = False

    if mod_var.analizar_doc == False:

        mod_var.analizar_doc = True

        if anio_seleccionado != "":
            if combo_seleccionado != "" and periodo_desde != "" and periodo_hasta != "":
                if (re_match & re_match_2) == True:
                    mod.registro.analizar_por_sitio()
                else:
                    showinfo(
                        "Mensaje Período", "El período ingresado deben ser números"
                    )
            else:
                showinfo(
                    "Campos incompletos",
                    "Complete todos los campos",
                )
        else:
            showinfo(
                "AÑO INGRESADO",
                "Ingrese año del periodo a analizar y seleccione la documentación",
            )

    else:
        showinfo("Mensaje Analizar", "La documentación ya ha sido analizada")


def aplicar_descargar():

    """esta funcion descarga los archivos pendientes o todos los archivos existentes"""

    import module_variable as mod_var
    import vista as mod_vista

    if mod_var.var1.get() == True:
        control_exportar("doc_airport")

    if mod_var.var2.get() == True:
        combo_seleccionado = vista.combo_fir.get()
        combo_seleccionado = combo_seleccionado + "_pendientes"
        control_exportar(combo_seleccionado)

    vista.win_descargar.destroy()
