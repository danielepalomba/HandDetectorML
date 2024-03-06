import joblib
import pandas as pd
import cv2
import mediapipe as mp

class MyModel:

    def __init__(self):
        # Carica il modello addestrato e lo scaler
        self.model = joblib.load('model.joblib')
        self.scaler = joblib.load('scaler.joblib')

    def predict(self, input_data):
        #print("Feature Names Out:", self.scaler.get_feature_names_out())
        input_df = pd.DataFrame([input_data], columns=self.scaler.get_feature_names_out())
        #print("Input DataFrame:", input_df.shape)
        normalized_data = self.scaler.transform(input_df)
        prediction = self.model.predict(normalized_data)
        return prediction

if __name__ == "__main__":
    my_model = MyModel()

    mphands = mp.solutions.hands
    mpdrawing = mp.solutions.drawing_utils

    vidcap = cv2.VideoCapture(0)

    with mphands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        prev_landmarks = None

        while True:
            ret, frame = vidcap.read()
            if not ret:
                print("Errore nella lettura del frame")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processFrames = hands.process(rgb_frame)

            if processFrames.multi_hand_landmarks:
                for lm in processFrames.multi_hand_landmarks:
                    mpdrawing.draw_landmarks(frame, lm, mphands.HAND_CONNECTIONS)

                    landmarks = []
                    for point in lm.landmark:
                        landmarks.extend([point.x, point.y, point.z])

                    if prev_landmarks is not None:
                        # Calcola la differenza tra le coordinate della mano in due frame consecutivi
                        diff = sum(abs(a - b) for a, b in zip(prev_landmarks, landmarks))

                        # Soglia per determinare se la mano è ferma
                        threshold = 10.0

                        if diff < threshold:
                            result = my_model.predict(landmarks)
                            if result in [1, 2, 3]:
                                if(result == 1):
                                    print("FORBICE")
                                if(result == 2):
                                    print("CARTA")
                                if(result == 3):
                                    print("SASSO")
                            break

                    # Aggiorna le coordinate precedenti
                    prev_landmarks = landmarks

            cv2.imshow('Hand Tracking', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    vidcap.release()
    cv2.destroyAllWindows()
