import cv2
import mediapipe as mp
import csv

my_file = 'your-file.csv'

# mediapipe hands module
mphands = mp.solutions.hands
mpdrawing = mp.solutions.drawing_utils

# video capture
vidcap = cv2.VideoCapture(0)

# hand tracking
with mphands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    # add columns name to CSV file
    with open(my_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # write columns name
        header = ['Landmark_' + str(i) for i in range(1, 64)]
        writer.writerow(header)

    while True:
        ret, frame = vidcap.read()
        if not ret:
            break

        # from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        processFrames = hands.process(rgb_frame)

        # print landmarks on frame
        if processFrames.multi_hand_landmarks:
            for lm in processFrames.multi_hand_landmarks:
                mpdrawing.draw_landmarks(frame, lm, mphands.HAND_CONNECTIONS)

                # landmarks coordinates
                landmarks = []
                for point in lm.landmark:
                    landmarks.extend([point.x, point.y, point.z])

                # save coordinate into CSV file
                with open(my_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(landmarks)

        # show frame
        cv2.imshow('Hand Tracking', frame)

        # Push 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# release resources
vidcap.release()
cv2.destroyAllWindows()
