import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3
import time

# Inisialisasi TTS
engine = pyttsx3.init()

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=2)

# Cooldown suara
last_speech_time = 0
cooldown = 2

print("📷 Kamera aktif. Coba gesture + lihat garis merah di tangan...")

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            handType = hand["type"]
            fingers = detector.fingersUp(hand)
            lmList = hand["lmList"]  # daftar koordinat landmark tangan

            # 🔹 Efek "garis darah" → gambar garis merah antar sendi tangan
            for i in range(len(lmList) - 1):
                x1, y1 = lmList[i][0:2]
                x2, y2 = lmList[i+1][0:2]
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # garis merah

            # 🔹 Gesture suara (dengan cooldown biar ga spam)
            if time.time() - last_speech_time > cooldown:
                if handType == "Right" and fingers == [0,1,0,0,0]:
                    print("👉 Gesture terdeteksi → Bicara: 'Nama saya'")
                    engine.say("Nama saya")
                    engine.runAndWait()
                    last_speech_time = time.time()

                elif handType == "Left" and fingers == [1,1,1,1,1]:
                    print("🤲 Gesture terdeteksi → Bicara: 'Bara'")
                    engine.say("Bara")
                    engine.runAndWait()
                    last_speech_time = time.time()

                elif handType == "Right" and fingers == [0,1,1,0,0]:
                    print("✌️ Gesture terdeteksi → Bicara: 'Sampai jumpa'")
                    engine.say("Sampai jumpa")
                    engine.runAndWait()
                    last_speech_time = time.time()

    cv2.imshow("Gesture + Efek Darah", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
