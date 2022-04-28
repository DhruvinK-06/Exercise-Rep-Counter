from GetPose import *
import mediapipe as mp
mp_pose = mp.solutions.pose


def return_cords(file):

    pose_image = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    global shape
    # Capture the video
    vid = cv2.VideoCapture(file)
    vals = list()
    # process all the frames
    while vid.isOpened():
        succ, img = vid.read()
        # if the frame is successfully found then proceed or else break
        if succ:
            shape = img.shape
            # returns the landmarks for a given frame
            result = detectPose(img, pose_image)
            part = None
            if result.pose_landmarks:
                coords = result.pose_landmarks.ListFields()[0][1]
                vals.append(coords)
        else:
            break
    return vals