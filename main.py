import time
import pyautogui as pag
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]  # tips of all the fingers

time.sleep(5)
cap = cv2.VideoCapture(0)
prev_key = 'nothing'
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        result = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []
        # Handconnections help use connect my hands
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                if result.multi_hand_landmarks:
                    myHands = result.multi_hand_landmarks[0]
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        lmList.append([id, cx, cy])
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hand.HAND_CONNECTIONS)
        fingers = []
        if len(lmList) != 0:
            # when the tip is below the pip
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)
            # print(total)
            if (total == 5):
                cv2.putText(image, 'Right Direction', (20, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(image, 'Accelerator', (420, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)

                if (prev_key == "left"):
                    pag.keyUp('left')
                    prev_key = "right"

                pag.keyDown('right')
                prev_key = "right"
            if total == 0:
                cv2.putText(image, 'Left Direction', (20, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(image, 'Reverse', (420, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)

                if prev_key == 'right':
                    pag.keyUp('right')
                    prev_key = 'left'

                pag.keyDown('left')
                prev_key = 'left'

            if (0 < total < 5):
                cv2.putText(image, 'Nothing', (20, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(image, 'No Action', (420, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1,
                            cv2.LINE_AA)

                if prev_key == 'right':
                    pag.keyUp('right')
                    prev_key = 'nothing'

                if prev_key == 'left':
                    pag.keyUp('left')
                    prev_key = 'nothing'
            if total == 2:
                pag.leftClick()

            """
            if (lmList[8][2]<lmList[6][2]):
                print("open")
            else:
                print("close")
            """
        cv2.imshow("frame", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
