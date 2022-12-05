from tkinter import *

import sys
from module_base_de_datos import connection_db
import itertools
import csv
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *
import vista

# from PIL import ImageTk, Image
# import base64
from fpdf import FPDF

import os
import logging


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

        """esta funcion carga un contacto en la base de datos"""

        from module_base_de_datos import operacion_db

        # ------------AQUI CARGA LA BASE DE DATOS----------------

        a = len(files)
        n = 0
        while n < a:
            sql = "INSERT INTO doc_airport (AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
            val = [airport, system, files[n], year, fir]
            operacion_db(sql, val)
            doc_input = Doc_input(airport, system, files, year, fir)
            self.doc_search.append(doc_input)
            n += 1
            # self.notificar()

    def cargar_csv(self, id, airport, system, files, year, fir):

        """esta funcion carga la tabla en el .csv al exportar"""

        registers = Doc_input(airport, system, files, year, fir)
        self.doc_search.append(registers)

    def separar_por_sitio(self):

        """Esta funcion se utiliza tanto para buscar todos los contactos en la agenda, como así también uno específico"""

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

            elif informacion[5] == "DOZ":
                sql = "INSERT INTO fir_doz(AIRPORT,SYSTEM,FILES,YEAR, FIR)VALUES(%s,%s,%s,%s,%s)"
                val = [
                    informacion[1],
                    informacion[2],
                    informacion[3],
                    informacion[4],
                    informacion[5],
                ]
                operacion_db(sql, val)

    def analizar_por_sitio(self):

        # Esta funcion analiza por fir seleccionada la información existente.
        import re
        from module_base_de_datos import operacion_db_buscar
        from module_base_de_datos import operacion_db
        import module_variable as mod_var
        from vista import combo_fir, mes_desde_input, mes_hasta_input, w11

        global Str_system
        global informacion
        # global informacion_aux
        global mes
        global files_mes
        global aux_mes_anterior
        global aux_airport
        global aux_system
        global array_ils
        global array_li
        global array_vor
        global array_total
        global no_data_mes
        global anio_desde
        global anio_hasta
        global aux_mes_2
        global periodo  # antes periodo
        global check_mes_hasta, check_mes_desde

        global array_rechazados
        # global w11
        no_data_mes = False
        array_rechazados = []
        check_mes_hasta = False
        check_mes_desde = False
        periodo = False
        informacion = ""
        # informacion_aux = ""

        array_ils = ["LH", "ILS PARAMETROS", "DME ILS PARAMETROS"]
        array_vor = [
            "LH",
            "VOR PARAMETROS I",
            "VOR PARAMETROS II",
            "DME VOR PARAMETROS",
        ]
        array_li = ["LH", "LI PARAMETROS"]

        array_total = set(array_ils + array_li + array_vor)

        files_mes = []

        anio_desde = int(mes_desde_input.get())
        anio_hasta = int(mes_hasta_input.get())

        fir_seleccionada = combo_fir.get()
        sql = "SELECT *from " + fir_seleccionada
        resultado = operacion_db_buscar(sql)

        mes_anterior = 0
        for sistema in resultado:
            aux_airport = sistema[1]
            aux_system = sistema[2]
            mes_anterior = sistema[3]
            mes_anterior = mes_anterior[5] + mes_anterior[6]
            aux_mes_anterior = int(mes_anterior)
            break
        for informacion in resultado:

            if (aux_airport != informacion[1]) & (check_mes_hasta == True):

                aux_airport = informacion[1]
                check_mes_hasta = False
                aux_system = informacion[2]
                check_mes_desde = False

            elif (aux_system != informacion[2]) & (check_mes_hasta == True):

                check_mes_hasta = False
                aux_system = informacion[2]
                check_mes_desde = False
            """
            elif (aux_airport == informacion[1]) & (check_mes_hasta == True):

                check_mes_hasta = False
                check_mes_desde = False
                periodo = False
            """
            if (
                (aux_airport == informacion[1])
                & (check_mes_hasta == False)
                & (aux_system == informacion[2])
            ):

                aux_mes_2 = aux_mes_anterior
                file_cadena = informacion[3]
                mes = file_cadena[5] + file_cadena[6]
                # word = file_cadena.find("LH")
                mes_array = int(mes)

                if mes_array >= anio_desde:
                    check_mes_desde = True
                ########### modificación 5-10-22
                while anio_desde < mes_array:  # or (mes_array < anio_hasta):
                    aux_mes_anterior = anio_desde
                    anio_desde += 1
                    no_data_mes = True
                    periodo = self.check_array()
                    if periodo == True:
                        periodo = False
                        break
                    aux_mes_anterior = anio_desde

                if (
                    (informacion[2] == aux_system)
                    & ((aux_mes_anterior) == int(mes))
                    & (periodo == False)
                    & (aux_airport == informacion[1])
                ):
                    # aca
                    """
                    if informacion_aux != "":
                        if (
                            (informacion_aux[2] == aux_system)
                            & ((aux_mes_anterior) == int(mes))
                            & (periodo == False)
                            & (aux_airport == informacion_aux[1])
                        ):

                            files_mes.append(informacion_aux[3])
                            informacion_aux = ""
                    """
                    files_mes.append(informacion[3])

                    aux_mes_anterior = int(mes)

                else:  # una vez cargado todo el mes, analiza la información

                    if (
                        (periodo == False)
                        & (check_mes_hasta == False)
                        & (check_mes_desde == True)
                    ):  #####################
                        periodo = self.check_array()
                        check_mes_desde = False
                    else:
                        periodo = False
                        anio_desde = int(mes_desde_input.get())
                    # break
            else:

                if (aux_mes_anterior <= anio_hasta) & (check_mes_hasta == False):

                    no_data_mes = True
                    periodo = self.check_array()
                    aux_mes_anterior += 1
                    if periodo == False:
                        periodo = self.check_array()
                    else:
                        periodo = False
                        anio_desde = int(mes_desde_input.get())

        if informacion != "":

            if (periodo == False) & (check_mes_hasta == False):
                self.check_array()

            vista.w11.destroy()
            vista.w11 = Label(vista.master, text="OK", foreground="green")
            vista.w11.place(x=530, y=90)

            showinfo("MENSAJE", "Operación exitosa")
            aux_system = ""
            array_system = ""
            informacion = []

            if array_rechazados != "":
                log_rechazado(array_rechazados)
                array_rechazados = []
                showinfo("MENSAJE", "Se ha generado un log con archivos rechazados")
        else:
            showinfo("MENSAJE", "No hay información disponible")

    def check_array(self):

        # esta función compara los documentos con analizados con los arrays preestablecidos
        from vista import mes_desde_input

        global Str_system
        global files_mes
        global aux_system
        global aux_mes_anterior
        global aux_airport

        global aux_system
        global array_ils
        global array_li
        global array_vor
        global array_total
        global anio_hasta, anio_desde
        global aux_mes_2
        global periodo  # antes periodo
        global check_mes_hasta
        global check_mes_desde

        global array_rechazados
        # global informacion_aux

        # array_rechazados = []

        periodo_ok = False
        a = 0
        b = len(files_mes)
        c = 0

        if aux_system == "ILS":
            array_system = array_ils

        elif aux_system == "VOR":
            array_system = array_vor

        elif aux_system == "LI":
            array_system = array_li

        l = 0
        rechazado = False
        while a < b:

            for array_data in array_total:

                word = files_mes[a].find(array_data)
                if word != -1:

                    try:
                        if array_data == "VOR PARAMETROS II":
                            array_system.remove(array_data)
                            rechazado = True
                            break
                        else:
                            command = str(array_data)
                            array_system.remove(command)
                            rechazado = True
                            break
                    except:
                        pass

            if rechazado == False:
                array_rechazados.append(files_mes[a])

            a += 1
        try:
            Str_system = "-".join(array_system)
            self.registrar_pendientes()
        except:
            print(aux_system + " no esta en la lista")
        
        

        if aux_mes_anterior == anio_hasta:
            periodo = True  # False
            aux_airport = informacion[1]
            anio_desde = int(mes_desde_input.get())
            aux_mes_anterior = anio_desde
            check_mes_hasta = True
            check_mes_desde = False
            # informacion_aux = informacion
            # periodo = False
        return periodo

    def registrar_pendientes(self):

        from module_base_de_datos import operacion_db
        from vista import combo_fir, mes_desde_input

        global Str_system
        global informacion
        global mes
        global files_mes
        global aux_mes_anterior
        global aux_airport
        global aux_system
        global array_ils
        global array_li
        global array_vor
        global no_data_mes
        global anio_desde

        # Str_system = "-".join(array_system)
        fir_seleccionada = combo_fir.get()
        if Str_system != "":

            sql = (
                "INSERT INTO "
                + fir_seleccionada
                + "_pendientes(AIRPORT,SYSTEM,MES,OBSERVACIONES,YEAR,FIR)VALUES(%s,%s,%s,%s,%s,%s)"
            )
            val = [
                aux_airport,
                aux_system,
                str(aux_mes_anterior),
                "Falta entregar: " + "" + Str_system,
                informacion[4],
                informacion[5],
            ]
            operacion_db(sql, val)

        files_mes = []
        if no_data_mes == False:

            if informacion[2] != aux_system:
                anio_desde = int(mes_desde_input.get())

            files_mes.append(informacion[3])
            # aux_mes_anterior = int(mes)
            # aux_airport = informacion[1]
            aux_system = informacion[2]

        no_data_mes = False

        array_ils = ["LH", "ILS PARAMETROS", "DME ILS PARAMETROS"]
        array_vor = [
            "LH",
            "VOR PARAMETROS I",
            "VOR PARAMETROS II",
            "DME VOR PARAMETROS",
        ]
        array_li = ["LH", "LI PARAMETROS"]


