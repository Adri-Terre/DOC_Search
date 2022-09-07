from peewee import *
import mysql.connector
from tkinter.filedialog import askopenfilename
from tkinter import Label
from tkinter.messagebox import *

import module_variable as mod_var


def connection_db():

    """ este script permite conectarse con la tabla de la base de datos, y si no existe la crea con MySQL. """

    my_db = mysql.connector.connect(host="localhost", user="root", password="")
    mycursor = my_db.cursor()
    sql = "DROP DATABASE IF EXISTS DOC_SEARCH"
    mycursor.execute(sql)

    try:

        my_db = mysql.connector.connect(host="localhost", user="root", password="")
        mycursor = my_db.cursor()
        sql = "CREATE DATABASE DOC_SEARCH"
        mycursor.execute(sql)

        print("Nueva base de datos: doc_search - creada")

        my_db = mysql.connector.connect(
            host="localhost", user="root", password="", database="doc_search"
        )
        mod_var.mycursor = my_db.cursor()
        mod_var.mycursor.execute(
            "CREATE TABLE doc_airport (ID INT AUTO_INCREMENT PRIMARY KEY, AIRPORT VARCHAR(255),SYSTEM VARCHAR(255),FILES VARCHAR(255), YEAR VARCHAR(255), FIR VARCHAR(255)"
        )
        mod_var.mycursor.execute(
            "CREATE TABLE fir_eze (ID INT AUTO_INCREMENT PRIMARY KEY, AIRPORT VARCHAR(255),SYSTEM VARCHAR(255),FILES VARCHAR(255), YEAR VARCHAR(255), FIR VARCHAR(255)"
        )
        mod_var.mycursor.execute(
            "CREATE TABLE fir_doz (ID INT AUTO_INCREMENT PRIMARY KEY, AIRPORT VARCHAR(255),SYSTEM VARCHAR(255),FILES VARCHAR(255), YEAR VARCHAR(255), FIR VARCHAR(255)"
        )
        mod_var.mycursor.execute(
            "CREATE TABLE fir_sis (ID INT AUTO_INCREMENT PRIMARY KEY, AIRPORT VARCHAR(255),SYSTEM VARCHAR(255),FILES VARCHAR(255), YEAR VARCHAR(255), FIR VARCHAR(255)"
        )
        mod_var.mycursor.execute(
            "CREATE TABLE fir_cba (ID INT AUTO_INCREMENT PRIMARY KEY, AIRPORT VARCHAR(255),SYSTEM VARCHAR(255),FILES VARCHAR(255), YEAR VARCHAR(255), FIR VARCHAR(255)"
        )
        mod_var.mycursor.execute(
            "CREATE TABLE fir_crv (ID INT AUTO_INCREMENT PRIMARY KEY, AIRPORT VARCHAR(255),SYSTEM VARCHAR(255),FILES VARCHAR(255), YEAR VARCHAR(255), FIR VARCHAR(255)"
        )
        mod_var.mycursor.execute(
            "CREATE TABLE aep_table (ID INT AUTO_INCREMENT PRIMARY KEY, AIRPORT VARCHAR(255),FIR VARCHAR(255)"
        )
        db_conectado = True
        # db_tabla_aep = True
        return db_conectado

    except mysql.connector.Error as err:

        if err.errno == 2003:
            showinfo(
                "Conexión a base de datos",
                "No conectado. Verifique que los servicios de MySQL se estén ejecutando",
            )
            db_conectado = False
            return db_conectado

        else:

            mibase = MySQLDatabase(
                "doc_search", user="root", password="", host="localhost", port=3306
            )
            # mibase = MySQLDatabase(
            #    "aep_table", user="root", password="", host="localhost", port=3306
            # )

            class BaseModel(Model):
                class Meta:
                    database = mibase

            class doc_airport(BaseModel):

                AIRPORT = CharField()
                SYSTEM = CharField()
                FILES = CharField()
                YEAR = CharField()
                FIR = CharField()

            class aep_table(BaseModel):

                AIRPORT = CharField()
                FIR = CharField()

            class fir_cba(BaseModel):

                AIRPORT = CharField()
                SYSTEM = CharField()
                FILES = CharField()
                YEAR = CharField()
                FIR = CharField()

            class fir_eze(BaseModel):

                AIRPORT = CharField()
                SYSTEM = CharField()
                FILES = CharField()
                YEAR = CharField()
                FIR = CharField()

            class fir_sis(BaseModel):

                AIRPORT = CharField()
                SYSTEM = CharField()
                FILES = CharField()
                YEAR = CharField()
                FIR = CharField()

            class fir_crv(BaseModel):

                AIRPORT = CharField()
                SYSTEM = CharField()
                FILES = CharField()
                YEAR = CharField()
                FIR = CharField()

            class fir_doz(BaseModel):

                AIRPORT = CharField()
                SYSTEM = CharField()
                FILES = CharField()
                YEAR = CharField()
                FIR = CharField()

            class fir_cba_pendientes(BaseModel):

                AIRPORT = CharField()
                SYSTEM = CharField()
                MES = CharField()
                OBSERVACIONES = CharField()
                YEAR = CharField()
                FIR = CharField()

            mibase.connect()
            mibase.create_tables([doc_airport])
            mibase.create_tables([aep_table])
            mibase.create_tables([fir_cba])
            mibase.create_tables([fir_sis])
            mibase.create_tables([fir_crv])
            mibase.create_tables([fir_eze])
            mibase.create_tables([fir_doz])

            mibase.create_tables([fir_cba_pendientes])
            db_conectado = True

        if err.errno == 1007:
            mod_var.db_table_aep = True
        return db_conectado
    except:
        pass


def operacion_db(sql, val):

    """ esta funcion, a traves de Peewee, se utiliza para grabar/actualizar los contactos en la base de datos """

    my_db = MySQLDatabase(
        "doc_search", user="root", password="", host="localhost", port=3306
    )
    mod_var.mycursor = my_db.cursor()
    mod_var.mycursor.execute(sql, val)
    my_db.commit()


def operacion_db_buscar(sql):

    """ esta funcion, a traves de Peewee, se utiliza para buscar los contactos en la base de datos """

    my_db = MySQLDatabase(
        "doc_search", user="root", password="", host="localhost", port=3306
    )
    mod_var.mycursor = my_db.cursor()
    mod_var.mycursor.execute(sql)
    resultado = mod_var.mycursor.fetchall()

    return resultado
