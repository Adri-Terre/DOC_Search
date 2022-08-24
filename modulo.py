from tkinter import *
import sys
from module_base_de_datos import connection_db
import itertools
import csv
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *

# from PIL import ImageTk, Image
# import base64
from fpdf import FPDF

import os


class Doc_input:
    nuevoId = itertools.count()

    def __init__(self, airport, system, files, year, fir):
        self.codigo = next(self.nuevoId)
        self.airport = airport
        self.system = system
        self.files = files
        self.year = year
        self.fir = fir


class Registros:  # (Patr_Obs):
    def __init__(self):
        self.doc_search = []

    def cargar_doc(self, airport, system, files, year, fir):

        """ esta funcion carga un contacto en la base de datos """

        from module_base_de_datos import operacion_db

        # ------------AQUI CARGA LA BASE DE DATOS----------------
        # if askyesno("Consulta", "¿Desea dar de alta el contacto?"):
        a = len(files)
        n = 0
        while n < a:
            sql = "INSERT INTO doc_airport (AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
            val = [airport, system, files[n], year, fir]
            operacion_db(sql, val)
            # showinfo("OK", "Operación exitosa")
            doc_input = Doc_input(airport, system, files, year, fir)
            self.doc_search.append(doc_input)
            n += 1
            # self.notificar()

    """
    def cargar_sitios(self, airport, fir):

        #esta funcion carga un contacto en la base de datos
        import module_variable as mod_var

        from module_base_de_datos import operacion_db

        # ------------AQUI CARGA LA BASE DE DATOS DE LA TABLA AEP_TABLE CON LOS AEROPUERTOS Y SUS FIR----------------

        a = len(airport)
        n = 0
        while n < a:
            sql = "INSERT INTO aep_table (AIRPORT,FIR) VALUES(%s,%s)"
            val = [airport[n], fir[n]]
            operacion_db(sql, val)
            # showinfo("OK", "Operación exitosa")
            aep_input = Aep_input(airport, fir)
            self.doc_search.append(aep_input)
            n += 1
            # self.notificar()
        mod_var.db_table_aep = True
    """

    def cargar_csv(self, id, airport, system, files, year, fir):

        """ esta funcion carga la tabla en el .csv al exportar """

        registers = Doc_input(airport, system, files, year, fir)
        self.doc_search.append(registers)

    def separar_por_sitio(self):

        """ Esta funcion se utiliza tanto para buscar todos los contactos en la agenda, como así también uno específico """

        from module_base_de_datos import operacion_db_buscar
        from module_base_de_datos import operacion_db
        import module_variable as mod_var

        mod_var.encontrado = 0
        mod_var.no_encontrado = 0
        mod_var.total_encontrados = 0
        sql = "SELECT *from doc_airport"
        resultado = operacion_db_buscar(sql)

        for informacion in resultado:

            if informacion[5] == "EZE":

                sql = "INSERT INTO fir_eze(AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
                val = [
                    informacion[1],
                    informacion[2],
                    informacion[3],
                    informacion[4],
                    informacion[5],
                ]
                operacion_db(sql, val)
                # showinfo("OK", "Operación exitosa")
                # doc_input = Doc_input(airport, system, files, year, fir)
                # self.doc_search.append(doc_input)
                # n += 5
            elif informacion[5] == "SIS":
                sql = "INSERT INTO fir_sis(AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
                val = [
                    informacion[1],
                    informacion[2],
                    informacion[3],
                    informacion[4],
                    informacion[5],
                ]
                operacion_db(sql, val)

            elif informacion[5] == "CBA":
                sql = "INSERT INTO fir_cba(AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
                val = [
                    informacion[1],
                    informacion[2],
                    informacion[3],
                    informacion[4],
                    informacion[5],
                ]
                operacion_db(sql, val)

            elif informacion[5] == "CRV":
                sql = "INSERT INTO fir_crv(AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
                val = [
                    informacion[1],
                    informacion[2],
                    informacion[3],
                    informacion[4],
                    informacion[5],
                ]
                operacion_db(sql, val)

            elif informacion[n] == "DOZ":
                sql = "INSERT INTO fir_doz(AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
                val = [
                    informacion[1],
                    informacion[2],
                    informacion[3],
                    informacion[4],
                    informacion[5],
                ]
                operacion_db(sql, val)

    def analizar_por_sitio(self, check_sitio):

        """ Esta uncion se utiliza tanto para buscar todos los contactos en la agenda, como así también uno específico
        
        from module_base_de_datos import operacion_db_buscar
        from module_base_de_datos import operacion_db
        import module_variable as mod_var

        mod_var.encontrado = 0
        mod_var.no_encontrado = 0
        mod_var.total_encontrados = 0
        sql = "SELECT *from doc_airport"
        resultado = operacion_db_buscar(sql)

        for informacion in resultado:

            if informacion[5] == "EZE":

                sql = "INSERT INTO fir_eze(AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
                val = [
                    informacion[1],
                    informacion[2],
                    informacion[3],
                    informacion[4],
                    informacion[5],
                ]
                operacion_db(sql, val)
                # showinfo("OK", "Operación exitosa")
                # doc_input = Doc_input(airport, system, files, year, fir)
                # self.doc_search.append(doc_input)
                # n += 5
        """

    def grabar(self):

        """ esta funcion se emplea para exportar la agenda a .csv"""

        with open("Archivo-CSV.csv", "w") as fichero:
            escribir = csv.writer(fichero)
            escribir.writerow(("ID", "airport", "system", "files", "year", "fir"))
            n = 0
            for registers in self.doc_search:
                n += 1
                escribir.writerow(
                    (
                        registers.codigo,
                        registers.airport,
                        registers.files[n - 1],
                        registers.year,
                        registers.fir,
                    )
                )

        fichero.close()


