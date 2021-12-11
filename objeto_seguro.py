#   Sergio Alberto Salguero Luna
#   Proyecto Final (Primera Parte)

from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import base64
import random


# Definición de la clase ObjetoSeguro
class ObjetoSeguro(object):
    def __init__(self, nombre):
        self.nombre = nombre
        self.__priv_key = None
        self.__pub_key = None
        self.pub_key_destinatario = None
        self.id = 0
        self.__gen_llaves()

    # Métodos de la clase ObjetoSeguro
    def __gen_llaves(self):
        priv_key_orig = generate_eth_key()
        self.__priv_key = priv_key_orig.to_hex()
        self.__pub_key = priv_key_orig.public_key.to_hex()

    def saludar(self, msj):
        print(msj)

    def responder(self, msj):
        respuesta = msj + 'MensajeRespuesta'
        print(respuesta)
        respuesta_cif = self.cifrar_msj(
            self.pub_key_destinatario, respuesta)
        return respuesta_cif

    def llave_publica(self):
        return self.__pub_key

    def cifrar_msj(self, pub_key, msj):
        msj_codificado = self.__codificar64(msj)
        encrypted = encrypt(pub_key, msj_codificado)
        return encrypted

    def descifrar_msj(self, msj):
        decrypted = decrypt(self.__priv_key, msj)
        return decrypted

    def __codificar64(self, msj):
        msj_codificado = base64.b64encode(msj.encode('utf-8'))
        return msj_codificado

    def decodificar64(self, msj):
        msj_decodificado = base64.b64decode(msj).decode('utf-8')
        return msj_decodificado

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
        descifrado = self.descifrar_msj(msj)
        decodificado = self.decodificar64(descifrado)
        self.almacenar_msj(decodificado)
