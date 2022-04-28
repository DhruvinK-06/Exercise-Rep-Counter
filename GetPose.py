import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose
pose_image = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
def detectPose(image_pose, pose):
    image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
    result = pose.process(image_in_RGB)
    return result


