import datetime

class Ticket:
    def __init__(self, numero: int, vehiculo, lugar):
        self.numero = numero
        self.vehiculo = vehiculo
        self.lugar = lugar
        self.costo = 0.0