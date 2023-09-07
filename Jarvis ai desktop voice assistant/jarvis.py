# import random
import pyttsx3, datetime, time, winsound, threading, requests, pytz, re
import speech_recognition as sr
# import webbrowser
# import os
# import smtplib
# import subprocess
# import pyautogui
# import cv2
# from cvzone.HandTrackingModule import HandDetector
# import numpy as np
# import math
# from cvzone.ClassificationModule import Classifier
from bs4 import BeautifulSoup

'''# cap = cv2.VideoCapture(0)
# detector = HandDetector(maxHands=1)
# classifier = Classifier('Model/keras_model.h5', "Model/labels.txt")
# offset = 20
# imgSize = 300
# labels = ['A', 'B', 'C'] '''

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ['st', 'nd', 'rd', 'th']
HOURS = list(range(1, 13))
MINUTES = list(range(0, 60))
AM_PM = ["am", "pm"]

engine = pyttsx3.init() # 'sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_date(text):
    text = text.lower()
    today = datetime.date.today()
    if text.count('today')>0:
        return today
    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found>0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month<today.month and month!=-1:
        year = year+1
    if day<today.day and month==-1 and day!=-1:
        month = month+1
    if month==-1 and day==-1 and day_of_week!=-1:
        current_day_of_week = today.weekday()
        diff = day_of_week-current_day_of_week
        if diff<0:
            diff+=7
            if text.count('next')>=1:
                diff+=7
        return today+datetime.timedelta(diff)
    if month == -1 or day == -1:
        return None
    return datetime.date(month=month, day=day, year=year)

def get_time(text):
    text = text.lower()
    hour = -1
    minute = -1
    am_pm = ""
    
    for word in re.findall(r'\w+', text):
        if word.isdigit():
            num = int(word)
            if 1 <= num <= 12:
                hour = num
            elif 0 <= num <= 59:
                minute = num
        elif word in ["am", "pm"]:
            am_pm = word
    
    if hour == -1 or minute == -1:
        return None
    
    if am_pm == "pm" and hour < 12:
        hour += 12
    
    return datetime.time(hour=hour, minute=minute)

def get_events(day, service):
    # Google Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    
    # in the api code: events_result = service.events().list(timeMin = date.isoformat(), timeMax = end_date.isoformat(),).execute()
    
    # start_time = str(start.split("T")[1].split("-")[0])
    # if int(start_time.split(":")[0])<12:
    #     start_time = start_time + "am"
    # else:
    #     start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
    #     start_time = start_time + "pm"

