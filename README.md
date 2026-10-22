Sistema Automatizado de Control de Estacionamiento (ALPR)Sistema automatizado de control de acceso vehicular para el nuevo estadio de fútbol de TecMilenio. Este proyecto utiliza visión artificial (OCR y Haar Cascades) para identificar automáticamente las placas de los vehículos, gestionando las entradas, salidas, cálculo de tarifas y asignación de lugares a través de una API REST.✨ Características Principales📷 Reconocimiento Automático de Placas (ALPR): Captura de video en tiempo real, detección de placas y extracción de texto mediante OCR.🅿️ Gestión de Espacios: Verificación de disponibilidad y asignación automática de lugares libres al momento de la entrada.🎫 Generación de Tickets: Creación automática de tickets digitales con número consecutivo, vehículo, lugar asignado y hora de entrada.💰 Cálculo de Tarifas: Cálculo automático del costo del servicio basado en el tiempo transcurrido al procesar la salida.🔌 API RESTful: Endpoints independientes para el registro de entradas y salidas, documentados automáticamente con Swagger UI.🏗️ Arquitectura del SistemaEl sistema está diseñado bajo una arquitectura orientada a microservicios y Edge Computing:Capa Edge (Cámaras): Dispositivos que ejecutan el cliente (camara.py) con OpenCV para el procesamiento de imágenes en el borde.API Gateway: Construido con FastAPI (main.py), sirve como punto de entrada y enrutador.Servicios de Negocio: Lógica central para la gestión de vehículos, lugares y tickets (estacionamiento_service.py).(Propuesto) Autenticación y Auditoría: Gestión de roles (ADMIN/OPERADOR) y registro de bitácoras.🚀 Instalación y UsoPrerrequisitosPython 3.8 o superior.Cámara web funcional para el cliente ALPR.Configuración del EntornoClona el repositorio:git clone https://github.com/miguelaleman14/EstacionamientoPlacas.git
cd EstacionamientoPlacas
Crea y activa un entorno virtual (recomendado):python -m venv .venv
source .venv/bin/activate  # En Windows usa: .venv\Scripts\activate
Instala las dependencias:pip install fastapi uvicorn opencv-python requests
(Asegúrate de instalar tu motor OCR preferido, como pytesseract o easyocr, si el script de cámara lo requiere).Ejecución del Servidor (API)Inicia el servidor backend usando Uvicorn:uvicorn main:app --reload
La API estará disponible en http://127.0.0.1:8000.
Puedes ver la documentación interactiva (Swagger) en http://127.0.0.1:8000/docs.Ejecución del Cliente (Cámara)En otra terminal, ejecuta el script de reconocimiento facial:python camara.py
📡 Endpoints de la APIMétodoEndpointDescripciónPOST/api/entradaRegistra la entrada, asigna lugar y crea ticket. (Requiere placa como query param)POST/api/salidaProcesa la salida, libera el lugar y calcula el costo. (Requiere placa como query param)Ejemplo de petición de salida:curl -X 'POST' 'http://127.0.0.1:8000/api/salida?placa=ABC123'
📂 Estructura del Proyecto EstacionamientoPlacas
 ┣ 📂 models/             
 ┃ ┣ 📜 lugar.py          
 ┃ ┣ 📜 ticket.py        
 ┃ ┗ 📜 vehiculo.py       
 ┣ 📂 services/           
 ┃ ┗ 📜 estacionamiento_service.py 
 ┣ 📂 tests/              
 ┣ 📜 main.py             
 ┣ 📜 camara.py          
 ┗ 📜 README.md
