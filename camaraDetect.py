import cv2

# Intenta abrir la cámara 0 (la principal)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara 😢")
else:
    print("¡Cámara detectada! 🎥✨")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el frame 😕")
            break

        cv2.imshow("Cámara en vivo 🖼️", frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
