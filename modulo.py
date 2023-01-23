from tkinter import *
import sys
from module_base_de_datos import connection_db
import itertools
import csv
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *
import vista
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

        """esta funcion carga los archivos en la base de datos"""

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

    def cargar_csv(self, id, airport, system, files, year, fir):

        """esta funcion carga la tabla en el .csv al exportar"""

        registers = Doc_input(airport, system, files, year, fir)
        self.doc_search.append(registers)

    def separar_por_sitio(self):

        """Esta funcion se utiliza para separar todos los archivos por su regional"""

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

        """Esta funcion analiza por fir seleccionada la información existente"""

        import re
        from module_base_de_datos import operacion_db_buscar
        from module_base_de_datos import operacion_db
        import module_variable as mod_var
        from vista import combo_fir, mes_desde_input, mes_hasta_input, w11

        global str_system
        global informacion
        global mes
        global files_mes
        global files_mes_aux
        global files_mes_aux_2
        global aux_mes_anterior
        global aux_airport
        global aux_system
        global array_ils
        global array_ils_sin_dme
        global array_li
        global array_vor
        global array_vor_sin_dme
        global array_total
        global no_data_mes
        global anio_desde
        global anio_hasta
        global aux_mes_2
        global periodo
        global check_mes_hasta, check_mes_desde
        global anio_state
        global array_rechazados
        global aux_system_2
        global special_var
        no_data_mes = False
        array_rechazados = []
        check_mes_hasta = False
        check_mes_desde = False
        periodo = False
        informacion = ""
        anio_state = True
        special_var = False

        array_ils = ["LH", "DME ILS PARAMETROS", "ILS PARAMETROS"]

        array_vor = [
            "LH",
            "VOR PARAMETROS II",
            "VOR PARAMETROS I",
            "DME VOR PARAMETROS",
        ]

        array_li = ["LH", "LI PARAMETROS"]

        array_vor_sin_dme = [
            "LH",
            "VOR PARAMETROS II",
            "VOR PARAMETROS I",
        ]

        array_ils_sin_dme = ["LH"]

        array_total = set(array_ils + array_li + array_vor)

        files_mes = []
        files_mes_aux = []
        files_mes_aux_2 = []

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
                anio_desde = int(mes_desde_input.get())

            elif (aux_system != informacion[2]) & (check_mes_hasta == True):

                check_mes_hasta = False
                aux_system = informacion[2]
                check_mes_desde = False
                anio_desde = int(mes_desde_input.get())

            elif (aux_airport == informacion[1]) & (check_mes_hasta == True):

                check_mes_hasta = False
                check_mes_desde = False
                periodo = False
                anio_desde = int(mes_desde_input.get())

            if (
                (aux_airport == informacion[1])
                & (check_mes_hasta == False)
                & (aux_system == informacion[2])
            ):

                aux_mes_2 = aux_mes_anterior
                file_cadena = informacion[3]

                mes = file_cadena[5] + file_cadena[6]

                mes_array = int(mes)

                if len(files_mes_aux) != 0:
                    mes_pend = files_mes_aux[5] + files_mes_aux[6]
                    mes_array_pend = int(mes_pend)
                    # agrego el 12-01

                    if mes_array_pend <= anio_hasta:  # agrego el 12-01

                        if (special_var == True) & (mes_array_pend > aux_mes_anterior):
                            while aux_mes_anterior < mes_array_pend: #agrego el 23-1
                                self.check_array()
                                aux_mes_anterior += 1
                                anio_desde = aux_mes_anterior  # agrego el 10/01
                                special_var = False

                        if mes_array_pend != mes_array:
                            files_mes = []  # comento el 27-12
                            files_mes.append(files_mes_aux)
                            aux_mes_anterior_2 = aux_mes_anterior
                            aux_mes_anterior = mes_array_pend
                            aux_airport_2 = aux_airport
                            aux_airport = (
                                files_mes_aux[11]
                                + files_mes_aux[12]
                                + files_mes_aux[13]
                            )
                            aux_system_2 = aux_system
                            aux_system = (
                                files_mes_aux[15]
                                + files_mes_aux[16]
                                + files_mes_aux[17]
                            )

                            if aux_system == "DME":
                                aux_system = (
                                    files_mes_aux[19]
                                    + files_mes_aux[20]
                                    + files_mes_aux[21]
                                )

                            files_mes_aux = []
                            anio_state = False  # agrego 29-12 10.30 hs
                            self.check_array()
                            aux_mes_anterior = aux_mes_anterior_2
                            aux_airport = aux_airport_2
                            aux_system = aux_system_2
                            anio_desde += 1  ### 23-12
                            anio_state = True

                            aux_mes_anterior += 1
                        files_mes_aux_2 = files_mes_aux  # agrego 28-12
                        files_mes_aux = []  # se borra el 27-12

                ############

                if mes_array >= anio_desde:
                    check_mes_desde = True
                ########### modificación 5-10-22

                if (files_mes_aux_2 != []) & (periodo == True):
                    mes_array = anio_hasta
                    periodo = False
                    special_var = True
                    anio_state = False
                    aux_airport = (
                        files_mes_aux_2[11] + files_mes_aux_2[12] + files_mes_aux_2[13]
                    )
                    aux_system = (
                        files_mes_aux_2[15] + files_mes_aux_2[16] + files_mes_aux_2[17]
                    )
                while (anio_desde < mes_array) & (
                    mes_array <= anio_hasta
                ):  # agrego 12-01

                    if (files_mes_aux_2 != []) & (
                        special_var == False  # agrego el 03-01 a las 01hs
                    ):  # agrego 29-12 14.3 hs
                        mes_array = int(files_mes_aux_2[5] + files_mes_aux_2[6])

                    aux_mes_anterior = anio_desde

                    anio_desde += 1
                    no_data_mes = True

                    file_cadena = []  # agrego esto 12/12
                    periodo = self.check_array()
                    anio_state = True

                    if periodo == True:
                        periodo = False
                        break
                    aux_mes_anterior = anio_desde

                if files_mes_aux_2 != []:
                    mes_array = int(files_mes_aux_2[5] + files_mes_aux_2[6])
                    if int(mes) > aux_mes_anterior:
                        files_mes.append(files_mes_aux_2)
                        anio_state = False
                        files_mes_aux_2 = []
                        periodo = self.check_array()
                        anio_state = True
                        aux_mes_anterior = int(mes)
                        files_mes = []
                        anio_desde = aux_mes_anterior

                if (
                    (informacion[2] == aux_system)
                    & ((aux_mes_anterior) == int(mes))
                    & (periodo == False)
                    & (aux_airport == informacion[1])
                ):
                    files_mes.append(informacion[3])
                    if files_mes_aux_2 != []:  # agrego 03-01 12.30 hs
                        mes_array = int(
                            files_mes_aux_2[5] + files_mes_aux_2[6]
                        )  # agrego 03-01 12.30 hs
                        if int(mes) == aux_mes_anterior:  # agrego 03-01 12.30 hs
                            files_mes.append(files_mes_aux_2)  # agrego 03-01 12.30 hs
                            files_mes_aux_2 = []  # agrego 03-01 14.02 HS
                    aux_mes_anterior = int(mes)
                    anio_state = False
                else:  # una vez cargado todo el mes, analiza la información

                    if (
                        (periodo == False)
                        & (check_mes_hasta == False)
                        & (check_mes_desde == True)
                    ):  #####################
                        anio_state = True  #################23-12 19 hs
                        periodo = self.check_array()
                        anio_desde += 1  # agregooooooo      29-12 18.30 hs
                        check_mes_desde = False
                    else:
                        periodo = False
                        anio_desde = int(mes_desde_input.get())

            else:

                if (aux_mes_anterior <= anio_hasta) & (check_mes_hasta == False):
                    aux_system_2 = aux_system  # agrego esto 28-12 11 hs
                    no_data_mes = True
                    periodo = self.check_array()  #############################
                    aux_mes_anterior += 1
                    if periodo == False:
                        anio_state = True  # agrego esto 28-12 11 hs
                        periodo = self.check_array()
                        files_mes_aux_2 = informacion[3]
                        mes_pend = (
                            files_mes_aux_2[5] + files_mes_aux_2[6]
                        )  # agreego esto 28-12 16 hs

                        if (aux_system_2 != informacion[2]) & (
                            aux_mes_anterior > int(mes_pend)
                        ):
                            files_mes_aux = informacion[3]

                            while (aux_mes_anterior < anio_hasta) & (
                                check_mes_hasta == False
                            ):
                                aux_mes_anterior += 1
                                aux_system = aux_system_2
                                periodo = self.check_array()

                        elif (
                            (aux_system_2 == informacion[2])
                            & (aux_mes_anterior > int(mes_pend))
                            & (aux_airport != informacion[1])
                        ):

                            files_mes_aux = informacion[3]
                            while (aux_mes_anterior < anio_hasta) & (
                                check_mes_hasta == False
                            ):
                                aux_mes_anterior += 1
                                aux_system = aux_system_2
                                periodo = self.check_array()

                        if check_mes_hasta == False:
                            files_mes_aux = []
                            aux_system_2 = ""  # agrego esto 28-12 11 hs

                    else:
                        periodo = False
                        anio_desde = int(mes_desde_input.get())
                        aux_mes_anterior = (
                            anio_desde  # 27-12 19 hs #######################
                        )
        if informacion != "":

            if (periodo == False) & (check_mes_hasta == False):
                self.check_array()
            while (
                (aux_mes_anterior < anio_hasta)
                & (periodo == False)
                & (check_mes_hasta == False)
            ):
                anio_state = True
                aux_mes_anterior += 1
                periodo = self.check_array()

            vista.w11.destroy()
            vista.w11 = Label(vista.master, text="OK", foreground="green")
            vista.w11.place(x=530, y=90)

            showinfo("MENSAJE", "Operación exitosa")
            aux_system = ""
            array_system = ""
            informacion = []

            if len(array_rechazados) != 0:
                log_rechazado(array_rechazados)
                array_rechazados = []
                showinfo("MENSAJE", "Se ha generado un log con archivos rechazados")
        else:
            showinfo("MENSAJE", "No hay información disponible")

    def check_array(self):

        """esta función compara los documentos existentes del aeropuerto, con los que exige el manual técnico y el procedimiento"""

        from vista import mes_desde_input
        import module_variable as mod_var

        global str_system
        global files_mes, files_mes_aux
        global aux_system
        global aux_mes_anterior
        global aux_airport
        global sistema_auxiliar
        global aux_system
        global array_ils
        global array_ils_sin_dme
        global array_li
        global array_vor
        global array_vor_sin_dme
        global array_total
        global anio_hasta, anio_desde
        global aux_mes_2
        global periodo
        global check_mes_hasta
        global check_mes_desde
        global array_rechazados
        global anio_state
        global files_mes_aux_2
        global special_var

        a = 0
        c = 0
        sistema_auxiliar = NONE
        comando_ok = False
        command_array = []

        array_system = ""

        if (len(files_mes_aux) != 0) & (anio_state == False):
            for pend_files in files_mes_aux:
                files_mes.append(pend_files)

            files_mes_aux = []

        if (len(files_mes_aux_2) != 0) & (anio_state == False):

            files_mes.append(files_mes_aux_2)

            files_mes_aux_2 = []

        b = len(files_mes)

        if aux_system == "ILS":
            array_system = array_ils

        elif aux_system == "VOR":
            array_system = array_vor
            sistema_auxiliar = aux_system

        elif (aux_system == "LI") or (aux_system == "LI "):
            array_system = array_li

        match aux_airport:

            case "GPI":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "LYE":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "MJZ":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "PTA":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "VIE":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "NIN":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "SDE":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "GBE":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "USU":
                if aux_system == "VOR":
                    array_system = array_vor_sin_dme
            case "DIL":
                if aux_system == "ILS":
                    array_system = array_ils_sin_dme
            case "RYD":
                if aux_system == "ILS":
                    array_system = array_ils_sin_dme

        l = 0

        if anio_state == False:
            ####################
            while a < b:
                rechazado = False
                c = 0
                for array_data in array_system:  # array_total:

                    if array_data in files_mes[a]:
                        try:
                            if array_data == "VOR PARAMETROS II":

                                rechazado = True
                                mod_var.contador_vor_par_2 += 1
                                break
                            else:
                                if array_data == "LH":
                                    if ("DME ILS" in files_mes[a]) or (
                                        "DME VOR" in files_mes[a]
                                    ):
                                        pass
                                    else:
                                        command = str(array_data)
                                        array_system.remove(command)
                                        rechazado = True
                                        command_array.append(command)
                                ####
                                else:
                                    command = str(array_data)
                                    array_system.remove(command)
                                    rechazado = True
                                    command_array.append(command)
                                ####
                                break
                        except:
                            pass

                if rechazado == False:
                    c = 0

                    while c < len(command_array):

                        if command_array[c] in files_mes[a]:
                            comando_ok = True
                            break
                        c += 1
                    if comando_ok == False:
                        array_rechazados.append(files_mes[a])
                        # break
                a += 1

                if len(array_system) == 0:
                    break
            #################################################

        try:
            if aux_system == "VOR":
                array_system.remove("VOR PARAMETROS II")

            str_system = "-".join(array_system)
            anio = informacion[4]
            fir = informacion[5]
            self.registrar_pendientes(
                aux_airport,
                aux_system,
                aux_mes_anterior,
                str_system,
                anio,
                fir,
            )

        except:
            print(aux_system + " no esta en la lista")

        if aux_mes_anterior == anio_hasta:

            anio_desde = int(mes_desde_input.get())

            if ((mod_var.contador_vor_par_2 >= 1) & (sistema_auxiliar == "VOR")) or (
                (mod_var.contador_vor_par_2 == 0) & (sistema_auxiliar == "VOR")
            ):

                if anio_hasta - anio_desde == 11:

                    resta = 4 - mod_var.contador_vor_par_2
                    if resta > 0:
                        self.registrar_pendientes(
                            aux_airport,
                            sistema_auxiliar,
                            "1-" + str(anio_hasta),
                            str(resta) + " FOLIO/S VOR PARAMETROS II (trimestrales)",
                            anio,
                            fir,
                        )

                elif anio_hasta - anio_desde > 9:

                    resta = 3 - mod_var.contador_vor_par_2
                    if resta > 0:
                        self.registrar_pendientes(
                            aux_airport,
                            sistema_auxiliar,
                            "1-" + str(anio_hasta),
                            str(resta) + " FOLIO VOR PARAMETROS II (trimestrales)",
                            anio,
                            fir,
                        )
                elif anio_hasta - anio_desde > 6:

                    resta = 2 - mod_var.contador_vor_par_2
                    if resta > 0:
                        self.registrar_pendientes(
                            aux_airport,
                            sistema_auxiliar,
                            "1-" + str(anio_hasta),
                            str(resta) + " FOLIO VOR PARAMETROS II (trimestrales)",
                            anio,
                            fir,
                        )
                elif anio_hasta - anio_desde > 3:
                    resta = 1 - mod_var.contador_vor_par_2
                    if resta > 0:
                        self.registrar_pendientes(
                            aux_airport,
                            sistema_auxiliar,
                            "1-" + str(anio_hasta),
                            str(resta) + " FOLIO VOR PARAMETROS II (trimestrales)",
                            anio,
                            fir,
                        )

            mod_var.contador_vor_par_2 = 0

            files_mes_aux_2 = []
            periodo = True
            aux_airport = informacion[1]

            aux_mes_anterior = anio_desde
            check_mes_hasta = True
            check_mes_desde = False

            files_mes_aux = informacion[3]

            mes_state = files_mes_aux[5] + files_mes_aux[6]

            if int(mes_state) > 1:
                anio_state = True
                files_mes_aux_2 = informacion[3]
                special_var = True

        return periodo

    def registrar_pendientes(
        self, aeropuerto, sistema, mes_analizado, sistema_pendiente, anio, fir
    ):
        """esta funcion carga en la base de datos los archivos pendientes"""

        from module_base_de_datos import operacion_db
        from vista import combo_fir, mes_desde_input

        global sistema_auxiliar
        global mes
        global files_mes
        global aux_system
        global array_ils
        global array_ils_sin_dme
        global array_li
        global array_vor
        global array_vor_sin_dme
        global no_data_mes
        global anio_desde
        global aux_system_2

        fir_seleccionada = combo_fir.get()
        if str_system != "":

            sql = (
                "INSERT INTO "
                + fir_seleccionada
                + "_pendientes(AIRPORT,SYSTEM,MES,OBSERVACIONES,YEAR,FIR)VALUES(%s,%s,%s,%s,%s,%s)"
            )
            val = [
                aeropuerto,
                sistema,
                str(mes_analizado),
                "Falta entregar: " + "" + sistema_pendiente,
                anio,
                fir,
            ]
            operacion_db(sql, val)

        files_mes = []
        if no_data_mes == False:

            if informacion[2] != aux_system:
                anio_desde = int(mes_desde_input.get())

            files_mes.append(informacion[3])
            sistema_auxiliar = aux_system
            aux_system = informacion[2]

        no_data_mes = False

        array_ils = ["LH", "DME ILS PARAMETROS", "ILS PARAMETROS"]

        array_vor = [
            "LH",
            "VOR PARAMETROS II",
            "VOR PARAMETROS I",
            "DME VOR PARAMETROS",
        ]

        array_li = ["LH", "LI PARAMETROS"]

        array_vor_sin_dme = [
            "LH",
            "VOR PARAMETROS II",
            "VOR PARAMETROS I",
        ]

        array_ils_sin_dme = ["LH"]


