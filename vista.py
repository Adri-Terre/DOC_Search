from msilib.schema import ComboBox
from tkinter import *
from tkinter.messagebox import *

# import sys
# from typing import Container
from module_base_de_datos import connection_db
import module_variable as mod_var
import controller
from tkinter import ttk  # para la barra de progreso


global w9, w10, w11, w13


def descargar():

    """esta funcion crea una pantalla donde muestra las opciones para descargar"""

    global win_descargar

    win_descargar = Toplevel()
    win_descargar.title("Descargar")
    win_descargar.geometry("300x100")

    mod_var.var1 = BooleanVar()
    mod_var.var2 = BooleanVar()
    # label_autor = Label(win, text="ING. TERRENI ADRIAN HORACIO\n\nv1.0 - AÑO: 2022")
    Checkbutton(
        win_descargar,
        text="Archivos existentes",
        onvalue=1,
        offvalue=0,
        variable=mod_var.var1,
    ).place(x=80, y=40)
    Checkbutton(
        win_descargar,
        text="Archivos pendientes",
        onvalue=1,
        offvalue=0,
        variable=mod_var.var2,
    ).place(x=80, y=10)

    Button(
        win_descargar,
        text="Aplicar",
        width=15,
        command=controller.aplicar_descargar,
        anchor=CENTER,
    ).place(x=90, y=70)
    # label_autor.place(x=60, y=20)


def autor():

    """esta funcion crea una pantalla donde se muestra el autor del proyecto"""

    win = Toplevel()
    win.title("Autor")
    win.geometry("300x100")
    label_autor = Label(win, text="ING. TERRENI ADRIAN HORACIO\n\nv1.0 - AÑO: 2022")
    label_autor.place(x=60, y=20)


def insertar_documentacion():

    """esta funcion, a traves del controller, inserta la documentacion a analizar"""

    controller.control_buscardocumentacion()


def analizar():
    controller.control_analizar_por_sitio()


def reset():
    controller.control_reset()


def call_exportar_1():

    """esta funcion, a traves del controller, exporta los datos de la agenda en .pdf, .csv"""

    controller.control_exportar("doc_airport")


def call_exportar_2():

    """esta funcion, a traves del controller, exporta los datos de la agenda en .pdf, .csv"""
    combo_seleccionado = combo_fir.get()
    combo_seleccionado = combo_seleccionado + "_pendientes"
    controller.control_exportar(combo_seleccionado)


# ----------------------------SECCIÓN GRÁFICA DE LA APP------------------------

master = Tk()

periodo = LabelFrame(master, text="Período", bd=2)
periodo.place(x=10, y=70, width=200, height=80)
w4 = Label(master, text="Desde")
w4.place(x=30, y=90)

mes_desde_input = Entry(master)
mes_desde_input.configure(width=10)
mes_desde_input.place(x=30, y=110)
mes_desde_input.focus_set()

w5 = Label(master, text="Hasta")
w5.place(x=120, y=90)

mes_hasta_input = Entry(master)
mes_hasta_input.configure(width=10)
mes_hasta_input.place(x=120, y=110)
mes_hasta_input.focus_set()

anio_frame = LabelFrame(master, text="Ingrese año", bd=2)
anio_frame.place(x=10, y=5, width=200, height=60)

anio_input = Entry(master)
anio_input.configure(width=15)
anio_input.place(x=30, y=30)
anio_input.focus_set()

""" Aquí se crea la pantalla principal """

master.geometry("620x300")
master.title("DOC Search")
menu = Menu(master)
master.config(menu=menu)
filemenu = Menu(menu)
# --------Archivo--------------------------
menu.add_cascade(label="Archivo", menu=filemenu)
filemenu.add_command(label="Exportar existentes", command=call_exportar_1)
filemenu.add_separator()
filemenu.add_command(label="Exportar pendientes", command=call_exportar_2)

# ---------Acerca de-----------------------
acerca_de = Menu(menu)
menu.add_cascade(label="Acerca de", menu=acerca_de)
acerca_de.add_command(label="Autor", command=autor)


# --------------BOTON-----------------------------------------------------------------
Button(
    master,
    text="Seleccionar documentación",
    width=22,
    command=insertar_documentacion,
    anchor=CENTER,
).place(x=220, y=28)
# -----------------------------------------------------------------------------------
Button(master, text="Reset", width=15, command=reset, anchor=CENTER).place(x=495, y=250)
# -----------------------------------------------------------------------------------
Button(master, text="Descargar", width=15, command=descargar, anchor=CENTER).place(
    x=370, y=250
)
# -----------------------------------------------------------------------------------

fir_frame = LabelFrame(master, text="Fir", bd=2)
fir_frame.place(x=10, y=160, width=200, height=60)

Button(master, text="Analizar", width=22, command=analizar, anchor=CENTER).place(
    x=220, y=175
)

# Checkbutton(master, text="Incluye tareas semanales").place(x=25, y=210)

combo_fir = ttk.Combobox(
    state="readonly", values=["fir_eze", "fir_cba", "fir_crv", "fir_sis", "fir_doz"]
)
combo_fir.place(x=30, y=180)

db_conectado = connection_db()

if mod_var.db_table_aep == False:
    controller.control_cargar_sitios()


if db_conectado == True:
    w2 = Label(master, text="Database Online", foreground="blue")
    w2.place(x=6, y=260)
else:
    w3 = Label(master, text="Database Offline", foreground="red")
    w3.place(x=6, y=260)

"""
progressbar = ttk.Progressbar(length=600)
# progressbar = ttk.Progressbar(root,variable=progress_var, maximun = MAX, length=600)
progressbar.place(x=9, y=280, height=15)
"""
w6 = Label(master, text="Archivos Descargados: ", foreground="black")
w6.place(x=400, y=30)

w7 = Label(master, text="Archivos Ordenados: ", foreground="black")
w7.place(x=400, y=60)

w8 = Label(master, text="Archivos Analizados: ", foreground="black")
w8.place(x=400, y=90)

w9 = Label(master, text="-", foreground="red")
w9.place(x=530, y=30)

w10 = Label(master, text="-", foreground="red")
w10.place(x=530, y=60)

w11 = Label(master, text="-", foreground="red")
w11.place(x=530, y=90)

w12 = Label(master, text="Reporte Creado: ", foreground="black")
w12.place(x=400, y=120)

w13 = Label(master, text="-", foreground="red")
w13.place(x=530, y=120)

master.mainloop()
