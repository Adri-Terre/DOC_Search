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

# import logging
# import smtplib, ssl
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
import os

# import json


class Doc_input:
    nuevoId = itertools.count()

    def __init__(self, airport, system, files, year, fir):
        self.codigo = next(self.nuevoId)
        self.airport = airport
        self.system = system
        self.files = files
        self.year = year
        self.fir = fir


class Aep_input:
    nuevoId = itertools.count()

    def __init__(self, airport, fir):
        self.codigo = next(self.nuevoId)
        self.airport = airport
        self.fir = fir


"""
class Patr_Obs:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        pass

    def notificar(self):
        for observador in self.observadores:
            observador.update()


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        self.observador_a = obj
        self.observador_a.agregar(self)

    def update(self):

        try:
            logging.basicConfig(
                filename="Log.log",
                filemode="a",
                format="%(asctime)s : %(levelname)s : %(message)s",
                datefmt="%d/%m/%y %H:%M:%S",
                level=logging.INFO,
            )

            logging.info(
                "Se ha Dado de Alta el registro: Nombre: "
                + str(self.observador_a.contactos[-1].nombre)
                + " Apellido: "
                + str(self.observador_a.contactos[-1].apellido)
                + " Empresa: "
                + str(self.observador_a.contactos[-1].empresa)
                + " Email: "
                + str(self.observador_a.contactos[-1].email)
                + " Telefono: "
                + str(self.observador_a.contactos[-1].movil)
            )
            print(
                "@Patron observador: Se ha dado de alta un registro en archivo Log.log"
            )
        except:
            print("Error inesperado")
            logging.fatal("Error inesperado")
"""


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

    def cargar_sitios(self, airport, fir):

        """ esta funcion carga un contacto en la base de datos """
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

    def cargar_csv(self, id, airport, system, files, year, fir):

        """ esta funcion carga la tabla en el .csv al exportar """

        registers = Doc_input(airport, system, files, year, fir)
        self.doc_search.append(registers)

    """
    def funcion_decorar_actualizar(funcion_m):
        def funcion_interna_m(
            self,
            nombre,
            apellido,
            empresa,
            email,
            movil,
            codigo,
            nombre_aux,
            apellido_aux,
            empresa_aux,
            email_aux,
            movil_aux,
            image_64_encode_aux,
        ):

            funcion_m(
                self,
                nombre,
                apellido,
                empresa,
                email,
                movil,
                codigo,
                nombre_aux,
                apellido_aux,
                empresa_aux,
                email_aux,
                movil_aux,
                image_64_encode_aux,
            )
            print("@Decorador: Actualización de registro en archivo Log.log")

            try:
                logging.basicConfig(
                    filename="Log.log",
                    filemode="a",
                    format="%(asctime)s : %(levelname)s : %(message)s",
                    datefmt="%d/%m/%y %H:%M:%S",
                    level=logging.INFO,
                )

                logging.info(
                    "Se realizan los siguientes cambios: Nombre: "
                    + str(nombre)
                    + " Apellido: "
                    + str(apellido)
                    + " Empresa: "
                    + str(empresa)
                    + " Email: "
                    + str(email)
                    + " Telefono: "
                    + str(movil)
                )

            except:
                print("Error inesperado")
                logging.fatal("Error inesperado")

        return funcion_interna_m

    def funcion_decorar_eliminar(funcion_e):
        def funcion_interna_e(
            self, nombre, apellido, empresa, email, movil, codigo,
        ):
            funcion_e(self, nombre, apellido, empresa, email, movil, codigo)
            import module_variable as mod_var

            if mod_var.var_eliminar == True:

                print("@Decorador: Se ha eliminado un registro")

                if askyesno(
                    "Consulta", "¿Desea enviar el registro eliminado por email?"
                ):

                    mail_from = input("\ningrese su correo electronico\n")
                    username = mail_from
                    password = input("\ningrese la contraseña\n")
                    mail_to = input(
                        "\ningrese el correo electronico del destinatario\n"
                    )
                    mail_subject = "Python"
                    mail_body = (
                        "Eliminación de registro: Nombre: "
                        + str(nombre)
                        + " Apellido: "
                        + str(apellido)
                        + " Empresa: "
                        + str(empresa)
                        + " Email: "
                        + str(email)
                        + " Telefono: "
                        + str(movil)
                    )

                    try:
                        mimemsg = MIMEMultipart()
                        mimemsg["From"] = mail_from
                        mimemsg["To"] = mail_to
                        mimemsg["Subject"] = mail_subject
                        mimemsg.attach(MIMEText(mail_body, "plain"))
                        connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
                        connection.starttls()
                        connection.login(username, password)
                        connection.send_message(mimemsg)
                        connection.quit()
                        print("\ncorreo electronico enviado\n")
                    except:
                        print(
                            "Verifique los datos ingresados y/o verifique los permisos en su cuenta GMAIL"
                        )
                else:
                    pass

        return funcion_interna_e

    @funcion_decorar_actualizar
    def actualizar(
        self,
        nombre,
        apellido,
        empresa,
        email,
        movil,
        codigo,
        nombre_aux,
        apellido_aux,
        empresa_aux,
        email_aux,
        movil_aux,
        image_64_encode_aux,
    ):
"""

    """        
 # esta funcion se emplea para actualizar/eliminar un contacto 
    
        import module_variable as mod_var
        from module_base_de_datos import operacion_db

        mod_var.func_modificar = False

        #aqui se actualiza la base de datos 

        if askyesno("Consulta", "¿Desea actualizar el contacto?"):

            sql = "UPDATE contactos SET NOMBRE = %s WHERE NOMBRE = %s"
            val = (nombre, nombre_aux)
            operacion_db(sql, val)
            sql = "UPDATE contactos SET APELLIDO = %s WHERE APELLIDO = %s"
            val = (apellido, apellido_aux)
            operacion_db(sql, val)
            sql = "UPDATE contactos SET EMPRESA = %s WHERE EMPRESA = %s"
            val = (empresa, empresa_aux)
            operacion_db(sql, val)
            sql = "UPDATE contactos SET EMAIL = %s WHERE EMAIL = %s"
            val = (email, email_aux)
            operacion_db(sql, val)
            sql = "UPDATE contactos SET TELEFONO = %s WHERE TELEFONO = %s"
            val = (movil, movil_aux)
            operacion_db(sql, val)

            if mod_var.actualizar_imagen == True:
                sql = "UPDATE contactos SET FOTO = %s WHERE FOTO = %s"
                val = (mod_var.image_64_encode, image_64_encode_aux)
                operacion_db(sql, val)
                mod_var.actualizar_imagen = False

            showinfo("OK", "Operación exitosa")

    @funcion_decorar_eliminar
    def eliminar(self, nombre, apellido, empresa, email, movil, codigo):

        #esta funcion se emplea para eliminar un contacto

        import module_variable as mod_var
        from module_base_de_datos import operacion_db

        mod_var.func_modificar = False

        #aquí se elimina lo deseado de la base de datos

        if askyesno("Consulta", "¿Desea eliminar el contacto?"):
            sql = "DELETE FROM contactos WHERE ID = '%s'"
            val = (codigo,)
            operacion_db(sql, val)
            showinfo("OK", "Operación exitosa")
            mod_var.func_eliminar = False
        else:
            mod_var.var_eliminar = False
    """

    def buscar(self, textoBuscar):

        """ Esta funcion se utiliza tanto para buscar todos los contactos en la agenda, como así también uno específico """

        from module_base_de_datos import operacion_db_buscar
        import module_variable as mod_var

        mod_var.encontrado = 0
        mod_var.no_encontrado = 0
        mod_var.total_encontrados = 0
        sql = "SELECT *from contactos"
        resultado = operacion_db_buscar(sql)

        for contacto in resultado:
            for x in contacto:

                if textoBuscar == "TODOS":
                    if mod_var.encontrado == 0:
                        n = 0
                        while n < 6:
                            mod_var.contacto_search.append(contacto[n])
                            n += 1
                        mod_var.no_encontrado = 1
                    mod_var.encontrado = mod_var.encontrado + 1
                    if mod_var.encontrado == 7:
                        mod_var.encontrado = 0
                        mod_var.contacto_encontrado = contacto
                elif textoBuscar == x:
                    mod_var.total_encontrados += 1
                    mod_var.contacto_encontrado = contacto
                    mod_var.encontrado = mod_var.encontrado + 1
                    mod_var.no_encontrado = 1

        buscartodos_boton = False
        return mod_var.contacto_encontrado

    def grabar(self):

        """ esta funcion se emplea para exportar la agenda a .csv"""

        with open("Archivo-CSV.csv", "w") as fichero:
            escribir = csv.writer(fichero)
            escribir.writerow(("ID", "airport", "system", "files", "year", "fir"))
            for registers in self.doc_search:
                escribir.writerow(
                    (
                        registers.codigo,
                        registers.airport,
                        registers.files,
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

    fichero = open("Archivo-CSV.csv", "wb")
    sql = "SELECT *FROM doc_airport"
    resultado = operacion_db_buscar(sql)
    y = 0

    a = len(resultado)
    if a != 0:
        for x in resultado:

            res = resultado[y]
            codigo = res[0]
            airport = res[1]
            system = res[2]
            files = res[3]
            year = res[4]
            fir = res[5]

            y = y + 1

            registro.cargar_csv(codigo, airport, system, files, year, fir)
            registro.grabar()

        fichero.flush()
        fichero.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=9)
        archivo = open("Archivo-CSV.csv", "r")

        for z in archivo:
            pdf.cell(250, 5, txt=z, ln=1, align="c")
        pdf.output("Archivo-PDF.pdf")

        """
        archivo = os.path.dirname(os.path.abspath(__file__)) + "\\Archivo-XML.xml"
        # Creamos cabecera
        cabecera = '<?xml version="1.0" encoding="utf-8"?>'
        # Creamos elementos raíz

        raiz = ET.Element("Agenda")

        sql = "SELECT *FROM contactos"
        resultado = operacion_db_buscar(sql)
        y = 0

        for x in resultado:

            res = resultado[y]
            codigo = res[0]
            nombres = res[1]
            apellidos = res[2]
            empresas = res[3]
            emails = res[4]
            moviles = res[5]

            y = y + 1

            # Creamos atributo

            usuario = ET.SubElement(raiz, "Contacto")
            nombre = ET.SubElement(usuario, "nombre")
            apellido = ET.SubElement(usuario, "apellido")
            empresa = ET.SubElement(usuario, "empresa")
            email = ET.SubElement(usuario, "email")
            celular = ET.SubElement(usuario, "celular")

            nombre.set("completo", nombres)
            apellido.set("completo", apellidos)
            empresa.set("completo", empresas)
            email.set("completo", emails)
            celular.set("completo", moviles)

            nombre.text = "Registro número: " + str(codigo)
            apellido.text = "Registro número: " + str(codigo)
            empresa.text = "Registro número: " + str(codigo)
            email.text = "Registro número: " + str(codigo)
            celular.text = "Registro número: " + str(codigo)

            # creamos XML
            datos = ET.tostring(raiz)
            datosstr = datos.decode("utf-8")

        archivo = open(archivo, "w")
        archivo.write(cabecera)
        archivo.write(datosstr)
        archivo.close()

        # JSON

        sql = "SELECT *FROM contactos"
        resultado = operacion_db_buscar(sql)
        y = 0
        data = {}
        data["contactos"] = []

        for x in resultado:

            res = resultado[y]
            codigo = res[0]
            nombres = res[1]
            apellidos = res[2]
            empresas = res[3]
            emails = res[4]
            moviles = res[5]

            y = y + 1
            data["contactos"].append(
                {
                    "Nombre": nombres,
                    "Apellido": apellidos,
                    "Empresa": empresas,
                    "Email": emails,
                    "Celular": moviles,
                }
            )

            file_name = "Archivo-JSON.json"

            with open(file_name, "w") as file:
                json.dump(data, file, indent=4)
        """
        showinfo("Exportar", "Contactos exportados en CSV, PDF")  # , XML Y JSON")

    else:
        showinfo("Exportar", "No hay registros en la base de datos")