registro = Registros()
# observador_a = ConcreteObserverA(agenda)


def limpiar():

    """ funcion que limpia los campos en la pantalla principal """

    from_controller_limpiar = True

    return from_controller_limpiar


def clear_window():

    """ esta funcion limpia la pantalla del menú editar """

    from_controller_limpiar_editar = True

    return from_controller_limpiar_editar


def foto_perfil_alta():

    """ Esta funcion carga y asocia una foto de perfil con el nuevo contacto. Se emplea "base64" para codificar la imagen """

    import module_variable as mod_var

    file_path = (
        askopenfilename()
    )  # aqui se abre el explorador de archivos para seleccionar una imagen y guarda la seleccion en la variable """

    image = open(file_path, "rb")  # abre el archivo en modo lectura
    image_read = image.read()
    mod_var.image_64_encode = base64.encodebytes(image_read)


def foto_perfil_decode():

    """ Esta funcion decodifica una foto de perfil previamente codificada en "base64" asociada al contacto buscado """

    import module_variable as mod_var

    global w8
    global w9

    image_64_decode = base64.decodebytes(mod_var.image_64_encode)
    image_result = open("foto_perfil.jpg", "wb")
    image_result.write(
        image_64_decode
    )  # crea una imagen editable y escribe el resultado decodificado
    image_result.flush()

    imagenL = Image.open("foto_perfil.jpg")
    miniatura = (160, 120)
    imagenL.thumbnail(miniatura)

    imagenL.save("img_miniatura.jpg")
    img = ImageTk.PhotoImage(file="img_miniatura.jpg")

    """ Guarda la imagen obtenida con el formato JPEG """

    load = Image.open("img_miniatura.jpg")
    mod_var.render = ImageTk.PhotoImage(load)


def exportar():

    """ esta funcion exporta los datos de la agenda en .pdf .csv .xml y .json"""

    from module_base_de_datos import operacion_db_buscar
    import xml.etree.ElementTree as ET

    global datosstr
    datosstr = ""

    resultado = ""

    if os.path.exists("Archivo-CSV.csv"):
        os.remove("Archivo-CSV.csv")

    fichero = open("Archivo-CSV.csv", "w")
    escribir = csv.writer(fichero)
    escribir.writerow(("ID", "airport", "system", "files", "year", "fir"))

    sql = "SELECT *FROM doc_airport"
    resultado = operacion_db_buscar(sql)
    y = 0

    a = len(resultado)
    if a != 0:

        for x in resultado:
            res = resultado[y]
            escribir.writerow((res[0], res[1], res[2], res[3], res[4], res[5],))

            y = y + 1

        fichero.flush()
        fichero.close()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=9)
        archivo = open("Archivo-CSV.csv", "r")

        for z in archivo:
            pdf.cell(250, 5, txt=z, ln=1, align="c")
        pdf.output("Archivo-PDF.pdf")

        showinfo("Exportar", "Archivos exportados en CSV, PDF")  # , XML Y JSON")

    else:
        showinfo("Exportar", "No hay registros en la base de datos")
