class Vehiculo:
    def __init__(self, placa, tipo):
        self.placa = placa
        self.tipo = tipo

    def obtener_info(self):
        return f"{self.tipo} - {self.placa}"