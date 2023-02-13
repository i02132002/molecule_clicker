import cv2
import numpy as np
import sys
import structure_factor


def mouse_callback(event, x, y, flags, params):
    # Create a named colour
    red = [0, 0, 255]
    # left-click event value is 1
    if event == 1:
        global left_clicks, scale_factor, imgS
        # store the coordinates of the left-click event
        left_clicks.append(list(np.array([x, y])/scale_factor*NM_PER_PIXEL))
        imgS = cv2.circle(imgS, (x, y), radius=1,
                          color=red, thickness=-1)
        print(left_clicks)
        cv2.imshow('image', imgS)


def update_image():
    global img, imgS, scale_factor
    filename = FILENAME
    img = cv2.imread(filename)
    imgS = cv2.resize(img, tuple(
        np.array([img.shape[0], img.shape[1]])*scale_factor))


def main():
    global FILENAME, scale_factor, NM_PER_PIXEL, left_clicks
    try:
        FILENAME = sys.argv[1]
        SCAN_SIZE = float(sys.argv[2])
        PIXELS = float(sys.argv[3])
        NM_PER_PIXEL = SCAN_SIZE / PIXELS
    except IndexError:
        print('Missing some arguments: filename, scan_size_nm, n_pixels')
        return

    left_clicks = list()
    scale_factor = 3

    update_image()
    scale_width = 1280 / imgS.shape[1]
    scale_height = 960 / imgS.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(imgS.shape[1] * scale)
    window_height = int(imgS.shape[0] * scale)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', window_width, window_height)

    # set mouse callback function for window
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow('image', imgS)
    print('Press esc to end program')

    while(1):
        k = cv2.waitKey(33)
        if k == 27:    # Esc key to stop
            break
        elif k == -1:  # normally -1 returned,so don't print it
            continue
    cv2.destroyAllWindows()
    try:
        f = open("positions.csv", 'r')
        print("File Exists")
    except IOError:
        f = open("positions.csv", 'w+')
        print("File Created")
    filename = "positions.csv"
    np.savetxt(filename, left_clicks, delimiter=",")
    structure_factor.plot_structure_factor(left_clicks, SCAN_SIZE, SCAN_SIZE)




if __name__ == main():
    main()
