class Lugar:
    def __init__(self, numero: int):
        self.numero = numero
        self.ocupado = False

    def ocupar(self):
        self.ocupado = True

    def liberar(self):
        self.ocupado = False