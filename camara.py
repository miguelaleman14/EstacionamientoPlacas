import cv2
import requests
import time
import easyocr
import re

print("Cargando modelo de OCR en memoria...")
# Cargamos EasyOCR una sola vez al inicio
reader = easyocr.Reader(['en'], gpu=False)

API_URL_ENTRADA = "http://127.0.0.1:8000/api/entrada"

camara = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Variables de control de tiempo y estado
ultimo_escaneo = 0
INTERVALO_ESCANEO = 4.0  # Segundos de espera entre lecturas OCR para no congelar la cámara
texto_pantalla = ""
tiempo_texto = 0

print("Iniciando cámara fluida... Presiona 'q' para salir.")

def limpiar_texto_placa(texto_raw):
    """Filtra y deja únicamente caracteres alfanuméricos válidos"""
    return re.sub(r'[^A-Z0-9]', '', texto_raw.upper())

while True:
    ret, frame = camara.read()
    if not ret:
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detección de placas con filtro de tamaño mínimo para evitar falsos rectángulos
    placas = cascade.detectMultiScale(
        gris, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(100, 40)  # Evita recortar cuadros diminutos que traban el OCR
    )

    tiempo_actual = time.time()

    for (x, y, w, h) in placas:
        # Dibujar rectángulo alrededor de la placa
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Solo procesar OCR si ha transcurrido el intervalo de espera
        if tiempo_actual - ultimo_escaneo > INTERVALO_ESCANEO:
            roi_placa = gris[y:y+h, x:x+w]
            
            if roi_placa.size > 0:
                print("\n[OCR] Analizando encuadre de placa...")
                
                # Ejecutar OCR sobre la región de interés recortada
                resultados = reader.readtext(roi_placa)
                
                texto_raw = ""
                for res in resultados:
                    texto_raw += res[1] + " "
                
                placa_detectada = limpiar_texto_placa(texto_raw)
                
                # Validar longitud mínima de placa (3 a 8 caracteres alfanuméricos)
                if 3 <= len(placa_detectada) <= 8:
                    print(f"[OCR ÉXITO] Placa leída: {placa_detectada}")
                    texto_pantalla = f"Placa: {placa_detectada}"
                    tiempo_texto = tiempo_actual
                    
                    # Enviar petición al servidor FastAPI
                    try:
                        respuesta = requests.post(f"{API_URL_ENTRADA}?placa={placa_detectada}")
                        datos = respuesta.json()
                        print(f"[SERVIDOR RESPUESTA]: {datos}")
                    except requests.exceptions.ConnectionError:
                        print("[ERROR] No se pudo conectar a la API.")
                    
                    # Actualizar tiempo del último escaneo exitoso
                    ultimo_escaneo = tiempo_actual
                else:
                    print(f"[OCR DESCARTADO] Texto no válido: '{texto_raw.strip()}'")
                    # Evitar reintentar inmediatamente si el encuadre fue fallido
                    ultimo_escaneo = tiempo_actual - 2.5 

    # Mantener el texto visual en pantalla durante 3 segundos
    if tiempo_actual - tiempo_texto < 3.0 and texto_pantalla:
        cv2.putText(frame, texto_pantalla, (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    # Mostrar la transmisión de video fluida
    cv2.imshow('Reconocimiento ALPR - TecMilenio', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()