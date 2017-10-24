#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Archivo: SensorTemporizador.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Perla Velasco & Yonathan Mtz & Alan Mercado.
# Version: 1.5.2 Marzo 2017
# Descripción:
#
#   Ésta clase define el rol de un publicador que envia mensajes a una cola
#   específica.
#   Las características de ésta clase son las siguientes:
#
#                                      SensorTemporizador.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Enviar mensajes      |  - Se conecta a la cola|
#           |      Publicador       |                         |    'direct timer      '|
#           |                       |                         |  - Envia datos de tiem-|
#           |                       |                         |    po a la cola.       |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Inicializa los va- |
#           |       __init__()       |      String: nombre      |    lores de nombre e  |
#           |                        |                          |    id.                |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Genera de manera a-|
#           |        set_id()        |           None           |    leatoria el id del |
#           |                        |                          |    usuario.           |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Devuelve el nombre |
#           |       get_name()       |           None           |    del usuario al cual|
#           |                        |                          |    fue asignado el    |
#           |                        |                          |    sensor.            |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Realiza la conexión|
#           |                        |                          |    con el servidor    |
#           |                        |                          |    de RabbitMQ local. |
#           |                        |                          |  - Define a que cola  |
#           |     start_service()    |           None           |    enviará los mensa- |
#           |                        |                          |    jes.               |
#           |                        |                          |  - Define que tipo de |
#           |                        |                          |    publicación se uti-|
#           |                        |                          |    lizará.            |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |Simula los medicamentos|
#           |     simulate_data()    |           None           |que seran suministrados|
#           |                        |                          |a los pacientes        |
#           +------------------------+--------------------------+-----------------------+
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |Simula la dosis de los |
#           |     simulate_dosis()   |           None           |medicamentos que seran |
#           |                        |                          |suministrados			|
#           +------------------------+--------------------------+-----------------------+
#
#           Nota: "propio de Rabbit" implica que se utilizan de manera interna para realizar
#            de manera correcta la recepcion de datos, para éste ejemplo no shubo necesidad
#            de utilizarlos y para evitar la sobrecarga de información se han omitido sus
#            detalles. Para más información acerca del funcionamiento interno de RabbitMQ
#            puedes visitar: https://www.rabbitmq.com/
#            
#
#--------------------------------------------------------------------------------------------------

import random
import pika


class ProcesadorTemporizador():
    nombre = None
    id = 0
    #horaMed es la hora en que toca tomar las medicinas
    horaMed=24


    def __init__(self, nombre):
        self.nombre = nombre
        self.id = int(self.set_id())

    def set_id(self):
        return random.randint(1000, 5000)

    def get_name(self):
        return self.nombre

    def start_service(self):
        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente línea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente línea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_timer', type='direct')
        severity = 'temp'
        #temp = self.simulate_data()
        #simulate=self.simulate_dosis();
        mensaje = 'TM:' + str(self.id) + ':' + self.nombre + \
            ':' + str(self.horaMed)
        #   +----------------------------------------------------------------------------+
        #   | La siguiente línea permite enviar datos a la cola seleccionada.            |
        #   +----------------------------------------------------------------------------+
        channel.basic_publish(exchange='direct_timer',
                              routing_key=severity, body=mensaje)        

        print('+---------------+--------------------+-------------------------------+-------+')
        print('|      ' + str(self.id) +'     |     ' + self.nombre +'     |      HORA ENVIADA      |  ' + str(self.horaMed) +'    | ')
        print('+---------------+--------------------+-------------------------------+-------+')
        print('')

        #Restamos una hora para simular que pasa el tiempo
        self.horaMed = self.horaMed - 1
        #Si la hora llega a cero, se reinicia el temporizador
        if self.horaMed == 0:
        	self.horaMed = 24





        connection.close()