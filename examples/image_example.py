from image_helper import image_open, local_path
from seammerging import seam_merging
from utils.tvd import TotalVariationDenoising
from utils.seams import print_seams
import cv2
from numpy import size, float64, array, abs
import time
import os

alpha = 0.5
betaEn = 0.5

iterTV = 80
makeNewDecData = False

debug = False
saveBMP = True

file_suffix = '_small'

folder_name = 'results'

X = image_open(local_path('../assets/skyscraper.jpg'))

deleteNumberW = -1
deleteNumberH = 0

y = cv2.cvtColor(X, cv2.COLOR_BGR2YCR_CB)
y = y.astype(float64)
structureImage = TotalVariationDenoising(y[:, :, 0], iterTV).generate()  # y = to_matlab_ycbcr(y[:, :, 0])

importance = y
kernel = array([[0, 0, 0],
                [1, 0, -1],
                [0, 0, 0]
                ])

importance = abs(cv2.filter2D(y[:, :, 0], -1, kernel, borderType=cv2.BORDER_REPLICATE)) + abs(cv2.filter2D(y[:, :, 0], -1, kernel.T, borderType=cv2.BORDER_REPLICATE))

img, seams = seam_merging(X, structureImage, importance, deleteNumberW, alpha, betaEn)

seams = print_seams(X, img, seams, deleteNumberW)

size = '_reduce' if deleteNumberW < 0 else '_enlarge'
size += str(-deleteNumberW) if deleteNumberW < 0 else str(deleteNumberW)
name = 'result_' + file_suffix + '_' + size + '_' + str(int(time.time()))
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
cv2.imwrite(local_path('./' + folder_name + '/' + name + '.png'), img)
cv2.imwrite(local_path('./' + folder_name + '/' + name + '_seams_.png'), seams)
# cv2.imwrite(local_path('./' + folder_name + '/' + name + '_cartoon_.png'), structureImage)
# cv2.imwrite(local_path('./' + folder_name + '/' + name + '_importance_.png'), importance)
