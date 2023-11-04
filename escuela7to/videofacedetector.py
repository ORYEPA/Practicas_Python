import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camara = cv2.VideoCapture(0)

while True:
    ret, fram = camara.read()
    gray = cv2.cvtColor(fram, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.circle(fram, (x + w // 2, y + h // 2), int(0.6 * w), (0, 255, 0), 2)
    cv2.imshow('Detección de Rostros en Tiempo Real', fram)
    

camara.release()
cv2.destroyAllWindows()