registro = Registros()


def exportar(file_export):

    """esta funcion exporta los datos de la agenda en .pdf .csv"""

    global w12, w13
    from module_base_de_datos import operacion_db_buscar
    import module_variable as mod_var
    from datetime import date

    fecha_actual = date.today()

    titulo = False

    global datosstr
    datosstr = ""

    resultado = ""
    table_name = file_export

    if table_name != "_pendientes":
        if table_name == "doc_airport":

            nombre_tabla_completa = str(fecha_actual) + " Registros_completos.csv"
            nombre_tabla_completa = nombre_tabla_completa.upper()
            if os.path.exists(nombre_tabla_completa):
                os.remove(nombre_tabla_completa)
            fichero = open(nombre_tabla_completa, "w")

        else:

            if os.path.exists(str(fecha_actual) + " " + table_name.upper() + ".csv"):
                os.remove(str(fecha_actual) + " " + table_name.upper() + ".csv")
            fichero = open(str(fecha_actual) + " " + table_name.upper() + ".csv", "w")

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
                pdf.image("logo.png", 145, -4, 52)

                if table_name == "doc_airport":
                    archivo = open(nombre_tabla_completa, "r")

                else:
                    archivo = open(
                        str(fecha_actual) + " " + table_name.upper() + ".csv", "r"
                    )

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

    """esta función genera un log con los archivos rechazados según la región que se analizó"""

    from vista import combo_fir

    combo_seleccionado = combo_fir.get()

    try:

        if len(array_rechazado) != 0:

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
