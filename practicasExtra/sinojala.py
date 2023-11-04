import numpy as np
import cv2

def get_image_contours(filename):
    # Read the image
    img = cv2.imread(filename, 0)
    
    # Define the Connect 4 algorithm
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
    
    # Apply the Connect 4 algorithm and obtain the labeled image
    labeled = connect4(img)
    
    # Obtain the contours of the labeled image
    contours, hierarchy = cv2.findContours(labeled.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Return the contours
    return contours
