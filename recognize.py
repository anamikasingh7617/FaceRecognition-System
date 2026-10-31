import cv2
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

xml_path = os.path.join(
    BASE_DIR, "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(xml_path)

if face_cascade.empty():
    print("XML file not found!")
    exit()

faces = []
labels = []
names = []

for name in os.listdir(DATASET_DIR):
    person_path = os.path.join(DATASET_DIR, name)

    if not os.path.isdir(person_path):
        continue

    label = len(names)
    names.append(name)

    for file in os.listdir(person_path):
        image_path = os.path.join(person_path, file)

        img = cv2.imread(image_path, 0)

        if img is not None:
            img = cv2.resize(img, (200, 200))
            faces.append(img)
            labels.append(label)

if len(faces) == 0:
    print("No registered faces found!")
    exit()

if not hasattr(cv2, "face"):
    print("OpenCV face module is unavailable!")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera not available!")
    exit()

print("Face Recognition Started. Press Q to exit.")

while True:
    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected = face_cascade.detectMultiScale(
        gray, 1.3, 5
    )

    for (x, y, w, h) in detected:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)
        print("Detected:", names[label], "Confidence:", confidence)
        if confidence < 50:
            name = names[label]
        else:
            name = "Unknown"

        cv2.rectangle(
            frame, (x, y), (x+w, y+h), (0, 255, 0), 2
        )

        cv2.putText(
            frame, name, (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9, (0, 255, 0), 2
        )

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()