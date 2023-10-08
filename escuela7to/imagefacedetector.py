import cv2
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt



def detect_faces():
    file_path = filedialog.askopenfilename()  
    if not file_path:
        return

    foto = cv2.imread(file_path)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    fotoGS = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(fotoGS, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.circle(foto, (x + w // 2, y + h // 2), int(0.6 * w), (0, 0, 255), 2)

    plt.imshow(cv2.cvtColor(foto, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    print(f"Número de caras detectadas: {len(faces)}")


def open_file_dialog():
    file_path = filedialog.askopenfilename()
    print(file_path)
    file=str(file_path)
    procesado_principal(file)
root = tk.Tk()

button = tk.Button(root, text="Open File", command=detect_faces)
button.pack()

root.mainloop()