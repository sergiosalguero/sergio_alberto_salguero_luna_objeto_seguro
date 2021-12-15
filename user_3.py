#   Sergio Alberto Salguero Luna
#   Proyecto Final

from objeto_seguro_final import ObjetoSeguro

if __name__ == '__main__':
    # Instancia de la clase ObjetoSeguro
    charly = ObjetoSeguro('Carlos')
    charly.cliente()
    # Realizar una consulta
    consulta = charly.consultar_msj(charly.gen_id())
    print(consulta)
