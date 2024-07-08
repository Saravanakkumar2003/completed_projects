import cv2
import winsound
import datetime
import os
cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray= cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur= cv2.GaussianBlur(gray, (5,5), 0)
    _ , thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None, iterations=3)
    contours,_ = cv2.findContours(dilated, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#check if the ambient light is low
    avg_light=cv2.mean(frame1)[0]
    if avg_light < 50:
        #switch to night mode
        night_frame=cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
        _ , night_thresh=cv2.threshold(night_frame,50,255,cv2.THRESH_BINARY_INV)
        frame1=cv2.cvtColor(night_thresh,cv2.COLOR_GRAY2RGB)
    else:
            #continue with normal code
         for c in contours:
             if cv2.contourArea(c)<5000:
                 continue
             x,y,w,h = cv2.boundingRect(c)
             cv2.rectangle(frame1, (x,y),(x+w, y+h), (0,255,0), 2)
             winsound.PlaySound('alertsoundmp',winsound.SND_ASYNC)
#save the caputure frame to file
             now=datetime.datetime.now()
             filename="captured_frame_{}.jpg".format(now.strftime("%Y%m%d_%H%M%S"))
             filepath=os.path.join("captured_frames",filename)
             cv2.imwrite(filepath,frame1)

    if cv2.waitKey(10) == ord('l'):
          break
    cv2.imshow("security camera",frame1) 
cv2.destroyAllWindows()
cam.release()
    

