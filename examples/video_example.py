import os
from os.path import basename, splitext
import numpy as np
import time
import cv2
import sys
from utils.video_helper import save_video_caps
from utils.tvd import TotalVariationDenoising
from utils.seams import print_seams
from seammerging.video import VideoSeamMergingWithDecomposition

# Fix path name relationships when this script is running from a different folder
if __name__ == '__main__':
  if os.path.dirname(__file__) != '':
    os.chdir(os.path.dirname(__file__))


def draw_flow(img, flow, step=8):
  h, w = img.shape[:2]
  y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1)
  fx, fy = flow[y, x].T

  # create line endpoints
  lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
  lines = np.int32(lines)

  # create image and draw
  vis = np.copy(img)
  # vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
  for (x1, y1), (x2, y2) in lines:
    cv2.line(vis, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
  return vis


iterTV = 80
alpha = 0.5
betaEn = 0.5

deleteNumberW = 30
counting_frames = 59
save_importance = False
save_vectors = True
global_vector = False
filename = '../assets/car.m4v'
suffix = ''
for i in xrange(len(sys.argv) - 1):
  if sys.argv[i] == '-s':
    deleteNumberW = int(sys.argv[i + 1])
  elif sys.argv[i] == '-f':
    counting_frames = int(sys.argv[i + 1])
  elif sys.argv[i] == '-i':
    save_importance = bool(sys.argv[i + 1])
  elif sys.argv[i] == '-v':
    save_vectors = bool(sys.argv[i + 1])
  elif sys.argv[i] == '-g':
    global_vector = bool(sys.argv[i + 1])

makeNewDecData = False

debug = False
saveBMP = True

cap = cv2.VideoCapture(filename)
size = '_reduce' if deleteNumberW < 0 else '_enlarge'
size += str(-deleteNumberW) if deleteNumberW < 0 else str(deleteNumberW)

name = splitext(basename(filename))[0] + suffix + '_' + size + '_' + str(int(time.time()))

frames_count, fps, width, height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT), cap.get(cv2.cv.CV_CAP_PROP_FPS), cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH), cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

frames_count = frames_count if counting_frames is None else counting_frames

importance = np.empty((frames_count, height, width))
structureImage = np.empty((frames_count, height, width))
vectors = np.empty((frames_count, height, width, 2))
video = np.empty((frames_count, height, width, 3))

i = 0
while cap.isOpened() and i < frames_count:
  ret, X = cap.read()
  if not ret:
    break
  y = cv2.cvtColor(X, cv2.COLOR_BGR2YCR_CB)
  y = y.astype(np.float64)
  structureImage[i] = TotalVariationDenoising(y[:, :, 0], iterTV).generate()

  # Motion vector frame per frame (filtered with medianBlur to delete salt and pepper noise)
  if i > 0:
    vectors[i - 1] = cv2.calcOpticalFlowFarneback(structureImage[i - 1], structureImage[i], 0.5, 1, 3, 15, 3, 5, 1)

  kernel = np.array([[0, 0, 0],
                     [1, 0, -1],
                     [0, 0, 0]])
  importance[i] = np.abs(cv2.filter2D(y[:, :, 0], -1, kernel, borderType=cv2.BORDER_REPLICATE)) + np.abs(cv2.filter2D(y[:, :, 0], -1, kernel.T, borderType=cv2.BORDER_REPLICATE))
  video[i] = X
  i += 1

if save_importance:
  imp = np.clip(importance, 0, 255).astype(np.uint8)
  imp = np.expand_dims(imp, axis=3)[:, :, :, [0, 0, 0]]
  save_video_caps(imp, './results/' + name + '_importance_')

videomethod = VideoSeamMergingWithDecomposition(video, structureImage, importance, vectors, deleteNumberW, alpha, betaEn)
result = videomethod.generate()
seams = videomethod.seams

# Saving seams frame images
# A = print_seams(video, result, seams, deleteNumberW)
# A = np.clip(A, 0, 255).astype(np.uint8)
flow = np.zeros(video.shape)
for i, image, vector in zip(xrange(video.shape[0]), video, vectors):
  flow[i] = draw_flow(image, vector)
result = np.clip(result, 0, 255).astype(np.uint8)
save_video_caps(result, './results/' + name + '_')
save_video_caps(flow, './results/' + name + '_vectors_')
# save_video_caps(A, './results/' + name + '_seams_')
cap.release()
print 'Finished file: ' + basename(filename)
