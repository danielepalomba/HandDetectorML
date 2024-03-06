import joblib
import pandas as pd
import cv2
import mediapipe as mp

class MyModel:

    def __init__(self):
        # load model & scaler
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

    cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Hand Tracking', 1000, 1000)

    with mphands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        prev_landmarks = None

        exit_program = False

        while not exit_program:
            ret, frame = vidcap.read()
            if not ret:
                print("Error in frame")
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
                        # calculate the difference between the hand coordinates in two consecutive frames
                        diff = sum(abs(a - b) for a, b in zip(prev_landmarks, landmarks))

                        # threshold for determining whether the hand is still
                        threshold = 0.09
                        #  If the hand is still, you get the prediction
                        if diff < threshold:
                            result = my_model.predict(landmarks)
                            if result in [1, 2, 3, 4, 5]:
                                if result == 1:
                                    print("SCISSOR")
                                if result == 2:
                                    print("PAPER")
                                if result == 3:
                                    print("ROCK")
                                if result == 4:
                                    print("Bad Hand Position!")
                                if result == 5:
                                    print("Exit OK!")
                                    exit_program = True

                    prev_landmarks = landmarks

            cv2.imshow('Hand Tracking', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit_program = True

    vidcap.release()
    cv2.destroyAllWindows()
