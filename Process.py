from GetPoseVideo import *
import os
import numpy as np


# resolution of video
shape = (640, 854, 3)

class Process:
    global shape
    # Find euclidian distance between 2 points
    def dist(self, x1, y1, x2, y2):
        distance = ((( (x2 - x1 )**2 ) + ( (y2-y1)**2) )**0.5)
        return distance

    # find the distance between all 33 landmark points and add them
    def get_dist(self, frame1, frame2, shape = shape):
        s = 0
        for i in range(len(frame1)):
            x1, y1 = frame1[i].x, frame1[i].y
            x2, y2 = frame2[i].x, frame2[i].y
            s += self.dist(x1, y1, x2, y2)
        return s

    # find the angle for the knee bend
    def get_angle(self, frame, shape = shape):
        
        (h, w, c) = shape
        
        # the leg which is more visibile is the leg in front of the camera
        if frame[25].visibility > frame[26].visibility:
            xhip, yhip = int(frame[23].x * w), int(frame[23].y * h)
            xknee, yknee = int(frame[25].x * w), int(frame[25].y * h)
        else:
            xhip, yhip = int(frame[24].x * w), int(frame[24].y * h)
            xknee, yknee = int(frame[26].x * w), int(frame[26].y * h)

 
        # Calculate vectors and then find the angle between them
        x1, y1 = 0.0000000000001, yhip - yknee
        x2, y2 = xhip - xknee, yhip - yknee
        
        if y1 == 0:
            return 180
            
        v1 = [x1, y1]; v2 = [x2, y2]
        
        u1 = v1 / np.linalg.norm(v1)
        u2 = v2 / np.linalg.norm(v2)
        dp = np.dot(u1, u2)
        angle = np.rad2deg(np.arccos(dp))
        
        return int(angle * 2)

        
    def get_dummy_angle(self, coords):
        # get number of landmarks for  all the frames in the video
        n = len(coords)
        # mask for dummy frames
        dum = np.zeros(n)
        # mask for new video. 1 means that a new video starts from this frame
        new_vid = np.zeros(n)
        # 1st frame is always a new video
        new_vid[0] = 1
        # mask to check if a human is present in a video. 1 means that  a human is present
        human = np.ones(n)
        # angle list to find the knee angle for all the frames in the video. None for the frames where there is no human
        angle = list()
        for frame in coords:
            if frame:
                ang = self.get_angle(frame)
                angle.append(ang)
            else:
                angle.append(None)
            
        for i in range(n):
            if i == 0:
                i += 1
            if angle[i]:
                # if the previous frame contains a human and if it is not a dummy frame
                if human[i-1] and not dum[i - 1]:
                    # if the differnece between the knee angle and distance between the coordinates in the previous frame
                    # are greater than the below threshold values, then there are 2 possiblilities. Either the video has changed 
                    # or that the current frame is a dummy frame
                    if abs(angle[i] - angle[i-1]) > 20 and self.get_dist(coords[i], coords[i - 1]) > 0.3:
                        coord = coords[i-1]
                        ang = angle[i-1]
                        x = i + 1
                        f = 0
                        # check next 40 frames. If a similar frame to the last frame is found then the current frame is a dummy frame
                        # otherwise the video has changed
                        while(x < i + 40 and i + 40 < n):
                            if angle[x]:
                                if self.get_dist(coords[x], coord) <= 0.3 and abs(angle[x] - ang) <= 20:
                                    # if a similar frame is found then all the previous frames until the current frames are dummy
                                    while(i < x):
                                        dum[i] = 1
                                        i += 1
                                    i = x 
                                    f = 1
                                    break
                            x += 1
                        if f == 1:
                            continue
                        new_vid[i] = 1 
                # if the previous frame is dummy frame and the current is similar to previous frame 
                # then the current frame is also a dummy frame
                elif dum[i-1]:
                    if self.get_dist(coords[i], coords[i - 1]) <= 0.3 and abs(angle[i] - angle[i - 1]) < 20:
                        dum[i] = 1
            else:
                human[i] = 0
                    
        return dum, human, new_vid, angle