import cv2
import pyttsx3


import cv2
import os

# Absolutní cesta
cascade_path = "C:/Users/Pycham/mobilni_aplikace/data/haarcascade_frontalface_default3.xml"
print(f"Zkouším načíst: {cascade_path}")
print(f"Soubor existuje: {os.path.exists(cascade_path)}")

face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print("❌ Soubor se NEpodařilo načíst. Pravděpodobně je poškozený nebo špatně uložený.")
else:
    print("✅ Soubor byl načten správně!")


engine = pyttsx3.init()
cascade_path = "C:\\Users\\Petřík\\Desktop\\Kurz_python\\mobilni_aplikace\\data\\haarcascade_frontalface_default1.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    print("❌ Soubor se nepodařilo načíst. Zkontroluj cestu!")
    exit()
cap = cv2.VideoCapture(0)

recognized = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0 and not recognized:
        print("Obličej detekován, Petr se přihlásil.")
        engine.say("Petr se přihlásil")
        engine.runAndWait()
        recognized = True

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Petr?", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Přihlašování", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()