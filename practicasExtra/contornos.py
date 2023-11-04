import numpy as np
import cv2
from matplotlib import pyplot as plt

def connect4(img):
    labeled = np.zeros_like(img)
    next_label = 1
    labels = {}
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x] > 0:
                neighbors = []
                if x > 0 and labeled[y][x-1] > 0:
                    neighbors.append(labeled[y][x-1])
                if x > 0 and y > 0 and labeled[y-1][x-1] > 0:
                    neighbors.append(labeled[y-1][x-1])
                if y > 0 and labeled[y-1][x] > 0:
                    neighbors.append(labeled[y-1][x])
                if x < img.shape[1]-1 and y > 0 and labeled[y-1][x+1] > 0:
                    neighbors.append(labeled[y-1][x+1])
                if len(neighbors) == 0:
                    labeled[y][x] = next_label
                    labels[next_label] = [(x,y)]
                    next_label += 1
                else:
                    neighbors.sort()
                    labeled[y][x] = neighbors[0]
                    labels[neighbors[0]].append((x,y))
                    for label in neighbors[1:]:
                        for pt in labels[label]:
                            labeled[pt[1]][pt[0]] = neighbors[0]
                        labels[neighbors[0]] += labels[label]
                        del labels[label]
    return labeled
path='D:\Practicas_Python\practicasExtra/animales.jpg'
img = cv2.imread('D:\Practicas_Python\practicasExtra/animales.jpg')
labeled = connect4(img)
contours, hierarchy = cv2.findContours(labeled.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_contours = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
cv2.drawContours(img_contours, contours, -1, (0,255,0), 2)
plt.imshow(img_contours)
plt.show()
