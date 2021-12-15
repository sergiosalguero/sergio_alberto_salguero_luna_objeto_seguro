#   Sergio Alberto Salguero Luna
#   Proyecto Final

from objeto_seguro_final import ObjetoSeguro

if __name__ == '__main__':
    # Instancia de la clase ObjetoSeguro
    bob = ObjetoSeguro('Beto')
    bob.cliente()
    # Realizar una consulta
    consulta = bob.consultar_msj(bob.gen_id())
    print(consulta)
