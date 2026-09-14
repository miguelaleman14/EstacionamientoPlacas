from fastapi import FastAPI
from services.estacionamiento_service import EstacionamientoService
from models.vehiculo import Vehiculo
from models.lugar import Lugar

app = FastAPI()

lugares_demo = [Lugar(1), Lugar(2), Lugar(3)]
estacionamiento = EstacionamientoService(lugares=lugares_demo)

@app.post("/api/entrada")
def registrar_entrada_desde_camara(placa: str):
    nuevo_vehiculo = Vehiculo(placa, "Automovil")
    ticket = estacionamiento.registrar_entradas(nuevo_vehiculo)
    
    if ticket:
        return {"mensaje": "Acceso permitido", "ticket": ticket.numero, "lugar": ticket.lugar.numero}
    else:
        return {"error": "Estacionamiento lleno"}

@app.post("/api/salida")
def registrar_salida_desde_camara(placa: str):
    ticket = estacionamiento.registrar_salida(placa)
    
    if ticket:
        return {
            "mensaje": "Salida procesada, abriendo pluma", 
            "placa": placa, 
            "total_a_pagar": f"${ticket.costo}"
        }
    else:
        return {"error": "Vehículo no encontrado"}