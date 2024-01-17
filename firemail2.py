import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import requests
from playsound import playsound

fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        print("fire is detected")
        playsound('alert.mp3')

        # send email with location
        email = os.environ['EMAIL']
        password = os.environ['PASSWORD']
        to_address = ["dsaravanakkumar2003@gmail.com", "it244047@saranathan.ac.in"] #replace with the email addresses you wish to send

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = ", ".join(to_address)
        msg['Subject'] = 'Fire detected at home!'

        body = 'Hello,\n\nA fire has been detected at your home. Please take immediate action!'

        # get location
        response = requests.get('https://ipinfo.io/')
        location = response.json()['loc'].split(',')
        latitude = location[0]
        longitude = location[1]
        location_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
        location_text = f"Click the following link to view your location on Google Maps: {location_url}"

        msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(location_text, 'html'))

        # attach image
        img_name = 'fire.jpg'
        cv2.imwrite(img_name, frame)

        with open(img_name, 'rb') as f:
            img_data = f.read()

        msg.attach(MIMEApplication(img_data, name=os.path.basename(img_name)))

        # send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, to_address, text)
        server.quit()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

