import cv2
import mediapipe as mp
import numpy as np
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def main():
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            landmarks = results.pose_landmarks.landmark

            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y ]

            shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            left_distance = distance(nose, shoulder_left)
            right_distance = distance(nose, shoulder_right)

            if left_distance > right_distance:
                status = "RIGHT"
            if left_distance < right_distance:
                status = "LEFT"
            if left_distance == right_distance:
                status = "OK"

            cv2.putText(image, "Status:", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, status, (150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))

            cv2.imshow("S3 Project", image)

            if cv2.waitKey(10) & 0xff == ord('q'):  # q to close window
                break

        cap.release()
        cv2.destroyAllWindows()

def distance(x, y):
    x = np.array(x)
    y = np.array(y)

    distance = math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

    return distance

def test():
    print("Hello")

if __name__ == '__main__':
   main()