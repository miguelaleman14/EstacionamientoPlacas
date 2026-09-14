
from models.ticket import Ticket 
class EstacionamientoService:
    def __init__(self, lugares):
        self.lugares = lugares
        self.tickets = []
        self.contador_tickets = 1

    def registrar_entradas(self, vehiculo):
        for lugar in self.lugares:
            if not lugar.ocupado:
                lugar.ocupar()
                nuevo_ticket = Ticket(self.contador_tickets, vehiculo, lugar)
                self.tickets.append(nuevo_ticket)
                self.contador_tickets += 1
                return nuevo_ticket
        return None

    def registrar_salida(self, placa: str):
        for ticket in self.tickets:
            if ticket.vehiculo and ticket.vehiculo.placa == placa:
                if ticket.lugar:
                    ticket.lugar.liberar()
                ticket.costo = 20.0
                return ticket
        return None