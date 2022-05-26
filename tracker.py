import cv2 as cv

video_width = 1280
video_height = 720

target_box_x1 = int(video_width/2-200)
target_box_x2 = int(video_width/2+200)
target_box_y1 = int(video_height/2-100)
target_box_y2 = int(video_height/2+100)

lineWidth = 2

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_WIDTH, video_width)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, video_height)

def selectTarget():
    global video_width
    global video_height
    global target_box_x1 
    global target_box_x2 
    global target_box_y1
    global target_box_y2
    global lineWidth
    global vid

    frame = 0
    quitValue = False

    while(True):
        ret, frame = vid.read()

        noBoxImage = frame.copy()
        cv.rectangle(frame,(target_box_x1,target_box_y1), (target_box_x2,target_box_y2), (0,255,0), lineWidth)
        cv.line(frame,(int(video_width/2-10), int(video_height/2)), (int(video_width/2+10), int(video_height/2)), (0,255,0), 1)
        cv.line(frame,(int(video_width/2), int(video_height/2-10)), (int(video_width/2), int(video_height/2+10)), (0,255,0), 1)
        cv.imshow('Tracker', frame)

        key = cv.waitKey(1)

        if key == ord('l'):
            break
        elif key == ord('a'):
            target_box_x1 +=10
            target_box_x2 -=10
        elif key == ord('d'):
            target_box_x1 -=10
            target_box_x2 +=10
        elif key == ord('s'):
            target_box_y1 +=10
            target_box_y2 -=10
        elif key == ord('w'):
            target_box_y1 -=10
            target_box_y2 +=10
        elif key == ord('q'):
            quitValue = True
            break

    targetImage = noBoxImage[target_box_y1:target_box_y2, target_box_x1:target_box_x2]

    return quitValue, vid, targetImage, lineWidth

def trackTarget(vid, targetImage, lineWidth):
    cv.imwrite('target.jpg', targetImage)
    targetImage = cv.imread('target.jpg',0)
    w, h = targetImage.shape[::-1]

    quitValue = False

    while(True):
        _, frame = vid.read()

        grayscaleImage = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        res = cv.matchTemplate(grayscaleImage,targetImage,eval('cv.TM_CCOEFF_NORMED'))
        _, _, _, top_left = cv.minMaxLoc(res)
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv.rectangle(frame,top_left, bottom_right, (0,0,255), lineWidth)
        cv.imshow('Tracker', frame)

        key = cv.waitKey(1)

        if key == ord('l'):
            break
        elif key == ord('q'):
            quitValue = True
            break

    return quitValue

if __name__ == "__main__":
    while True:
        quitValue, vid, targetImage, lineWidth = selectTarget()
        if quitValue == True:
            break 
        quitValue = trackTarget(vid, targetImage, lineWidth)  
        if quitValue == True:
            break  