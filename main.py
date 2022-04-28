from GenVideo import generateVideo
from Process import *
from GetPoseVideo import return_cords
import os

file = os.path.join(os.path.dirname(__file__), 'KneeBendVideo.mp4')
vals = return_cords(file = file)

prc = Process()
dummy, human, new_vid, angle = prc.get_dummy_angle(vals)

generateVideo(file, dummy, angle, new_vid, human, shape)