registro = Registros()


def exportar(file_export):

    """esta funcion exporta los datos de la agenda en .pdf .csv .xml y .json"""
    global w12, w13
    from module_base_de_datos import operacion_db_buscar
    import module_variable as mod_var

    #   import xml.etree.ElementTree as ET
    from datetime import date

    fecha_actual = date.today()

    titulo = False

    global datosstr
    datosstr = ""

    resultado = ""
    table_name = file_export

    if table_name != "_pendientes":
        if table_name == "doc_airport":
            # str(fecha_actual) +
            nombre_tabla_completa = str(fecha_actual) + " Registros_completos.csv"
            nombre_tabla_completa = nombre_tabla_completa.upper()
            if os.path.exists(nombre_tabla_completa):
                os.remove(nombre_tabla_completa)
            fichero = open(nombre_tabla_completa, "w")

        else:

            if os.path.exists(str(fecha_actual) + " " + table_name.upper() + ".csv"):
                os.remove(str(fecha_actual) + " " + table_name.upper() + ".csv")
            fichero = open(str(fecha_actual) + " " + table_name.upper() + ".csv", "w")
        # else:
        # fichero = open(table_name + ".csv", "w")

        escribir = csv.writer(fichero)

        if table_name == "doc_airport":
            escribir.writerow(
                ("REPORTE NAV: REGISTROS EXISTENTES\t\t-\t\tFECHA", fecha_actual)
            )

        else:
            escribir.writerow(
                (
                    "REPORTE NAV: " + str(table_name).upper() + "\t\t-\t\tFECHA",
                    fecha_actual,
                )
            )

        escribir.writerow(
            ("Id", " Aeropuerto", " Sistema", " Mes", " Archivos", " Año")
        )

        sql = "SELECT *FROM " + table_name

        resultado = operacion_db_buscar(sql)
        y = 0

        a = len(resultado)
        if a != 0:

            for x in resultado:
                res = resultado[y]
                escribir.writerow(
                    (
                        res[0],
                        res[1],
                        res[2],
                        res[3],
                        res[4],
                        res[5],
                    )
                )

                y = y + 1

            fichero.flush()
            fichero.close()

            try:
                pdf = FPDF()
                pdf.add_page()

                pdf.set_font("Helvetica", "BU")
                # Image(string file [, float x [, float y [, float w [, float h [, string type [, mixed link]]]]]])

                pdf.image("logo.png", 145, -4, 52)

                if table_name == "doc_airport":
                    archivo = open(nombre_tabla_completa, "r")

                else:
                    archivo = open(
                        str(fecha_actual) + " " + table_name.upper() + ".csv", "r"
                    )

                # archivo = open("Archivo-CSV.csv", "r")

                for z in archivo:
                    pdf.cell(250, 4, txt=z, ln=1, align="L")

                    pdf.set_font("Helvetica", size=10)

                if table_name == "doc_airport":
                    nombre_tabla_completa_pdf = (
                        str(fecha_actual) + " Registros_completos.pdf"
                    )
                    nombre_tabla_completa_pdf = nombre_tabla_completa_pdf.upper()
                    pdf.output(nombre_tabla_completa_pdf)
                else:
                    pdf.output(str(fecha_actual) + " " + table_name.upper() + ".pdf")

                vista.w13 = Label(vista.master, text="OK", foreground="green")
                vista.w13.place(x=530, y=120)

                if table_name == "doc_airport":
                    table_name = "Registros completos"
                table_name = table_name.upper()
                showinfo("Message", table_name + " -> Archivos exportados en CSV y PDF")
            except IOError:
                showinfo("Message Error", "Archivo no creado")
        else:
            showinfo("Message", "No hay registros en la base de datos")
    else:
        showinfo("Message", "No hay registros en la base de datos")


def log_rechazado(array_rechazado):

    from vista import combo_fir

    combo_seleccionado = combo_fir.get()

    try:
        logging.basicConfig(
            filename="Archivos_rechazados_" + str(combo_seleccionado) + ".log",
            filemode="w",
            format="%(asctime)s : %(levelname)s : %(message)s",
            datefmt="%d/%m/%y %H:%M:%S",
            level=logging.INFO,
        )
        a = 0
        for x in array_rechazado:

            logging.info(
                "Se ha Rechazado el archivo: " + str(array_rechazado[a]) + "\n"
            )
            a += 1

        logging.shutdown()

    except:
        print("Error inesperado")
        logging.fatal("Error inesperado")
