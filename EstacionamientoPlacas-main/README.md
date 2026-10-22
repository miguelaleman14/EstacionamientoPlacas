# Sistema Automatizado de Control de Estacionamiento (ALPR)

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-ALPR-red.svg)

Sistema automatizado de control de acceso vehicular para el nuevo estadio de fútbol de **Universidad TecMilenio**. Este proyecto utiliza visión artificial (OCR y clasificadores de cascada de Haar) para identificar automáticamente las placas de los vehículos, gestionando las entradas, salidas, cálculo de tarifas y asignación de lugares a través de una API REST.

---

##  Características Principales

*    **Reconocimiento Automático de Placas (ALPR):** Captura de video en tiempo real, detección de placas y extracción de texto mediante OCR.
*    **Gestión de Espacios:** Verificación de disponibilidad y asignación automática de lugares libres al momento de la entrada.
*    **Generación de Tickets:** Creación automática de tickets digitales con número consecutivo, vehículo, lugar asignado y hora de entrada.
*   **Cálculo de Tarifas:** Cálculo automático del costo del servicio basado en el tiempo transcurrido al procesar la salida.
*   **API RESTful:** Endpoints independientes para el registro de entradas y salidas, documentados automáticamente con Swagger UI.

---

## Arquitectura del Sistema

El sistema está diseñado bajo una propuesta de arquitectura orientada a microservicios y Edge Computing:

*   **Capa Edge (Cámaras):** Dispositivos que ejecutan el cliente (`camara.py`) con OpenCV para el procesamiento de imágenes en el borde.
*   **API Gateway:** Construido con FastAPI (`main.py`), sirve como punto de entrada y enrutador.
*   **Servicios de Negocio:** Lógica central para la gestión de vehículos, lugares y tickets (`estacionamiento_service.py`).
*   **(Propuesto) Autenticación y Auditoría:** Gestión de roles (ADMIN/OPERADOR) y registro de bitácoras.

---

## Instalación y Uso

### Prerrequisitos
*   Python 3.8 o superior (Desarrollado con Python 3.14).
*   Cámara web funcional para el cliente ALPR.

### Configuración del Entorno

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/miguelaleman14/EstacionamientoPlacas.git
   cd EstacionamientoPlacas
   ```

2. **Crea y activa un entorno virtual (recomendado):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa: .venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install fastapi uvicorn opencv-python requests
   ```
   *(Asegúrate de instalar tu motor OCR preferido, como pytesseract o easyocr, según lo requiera tu entorno).*

### Ejecución

**1. Iniciar el Servidor (API Gateway)**
Abre una terminal e inicia el backend usando Uvicorn:
```bash
uvicorn main:app --reload
```
*La API estará disponible en http://127.0.0.1:8000.*
*Puedes ver la documentación interactiva (Swagger UI) en http://127.0.0.1:8000/docs.*

**2. Ejecutar el Cliente (Cámara)**
En otra terminal, ejecuta el script de reconocimiento de placas:
```bash
python camara.py
```

---

##  Endpoints de la API

| Método | Endpoint | Descripción | Parámetros |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/entrada` | Registra la entrada, asigna lugar y crea ticket. | `placa` (query param) |
| `POST` | `/api/salida` | Procesa la salida, libera el lugar y calcula el costo. | `placa` (query param) |

**Ejemplo de petición de salida (cURL):**
```bash
curl -X 'POST' 'http://127.0.0.1:8000/api/salida?placa=ABC123' -H 'accept: application/json'
```

---

## 📂 Estructura del Proyecto

```text
EstacionamientoPlacas/
├── models/
│   ├── lugar.py
│   ├── ticket.py
│   └── vehiculo.py
├── services/
│   └── estacionamiento_service.py
├── tests/
│   └── test_estacionamiento.py
├── camara.py
├── main.py
└── README.md
```

---
