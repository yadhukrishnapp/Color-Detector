import cv2
import pandas as pd

img_path = r'C:/Project/Color Detector/Images/pic4.jpg' # use any image of your choice
img = cv2.imread(img_path)
img = cv2.resize(img, (700, 500)) # for resizing the image

# global variable declaration
clicked = False

r = g = b = x_pos = y_pos = 0

# reading the csv file using pandas library and giving names to each column
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv('colors.csv', names=index, header=None)


# recognize_color function to calculate minimum distance from all colors and get the most matching color
def recognize_color(r, g, b):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(r - int(csv.loc[i,'R'])) + abs(g - int(csv.loc[i,'G'])) + abs(b - int(csv.loc[i,'B']))
        if (d <= minimum):
            minimum = d
            cname = csv.loc[i,'color_name']
    return cname


# mouseclick_function is to get x, y coordinates when mouse is double clicked
def mouseclick_function(event, x , y, flags, param): 
    if (event == cv2.EVENT_LBUTTONDBLCLK):
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('Color Detector') 
cv2.setMouseCallback('Color Detector', mouseclick_function)

while True:
    cv2.imshow('Color Detector', img)
    if (clicked):
        # cv2.rectangle(image, start point, end point, color, thickness) -1 is used to fill the entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # creating text string to display color name and RGB values
        text = recognize_color(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(image, text, start, font(0-7), fontScale, color, thickness, lineType)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # for very light colors it is recommended to display text in black color
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # when the user presses 'esc' key break the loop
    if (cv2.waitKey(20) & 0xFF == 27):
        break

cv2.destroyAllWindows()
