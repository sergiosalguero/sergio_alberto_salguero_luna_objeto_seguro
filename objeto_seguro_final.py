#   Sergio Alberto Salguero Luna
#   Proyecto Final

import socket
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import base64
import random


# Definición de la clase ObjetoSeguro
class ObjetoSeguro:
    def __init__(self, nombre):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port_and_ip = ('127.0.0.1', 12345)
        self.nombre = nombre
        self.__gen_llaves()
        self.__pub_key_destinatario = None
        self.nombre_destinatario = None
        self.flag_s = 0
        self.flag_c = 0
        self.id = 0
        self.id_list = []

    # Métodos de la clase ObjetoSeguro
    def cliente(self):
        # Conectar con el servidor
        self.node.connect(self.port_and_ip)
        print("Se ha establecido conexión con el servidor")
        self.flag_c = 1
        while True:
            # Intercambio de nombres y llaves públicas
            if self.flag_c == 1:
                self.__intercambio_cliente()
            if self.flag_c == 0:
                # Enviar un mensaje
                msg = input(">>> ")
                self.almacenar_msj(msg)
                msg_cif = self.__cifrar_msj(self.__pub_key_destinatario, msg)
                self.saludar(msg_cif)
                if msg == "END":
                    self.flag_c = 1
                    print("Fin de la conexión")
                    break
                if msg == "EXIT":
                    self.node.close()
                    print("Fin de la conexión")
                    exit()
                # Recibir un mensaje
                msg = self.node.recv(1024)
                msg_dec = self.esperar_respuesta(msg)
                if msg_dec == "END":
                    self.flag_c = 1
                    print("Fin de la conexión")
                    break
                if msg_dec == "EXIT":
                    self.node.close()
                    print("Fin de la conexión")
                    exit()

    def servidor(self):
        self.node.bind(self.port_and_ip)
        self.node.listen(5)
        while True:
            # Conectar con un cliente
            print("Esperando conexión...")
            client, address = self.node.accept()
            print("Se ha establecido conexión con un cliente")
            self.flag_s = 1
            while True:
                # Intercambio de llaves públicas
                if self.flag_s == 1:
                    self.__intercambio_servidor(client)
                if self.flag_s == 0:
                    # Recibir un mensaje
                    msg = client.recv(1024)
                    msg_dec = self.__decodificar64(self.__descifrar_msj(msg))
                    print(f'<<< {msg_dec}')
                    if msg_dec == "END":
                        self.flag_s = 1
                        print("Fin de la conexión")
                        break
                    if msg_dec == "EXIT":
                        client.close()
                        self.node.close()
                        print("Fin de la conexión")
                        exit()
                    # Enviar un mensaje
                    msg = input(">>> ")
                    self.responder(client, msg)
                    if msg == "END":
                        self.flag_s = 1
                        print("Fin de la conexión")
                        break
                    if msg == "EXIT":
                        client.close()
                        self.node.close()
                        print("Fin de la conexión")
                        exit()

    def __intercambio_cliente(self):
        # Enviar llave pública
        msj = f'Hola, soy {self.nombre}. Mi llave pública es: ' \
              f'{self.llave_publica()}.'
        print(f'>>> {msj}')
        self.node.send(msj.encode())
        # Recibir llave pública del destinatario
        msj = self.node.recv(1024).decode()
        datos = msj.split('.')
        lista = []
        for i in datos:
            lista.append(i)
        self.nombre_destinatario = lista[1][10:]
        self.__pub_key_destinatario = lista[2][22:]
        print(f'<<< {msj}')
        self.flag_c = 0

    def __intercambio_servidor(self, client):
        # Recibir llave pública del destinario
        msj = client.recv(1024).decode()
        datos = msj.split('.')
        lista = []
        for i in datos:
            lista.append(i)
        self.nombre_destinatario = lista[0][10:]
        self.__pub_key_destinatario = lista[1][22:]
        print(f'<<< {msj}')
        # Enviar llave pública
        msj = f'Hola {self.nombre_destinatario}. Me llamo {self.nombre}. ' \
              f'Mi llave pública es: {self.llave_publica()}.'
        client.send(msj.encode())
        print(f'>>> {msj}')
        self.flag_s = 0

    def __gen_llaves(self):
        priv_key_orig = generate_eth_key()
        self.__priv_key = priv_key_orig.to_hex()
        self.__pub_key = priv_key_orig.public_key.to_hex()

    def saludar(self, msj):
        self.node.send(msj)

    def responder(self, cliente, msj):
        msg_cif = self.__cifrar_msj(self.__pub_key_destinatario, msj)
        cliente.send(msg_cif)
        return msg_cif

    def llave_publica(self):
        return self.__pub_key

    def __cifrar_msj(self, pub_key, msj):
        return encrypt(pub_key, self.__codificar64(msj))

    def __descifrar_msj(self, msj):
        return decrypt(self.__priv_key, msj)

    def __codificar64(self, msj):
        return base64.b64encode(msj.encode('utf-8'))

    def __decodificar64(self, msj):
        return base64.b64decode(msj).decode('utf-8')

    def almacenar_msj(self, msg):
        try:
            archivo = open(f'RegistroMsj_{self.nombre}.txt', 'r')
            flag = True
        except:
            self.id = random.randrange(1000, 1199)
            reg_msg = {'ID': f'{self.id}', 'Mensaje': f'{msg}'}
            archivo = open(f'RegistroMsj_{self.nombre}.txt', 'w')
            archivo.write(f'{reg_msg}')
            archivo.close()
            self.id_list.append(self.id)
            flag = False
        if flag:
            texto = ''
            for each_line in archivo:
                texto = f'{texto}{each_line}'
            archivo.close()
            self.id = random.randrange(1000, 1199)
            reg_msg = {'ID': f'{self.id}', 'Mensaje': f'{msg}'}
            archivo = open(f'RegistroMsj_{self.nombre}.txt', 'w')
            archivo.write(f'{texto}\n{reg_msg}')
            archivo.close()
            self.id_list.append(self.id)
        return {'ID': self.id}

    def consultar_msj(self, id):
        archivo = open(f'RegistroMsj_{self.nombre}.txt')
        reg = {}
        for each_line in archivo:
            if each_line[8:12] == str(id):
                reg = {'ID': f'{each_line[8:12]}',
                       'Mensaje': f'{each_line[27:len(each_line)-2]}'}
        archivo.close()
        return reg

    def esperar_respuesta(self, msj):
        msg_dec = self.__decodificar64(self.__descifrar_msj(msj))
        self.almacenar_msj(msg_dec)
        print(f'<<< {msg_dec}')
        return msg_dec

    def gen_id(self):
        return self.id_list[random.randrange(1, len(self.id_list))-2]
