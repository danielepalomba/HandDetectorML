import cv2
import mediapipe as mp
import csv

my_file = 'your-file.csv'

# Inizializza mediapipe hands module
mphands = mp.solutions.hands
mpdrawing = mp.solutions.drawing_utils

# Inizializza video capture dalla webcam (0 indica la webcam predefinita)
vidcap = cv2.VideoCapture(0)

# Inizializza hand tracking
with mphands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    # Aggiungi i nomi delle colonne al file CSV
    with open(my_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Scrivi i nomi delle colonne
        header = ['Landmark_' + str(i) for i in range(1, 64)]
        writer.writerow(header)

    while True:
        ret, frame = vidcap.read()
        if not ret:
            break

        # Converti l'immagine BGR in RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processa il frame per il tracciamento delle mani
        processFrames = hands.process(rgb_frame)

        # Disegna i landmark sul frame
        if processFrames.multi_hand_landmarks:
            for lm in processFrames.multi_hand_landmarks:
                mpdrawing.draw_landmarks(frame, lm, mphands.HAND_CONNECTIONS)

                # Ottieni le coordinate dei landmark
                landmarks = []
                for point in lm.landmark:
                    landmarks.extend([point.x, point.y, point.z])

                # Salva le coordinate nel file CSV
                with open(my_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(landmarks)

        # Visualizza il frame
        cv2.imshow('Hand Tracking', frame)

        # Esci dal loop premendo 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Rilascia la cattura video e chiudi le finestre
vidcap.release()
cv2.destroyAllWindows()