'''# def wishme():
#     hour = int(datetime.datetime.now().hour)
#     if (hour >= 0 and hour < 12):
#         speak('Good Morning Sir!')
#     elif (hour >= 12 and hour < 17):
#         speak('Good Afternoon Sir!')
#     else:
#         speak('Good Evening Sir!')
#     speak('How may I help you?')

    # {'index': 1, 'structVersion': 2, 'name': 'Microphone Array (AMD Audio Dev', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
    # {'index': 1, 'structVersion': 2, 'name': 'Headset Microphone (Realtek(R) ', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}
    # ['Microsoft Sound Mapper - Input', 
    # 'Headset Microphone (Realtek(R) ', 
    # 'Microphone Array (AMD Audio Dev', 
    # 'Microsoft Sound Mapper - Output', 
    # 'Headphone (Realtek(R) Audio)', 
    # 'Speaker (Realtek(R) Audio)', 
    # 'Primary Sound Capture Driver', 
    # 'Headset Microphone (Realtek(R) Audio)', 
    # 'Microphone Array (AMD Audio Device)', 
    # 'Primary Sound Driver', 
    # 'Headphone (Realtek(R) Audio)', 
    # 'Speaker (Realtek(R) Audio)', 
    # 'Headphone (Realtek(R) Audio)', 
    # 'Speaker (Realtek(R) Audio)', 
    # 'Microphone Array (AMD Audio Device)', 
    # 'Headset Microphone (Realtek(R) Audio)', 
    # 'Stereo Mix (Realtek HD Audio Stereo input)', 
    # 'Headphones 1 (Realtek HD Audio 2nd output with HAP)', 
    # 'Headphones 2 (Realtek HD Audio 2nd output with HAP)', 
    # 'PC Speaker (Realtek HD Audio 2nd output with HAP)', 
    # 'Speakers 1 (Realtek HD Audio output with HAP)', 
    # 'Speakers 2 (Realtek HD Audio output with HAP)', 
    # 'PC Speaker (Realtek HD Audio output with HAP)', 
    # 'Microphone (Realtek HD Audio Mic input)', 
    # 'Microphone Array 1 (AMDAfdInstall Wave Microphone - 0)', 
    # 'Microphone Array 2 (AMDAfdInstall Wave Microphone - 0)']
    # ['Microsoft Sound Mapper - Input', 
    # 'Microphone Array (AMD Audio Dev', 
    # 'Microsoft Sound Mapper - Output', 
    # 'Speaker (Realtek(R) Audio)', 
    # 'Primary Sound Capture Driver', 
    # 'Microphone Array (AMD Audio Device)', 
    # 'Primary Sound Driver', 
    # 'Speaker (Realtek(R) Audio)', 
    # 'Speaker (Realtek(R) Audio)', 
    # 'Microphone Array (AMD Audio Device)', 
    # 'Stereo Mix (Realtek HD Audio Stereo input)', 
    # 'Headphones 1 (Realtek HD Audio 2nd output with HAP)', 
    # 'Headphones 2 (Realtek HD Audio 2nd output with HAP)', 
    # 'PC Speaker (Realtek HD Audio 2nd output with HAP)', 
    # 'Speakers 1 (Realtek HD Audio output with HAP)', 
    # 'Speakers 2 (Realtek HD Audio output with HAP)', 
    # 'PC Speaker (Realtek HD Audio output with HAP)', 
    # 'Microphone (Realtek HD Audio Mic input)', 
    # 'Microphone Array 1 (AMDAfdInstall Wave Microphone - 0)', 
    # 'Microphone Array 2 (AMDAfdInstall Wave Microphone - 0)'] '''
def takeCommand():
    r = sr.Recognizer()
    # if len(sr.Microphone.list_microphone_names())>25:
    #     mic = sr.Microphone(device_index=2)
    # else:
    mic = sr.Microphone()
    with mic as source:
        # r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=1.2)
        print('Listening...')
        speak("Ready Boss!")
        audio = r.listen(source=source, timeout=0, phrase_time_limit=7)
    
    try:
        speak("Recognizing...")
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in') # for hindi, use hi
        print(f'User Said: {query}\n')


    except Exception as e:
        print('Say that again please...')
        return "None"
    
    return query

'''# def sendemail(to, content):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.login('arjun.varshney1423@gmail.com', 'A_V_2314')
#     server.sendmail('arjun.varshney1423@gmail.com', to, content)
#     server.close() '''

def set_alarm(alarm_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            print("Alarm! Wake up!")
            # You can replace the print statement with a notification or any other desired action
            # Play a sound to get your attention
            winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            break
        time.sleep(1)  # Sleep for 1 second before checking the time again

def start_alarm_thread(alarm_time):
    alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time,))
    alarm_thread.start()

def wakeupDetected():
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            return "True-Mic"
        else:
            pass

def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=7156f0e5f0cb4b14be5be2f457e63f3a"
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    for article in articles:
        print(article['title'], article['url'])
        speak(article['title'])

