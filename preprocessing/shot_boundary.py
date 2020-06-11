import cv2
import numpy as np
import matplotlib.pyplot as plt

vidcap = cv2.VideoCapture("../data_raw/videos/2018-03-02_P11.mp4")

fps = int(vidcap.get(cv2.CAP_PROP_FPS))
frameCount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# print(fps)


previous_histogram = None


count = 0
success = True
frame_index = 0
time_stamps_chi = []
all_chi = [0]
def extract_timestamp(prev_hist, cur_hist, threshold, method, frame_numb):
    score = cv2.compareHist(prev_hist, cur_hist, method)

    threshold_asses = False
    timestamp = None
    if method is cv2.HISTCMP_CHISQR:
        threshold_asses = score > threshold
        timestamp = int(frame_numb/fps)

    if method is cv2.HISTCMP_CORREL:
        threshold_asses = score < threshold
        timestamp = int(frame_numb / fps)

    return threshold_asses, timestamp , score


while success:
    frame_index += 1

    success, image = vidcap.read()
    if count!=fps:
        count += 1
        continue
    count = 0

    if int(frame_index/fps) == 7000:
        break

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

    if previous_histogram is None:
        previous_histogram = histogram
        count += 1
        continue


    assesment_chi, time_chi, chi_score = extract_timestamp(previous_histogram, histogram, 50000000, cv2.HISTCMP_CHISQR, frame_index)
    all_chi.append(chi_score)
    if assesment_chi:
        time_stamps_chi.append(time_chi)

    previous_histogram = histogram

    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        break




# Frame time: 4760
# Chi: 67770651.16470273
# Correlation: 0.2324451849760124
