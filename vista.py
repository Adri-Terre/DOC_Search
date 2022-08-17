from tkinter import *
from tkinter.messagebox import *
import sys
from module_base_de_datos import connection_db
import module_variable as mod_var
import controller
from tkinter import ttk  # para la barra de progreso


def autor():

    """ esta funcion crea una pantalla donde se muestran los integrantes del proyecto"""

    win = Toplevel()
    win.title("Autor")
    win.geometry("300x100")
    label_autor = Label(win, text="ING. TERRENI ADRIAN HORACIO\n",)

    label_autor.place(x=60, y=20)


def insertar_documentacion():

    """ esta funcion, a traves del controller, inserta la documentacion a analizar"""
    controller.control_buscardocumentacion()


def buscartodos():
    controller.control_separartodos()


def limpiar():
    controller.control_limpiar()


def call_exportar():

    """ esta funcion, a traves del controller, exporta los datos de la agenda en .pdf, .csv, xml, json """

    controller.control_exportar()


# ----------------------------SECCIÓN GRÁFICA DE LA AGENDA------------------------

master = Tk()

w1 = Label(master, text="INGRESE AÑO")
w1.place(x=10, y=10)

anio_input = Entry(master)
anio_input.configure(width=20)
anio_input.place(x=10, y=30)
anio_input.focus_set()

""" cuadro de texto donde van a aparecer los datos de contacto """

datos_carpetas = Text(master)
datos_carpetas.place(x=380, y=40, width=200, height=200)

""" Aquí se crea la pantalla principal """

master.geometry("620x300")
master.title("DOC Search")
menu = Menu(master)
master.config(menu=menu)
filemenu = Menu(menu)
# --------Archivo--------------------------
menu.add_cascade(label="Archivo", menu=filemenu)
filemenu.add_command(label="Exportar", command=call_exportar)
# filemenu.add_separator()
# filemenu.add_command(label="Cerrar", command=master.quit)

# ---------Menu----------------------------
Menu_x = Menu(menu)
menu.add_cascade(label="Menu", menu=Menu_x)
# Menu_x.add_command(label="Alta", command=alta)
# Menu_x.add_separator()
# Menu_x.add_command(label="Editar", command=editar)

# ---------Acerca de-----------------------
acerca_de = Menu(menu)
menu.add_cascade(label="Acerca de", menu=acerca_de)
acerca_de.add_command(label="Autor", command=autor)
# acerca_de.add_separator()
# acerca_de.add_command(label="Curso", command=curso)

# --------------BOTON-----------------------------------------------------------------
Button(
    master,
    text="Seleccionar documentación",
    width=22,
    command=insertar_documentacion,
    anchor=CENTER,
).place(x=150, y=28)
# -----------------------------------------------------------------------------------
Button(master, text="Limpiar pantalla", width=15, command=limpiar, anchor=CENTER).place(
    x=420, y=250
)
# -----------------------------------------------------------------------------------
Button(master, text="Buscar todos", width=20, command=buscartodos, anchor=CENTER).place(
    x=5, y=100
)

w = Label(master, text="EXTRACTO CARPETAS")
w.place(x=420, y=10)

# label conexion base de datos

# a = controller.control_cargar_sitios()
db_conectado = connection_db()

if mod_var.db_table_aep == False:
    controller.control_cargar_sitios()


if db_conectado == True:
    w2 = Label(master, text="Database 1 Online", foreground="green")
    w2.place(x=6, y=260)
else:
    w3 = Label(master, text="Database 1 Offline", foreground="red")
    w3.place(x=6, y=260)


if mod_var.db_table_aep == True:
    w4 = Label(master, text="Database 2 Online", foreground="green")
    w4.place(x=150, y=260)
else:
    w5 = Label(master, text="Database 2 Offline", foreground="red")
    w5.place(x=150, y=260)


progressbar = ttk.Progressbar(length=600)
# progressbar = ttk.Progressbar(root,variable=progress_var, maximun = MAX, length=600)
progressbar.place(x=9, y=280, height=15)

master.mainloop()