def scrape_web():
    # r = requests.get("https://omoptik.vercel.app/allcustomers")
    # with open('files/index.html', 'w') as f:
    #     f.write(r.text)
    with open('files/index.html', 'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.prettify())
    # print(soup.title.string)
    # print(soup.title.name)
    print(len(soup.find_all('tr')[1:]))
    for link in soup.find_all('tr')[1:]:
        # print(link, link.get('href'))
        print(link.get_text())
'''    # print(soup.find(id='something'))
    # print(soup.find(class_='something'))
    # print(soup.select('div.anyclass'))
    # print(soup.select('div#anyid'))
    # print(soup.div.get('class'))
    # for child in soup.find(id='container').children:
    #     print(child)
    # i=0
    # for parent in soup.find(class_='box').parents:
    #     i+=1
    #     print(parent)
        # if i==2:
        #     break
    # cont = soup.find(class_ = 'container')
    # cont.name = 'span'
    # cont["class"] = 'myClass class2'
    # cont.string = 'I am a string'
    # print(cont)
    # ulTag = soup.new_tag('ul')
    # liTag = soup.new_tag('li')
    # liTag.string = 'Home'
    # ulTag.append(liTag)
    # liTag = soup.new_tag('li')
    # liTag.string = 'About'
    # ulTag.append(liTag)
    # soup.html.body.insert(0, ulTag)
    # cont = soup.find(class_ = 'container')
    # print(cont.has_attr('class'))
    # def has_class_but_not_id(tag):
    #     return tag.has_attr('class') and not tag.has_attr('id')
    # results = soup.find_all(has_class_but_not_id)
    # print(results)

# def start_camera():
#     while True:
#         success, img = cap.read()
#         img = cv2.flip(img,1)
#         imgOutput = img.copy()
#         hands, img = detector.findHands(img, flipType=False)
#         if hands:
#             hand = hands[0]
#             x,y,w,h = hand['bbox']

#             imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255

#             imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

#             imgCropShape = imgCrop.shape

#             aspectRatio =h/w
#             if aspectRatio>1:
#                 k = imgSize/h
#                 wCal = math.ceil(k*w)
#                 imgResize = cv2.resize(imgCrop, (wCal, imgSize))
#                 imgResizeShape = imgResize.shape
#                 wGap = math.ceil((imgSize-wCal)/2)
#                 imgWhite[:, wGap:wCal+wGap]=imgResize
#                 prediction, index = classifier.getPrediction(imgWhite, draw=False)
#             else:
#                 k = imgSize/w
#                 hCal = math.ceil(k*h)
#                 imgResize = cv2.resize(imgCrop, (imgSize, hCal))
#                 imgResizeShape = imgResize.shape
#                 hGap = math.ceil((imgSize-hCal)/2)
#                 imgWhite[hGap:hCal+hGap, :]=imgResize
#                 prediction, index = classifier.getPrediction(imgWhite, draw=False)

#             cv2.rectangle(imgOutput, (x-offset,y-offset-50), (x-offset+90,y-offset), (255,0,255),cv2.FILLED)
#             cv2.putText(imgOutput, labels[index], (x,y-27), cv2.FONT_HERSHEY_COMPLEX,1.7,(255,255,255),2)
#             cv2.rectangle(imgOutput, (x-offset,y-offset), (x+w+offset,y+h+offset), (255,0,255),4)
#             # cv2.imshow('ImageCrop', imgCrop)
#             # cv2.imshow('ImageWhite', imgWhite)
#             return labels[index]
            
#         cv2.imshow('Image', imgOutput)
#         cv2.waitKey(1)

# def start_camera_thread():
#     camera_thread = threading.Thread(target=start_camera)
#     camera_thread.start()

# def note(text):
#     date = datetime.date.today()
#     file_name = str(date).replace(":", "-") + "-note.txt"
#     with open(file_name, "w") as f:
#         f.write(text)

#     subprocess.Popen(["notepad.exe", file_name])
    # os.remove(file_name)
'''
if __name__ == "__main__":
    # time.sleep(2)
    # wishme()
    speak('Good Day sir! How may I help you?')
    while True:
        # query = takeCommand().lower()
        query = input("Type something: ").lower()
        # query = start_camera()

        # if ('forward' in query):
        #     # time.sleep(3)
        #     pyautogui.keyDown('right')
        
        # elif ('A' in query):
        #     speak("A for Apple")
        
        # elif ('B' in query):
        #     speak("B for Ball")

        # elif ('C' in query):
        #     speak("C for Chrome")
        
        # elif ('go back' in query):
        #     # time.sleep(3)
        #     pyautogui.keyDown('left')

        if ('data' in query):
            speak('Scraping data...')
            scrape_web()
            speak("Data scraped")

        elif ('what do i have' in query):
            response=get_date(query)
            speak(response)

        elif ('time' in query):
            resp=get_time(query)
            speak(resp)

        elif ('news' in query):
            speak("Today's headlines are...")
            get_news()

        elif ('sleep' in query):
            query = wakeupDetected()
            if "True-Mic" in query:
                print("Wakeup Detected!!")
            else:
                pass

        elif ('what is your name' in query):
            speak('My name is Jarvis')

        elif ('hello' in query):
            speak('Hello Sir! How may I help you?')

        elif ('hi' in query):
            speak('Hello Sir! How may I help you?')

        elif ('how are you' in query):
            speak('I am fine sir. How about you?')

        elif ('i am also fine' in query):
            speak('Please stay safe and stay healthy')

        elif ('thank you' in query):
            speak('Thank you sir! Now please command me!')
        
        # elif ('open youtube' in query):
        #     webbrowser.open("https://www.youtube.com", webbrowser.WindowsDefault)

        # elif ('open google' in query):
        #     webbrowser.open("https://www.google.com", webbrowser.WindowsDefault)

        # elif ('open facebook' in query):
        #     webbrowser.open("https://www.facebook.com", webbrowser.WindowsDefault)
        
        # elif ('open whatsapp' in query):
        #     webbrowser.open("https://web.whatsapp.com", webbrowser.WindowsDefault)

        # elif ('send a whatsapp message' in query):
        #     speak("Please specify the mobile number of the receiver of your message")

        # elif ('website' in query):
        #     url = input("Please specify the url: ")
        #     webbrowser.open(url, webbrowser.WindowsDefault)

        # elif ('search' in query):
        #     searchvar = query.replace('search', '')

        # elif ('play' in query):
        #     ytlink = query.replace('play', '')
        #     speak("Playing " + ytlink)

        # elif('open chrome' in query):
        #     chromepath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        #     os.startfile(chromepath)

        # elif ('open code' in query):
        #     codepath = "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        #     os.startfile(codepath)

        # elif ('open music' in query):
        #     music_url = "F:\\oldies\\Movies and Cartoons\\else\\songs\\mp3"
        #     # os.startfile(music_url)
        #     songs = os.listdir(music_url)
        #     song = random.choice(songs) # songs[0]
        #     songlist = ("F:\\oldies\\Movies and Cartoons\\else\\songs\\mp3\\"+song)
        #     os.startfile(songlist)

        # elif ('make a note' in query):
        #     speak("What would you like me to make a note of?")
        #     note_text = takeCommand()
        #     # note_text = input("enter here: ")
        #     note(note_text)
        #     speak("I have made a note of that")

        elif ('the time' in query):
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir the time is {strTime}")

        # elif ('set timer' in query):
        #     print("Current time is: ", datetime.datetime.now().strftime("%H:%M:%S"))
        #     speak('Timer for 30 minutes has been set.')
        #     time.sleep(60*30)
            # notification.notify(
            # title="Half an hour has passed!!",
            # message='U have successfully spent half an hour more!!',
            # # app_icon=r'C:\Users\DELL\Desktop\Coding\Programming\App design\notification_app\icon.ico',
            # timeout=10
            # )

        elif ('set alarm' in query):
            alarm_time = input("Enter the alarm time in HH:MM format: ")
            start_alarm_thread(alarm_time)

        # elif ('send email' in query):
        #     try:
        #         speak('Who should be the receipient of this mail?')
        #         # to = takeCommand()
        #         to = input("Please enter the email id: ")
        #         speak('What should I say?')
        #         # content = takeCommand()
        #         content = input()
        #         sendemail(to, content)
        #         speak('Email has been sent!')
        #     except Exception as e:
        #         speak('Sorry sir...your email could not be sent.')
        
        elif ('quit' in query):
            speak('Thank you!')
            exit()

        else:
            speak('That command was not recognised')
