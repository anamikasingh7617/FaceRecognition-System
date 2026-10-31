import cv2
import os

name = input("Enter your name: ").strip()

if not name:
    print("Name cannot be empty!")
    exit()

path = os.path.join("dataset", name)
os.makedirs(path, exist_ok=True)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera not available!")
    exit()

xml_path = os.path.join(
    os.path.dirname(__file__),
    "haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(xml_path)

if face_cascade.empty():
    print("Error: XML file not loaded!")
    exit()


count = 0

while count < 50:
    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        count += 1
        cv2.imwrite(os.path.join(path, f"{count}.jpg"), face)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.putText(frame, f"Samples: {count}/50",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Face Registration", frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

print("Registration completed!")