import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

def count(list):
    cnt= 0
    thresh = (list.landmark[0].y*100-list.landmark[9].y*100)/2
    if (list.landmark[5].y*100-list.landmark[8].y*100)>thresh:
        cnt+=1
    
    if (list.landmark[9].y*100-list.landmark[12].y*100)>thresh:
        cnt+=1
        
    if (list.landmark[13].y*100-list.landmark[16].y*100)>thresh:
        cnt+=1
        
    if (list.landmark[17].y*100-list.landmark[20].y*100)>thresh:
        cnt+=1
        
    if (list.landmark[5].y*100-list.landmark[4].y*100)>3:
        cnt+=1
        
    return cnt
cap= cv2.VideoCapture(0)

drawings = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_objects=hands.Hands(max_num_hands=1)
start_init = False
prev=-1

while True:
    end_time = time.time()
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    res = hand_objects.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    
    
    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]
        
        cnt = count(hand_keyPoints)
        
        if not (prev==cnt):
            if not (start_init):
                start_time=time.time()
                start_init = True
            
            elif(end_time-start_time)>0.2:
                
                if (cnt==1):
                    pyautogui.press("right")
                    
                elif (cnt==2):
                    pyautogui.press("left")
                    
                elif (cnt==3):
                    pyautogui.press("up")
                    
                elif (cnt==4):
                    pyautogui.press("down")
                    
                elif (cnt==5):
                    pyautogui.press("space")                
            
        prev = cnt
        drawings.draw_landmarks(frame,res.multi_hand_landmarks[0],hands.HAND_CONNECTIONS)
    cv2.imshow("window",frame)
    
    if cv2.waitKey(1)==27:    
        cv2.destroyAllWindows()
        cap.release()    
        break