from Process import *
from GetPoseVideo import return_cords
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def generateVideo(file, dummy, angle, new_video, human, shape):
    vid = cv2.VideoCapture(file)
    n = len(angle)
    flag = np.zeros(n)
    rep_time = np.zeros(n)
    succ_rep = np.zeros(n)
    rep_count = np.zeros(n)
    stretch = np.zeros(n)
    feedback = np.zeros(n)
    for i in range(n):
        if i > 0 and not dummy[i] and angle[i] and human[i]:
            rep_count[i] = rep_count[i-1]
            if new_video[i]:
                rep_count[i-1] = 0
            
            if succ_rep[i-1] == 0:
                if angle[i] < 140 and flag[i-1] == 0:
                    flag[i] = 1
                    rep_time[i] = 1
                elif flag[i-1] == 1:
                    if angle[i] >= 140:
                        flag[i] = 0
                        rep_time[i] = 0
                        feedback[i] = 1
                        x = i + 1
                        while x < i + 60:
                            feedback[x] = 1
                            x += 1
                    else:
                        flag[i] = 1
                        rep_time[i] = rep_time[i-1] + 1
                        if rep_time[i] == 200:
                            succ_rep[i] = 1
                            rep_count[i] = rep_count[i-1] + 1
            else:
                if angle[i] <= 170:
                    stretch[i] = 1
                    succ_rep[i] = 1
                    rep_count[i] = rep_count[i-1]
                    rep_time[i] = rep_time[i-1]
                else:
                    succ_rep[i] = 0
                    rep_time[i] = 0
            
    print('Done Processing\nCreating video!')
                
    height, width, channels = shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    vpath = os.path.join(os.path.dirname(__file__), 'video.avi')
    video = cv2.VideoWriter(vpath, fourcc, 25, (width, height))
    i = 0
    while vid.isOpened():
        succ, img = vid.read()
        
        if succ:
            try:
                if dummy[i]:
                    i += 1
                    continue
            except:
                break
            if i % 1000 == 0 and i > 0:
                print('Frames processed:', i)
            
            original_image = img.copy()
            image_in_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = pose_image.process(image_in_RGB)
            # return result
            if result.pose_landmarks:    
                mp_drawing.draw_landmarks(image=original_image, landmark_list=result.pose_landmarks,
                                          connections=mp_pose.POSE_CONNECTIONS,
                                          landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                                       thickness=3, circle_radius=3),
                                          connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                                       thickness=2, circle_radius=2))
            
            cv2.rectangle(original_image, (500, 0), (850, 130) , (255,0,0), thickness = -1)
            cv2.putText(img = original_image, text = 'Reps:', org = (520, 30), fontScale = 1, 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, color = (255, 0, 255), thickness = 2)
            cv2.putText(img = original_image, text = str(int(rep_count[i])), org = (620, 30), fontScale = 1, 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, color = (255, 0, 255), thickness = 2)
            
            cv2.putText(img = original_image, text = 'Hold:', org = (670, 30), fontScale = 1, 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, color = (255, 0, 255), thickness = 2)
            cv2.putText(img = original_image, text = str(8 - int(rep_time[i]/25.0)) + ' s', org = (770, 30), fontScale = 1, 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, color = (255, 0, 255), thickness = 2)
            
            if feedback[i]:
                cv2.putText(img = original_image, text = 'Keep your knee bent!', org = (500, 100), fontScale = 1, 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, color = (255, 0, 255), thickness = 2)
            
            if stretch[i]:
                cv2.putText(img = original_image, text = 'Stretch your legs!', org = (550, 100), fontScale = 1, 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, color = (255, 0, 255), thickness = 2)
            
            video.write(original_image)                                                                         

        else:
            break
        i += 1

    video.release() 