#!/usr/bin/env python
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------------------------
# Archivo: procesador_temporizador.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Perla Velasco & Yonathan Mtz.
# Actualizado por lily's team
# Version: 1.0.1 Octubre 2017
# Descripción:
#
#   Ésta clase define el rol de un publicador que envia mensajes a una cola
#   específica.
#   Las características de ésta clase son las siguientes:
#
#                                        SensorTemporizador.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Enviar mensajes      |  - Se conecta a la cola|
#           |      Publicador       |                         |    'direct timer'.     |
#           |                       |                         |  - Envia datos del     |
#           |                       |                         |    medicamento a la    |
#           |                       |                         |    cola.               |
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
#           |                        |                          |  - Genera un número   |
#           | simulate_medicamento() |           None           |    aleatorio entre 0  |
#           |                        |                          |    y 7.               |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Genera un número   |
#           |     simulate_hora()    |           None           |    aleatorio entre 1  |
#           |                        |                          |    y 12.              |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Genera un número   |
#           |   simulate_minutos()   |           None           |    aleatorio entre 0  |
#           |                        |                          |    y 59.              |
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

import pika
import random
import time


class ProcesadorTemporizador:
    nombre = None
    id = 0
    medicinas = ['ibuprofeno', 'insulina', 'furosemida', 'piroxicam', 'tolbutamida']

    def __init__(self, pnombre):
        self.nombre = pnombre
        self.id = int(self.set_id())

    def set_id(self):
        return random.randint(1000, 5000)

    def get_name(self):
        return self.nombre

    #def add_medicamento(self, nombre_medicamento, hora):
    #    self.medicamentos.append(Medicamento(nombre_medicamento, hora))
    #    print(self.nombre + ' vi')

    def consume(self):
        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_timer', type='direct')
        severity = 'temporizador'
        
        
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite enviar datos a la cola seleccionada.            |
        #   +----------------------------------------------------------------------------+
        
        medicinas = self.simulate_med()
        hora = self.simulate_horas()
        minuto = self.simulate_minutos()
        hora_de_sistema = int(time.strftime("%I"))
        minutos_de_sistema = int(time.strftime("%M"))

        if (hora_de_sistema == hora):

        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite enviar datos a la cola seleccionada.            |
        #   +----------------------------------------------------------------------------+
        
            mensaje = 'PA;' + str(self.id) + ';' + self.nombre + ';' + str(self.medicinas[medicinas]) + ';' + str(hora) + ':' + str(minuto) + ';1 tableta'
            channel.basic_publish(exchange='direct_timer',
                                    routing_key=severity, body=mensaje)         
            print('+---------------+--------------------+-------------------------------+-------+')
            print('|      ' + str(self.id) +'     |     ' + self.nombre +'     | hora de medicina: |  ' + str(self.medicamentos[medicinas]) + '  |')
            print('+---------------+--------------------+-------------------------------+-------+')
            print('')
                
        connection.close()

    def simulate_med(self):
        return random.randint(int(0), int(7))

    def simulate_horas(self):
        return random.randint(int(1), int(12))

    def simulate_minutos(self):
        return random.randint(int(0), int(59))
