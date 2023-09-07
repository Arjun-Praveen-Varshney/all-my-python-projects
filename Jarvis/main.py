import speech_recognition as sr
from googletrans import Translator
import threading, requests, re, datetime, pyttsx3, time
# import openai
# from bs4 import BeautifulSoup

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ['st', 'nd', 'rd', 'th']

# openai.api_key = "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"
# completion = openai.Completion()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
# engine.setProperty('rate',170)

r = sr.Recognizer()
mic = sr.Microphone()

translate = Translator()

def speak(Text):
    print(f"\nJarvis: {Text}\n")
    try:
        engine.say(Text)
        engine.runAndWait()
    except:
        print("\nSome error occured :(\n")

def listen():
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1.25)
        print("Listening...")
        audio = r.listen(source,0,7)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="hi")
    except:
        print("Some error occured! :(")
        return ""
    
    query = str(query)
    return query

def listenForWakeWord():
    r=sr.Recognizer()
    # if len(names)>25:
    #     mic = sr.Microphone(device_index=2)
    # else:
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1.25)
        print("Listening...")
        audio = r.listen(source,0,7)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="hi")
    except:
        return ""
    
    query = str(query).lower()
    return query

def translationHinToEng(text):
    try:
        result = translate.translate(text)
        data = result.text
    except:
        print("Error occurred during translation")
        data = ''
    print(f"You: {data}")
    return data

def micExecution():
    try:
        query = listen()
        question = translationHinToEng(query)
    except:
        print("Error occurred during translation")
        question = ''
    data = str(question).lower()
    return data

def micExecutionForWakeWord():
    query = listenForWakeWord()
    data = translationHinToEng(query)
    return data

def wakeupDetected():
    while True:
        query = micExecutionForWakeWord().lower()
        if "wake up" in query:
            return "True-Mic"
        else:
            pass

'''# def replyBrain(question, chat_log=None):
#     FileLog = open("files\\chat_log.txt", "r")
#     chat_log_template = FileLog.read()
#     FileLog.close()

#     if chat_log is None:
#         chat_log = chat_log_template

#     prompt = f'{chat_log}You: {question}\nJarvis: '
#     response = completion.create(model="text-davinci-003", prompt=prompt, temperature=0.5, max_tokens=60, top_p=0.3, frequency_penalty=0.5, presence_penalty=0)
#     answer = response.choices[0].text.strip()
#     chat_log_template_update = chat_log_template + f"\nYou: {question} \nJarvis: {answer}"
#     FileLog = open("files\\chat_log.txt", "w")
#     FileLog.write(chat_log_template_update)
#     FileLog.close()
#     return answer'''

def fetchNews():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=7156f0e5f0cb4b14be5be2f457e63f3a"
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    for article in articles:
        print(article['url'])
        speak(article['title'])

def get_date(text):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    day_after_tomorrow = today + datetime.timedelta(days=2)
    if 'today' in text:
        return today
    if 'day after tomorrow' in text or 'day before yesterday' in text:
        return day_after_tomorrow
    elif 'tomorrow' in text or 'yesterday' in text:
        return tomorrow
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
    hour = -1
    minute = -1
    am_pm = ""

    time_match = re.search('\d.*:.*\d', text)
    if time_match:
        time_matched = time_match.group().replace(" ", "").split(":")
        
        hour = int(time_matched[0])
        minute = int(time_matched[1])
    
    # for word in re.findall(r'\w+', text):
    #     if word.isdigit():
    #         num = int(word)
    #         if 1 <= num <= 12:
    #             hour = num
    #         elif 0 <= num <= 59:
    #             minute = num
    #     elif word in ["am", "pm"]:
    #         am_pm = word
    
    time_of_day = {
        "am": "am",
        "pm": "pm",
        "evening": "pm",
        "afternoon": "pm",
        "noon": "pm",
        "night": "pm",
        "dusk": "pm",
        "sunset": "pm",
        "morning": "am",
        "day": "am",
        "midnight": "am",
        "dawn": "am",
        "sunrise": "am"
    }
    for key, value in time_of_day.items():
        if key in text:
            am_pm = value
    
    if hour == -1 or minute == -1:
        return None
    
    if am_pm == "pm" and hour < 12:
        hour += 12
    elif hour == 12:
        hour = 0
    return datetime.time(hour=hour, minute=minute)

def set_alarm(alarm_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == alarm_time:
            speak("Alarm! Wake up!")
            # You can replace the print statement with a notification or any other desired action
            # Play a sound to get your attention
            # winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            break
        time.sleep(1)  # Sleep for 1 second before checking the time again

def start_alarm_thread(alarm_time):
    alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time,))
    alarm_thread.start()

if __name__ == "__main__":
    speak("Hello Sir!")
    while True:
        query = micExecution().replace(".","")

        if len(query)<3:
            pass
        elif "news" in query:
            speak("Today's headlines are...")
            fetchNews()
        elif "alarm" in query:
            try:
                response = get_time(query)
                now = datetime.datetime.now()
                alarm_time = datetime.datetime.combine(now.date(), response)
                if alarm_time < now:
                    alarm_time += datetime.timedelta(days=1)
                speak(f"Do you want to set alarm for: {alarm_time}?")
                answer = micExecution().replace('.','')
                if "yes" in answer or "do" in answer or 'ok' in answer:
                    response = str(response)
                    start_alarm_thread(response)
                    speak("Alarm has been set!")
                else:
                    speak("Alarm has not been set!")
            except:
                speak("Try again")
        elif "remind" in query:
            try:
                respdate = get_date(query)
                speak(f"The date you want a reminder on is: {respdate}")
            except:
                speak("Try again")
        elif "sleep" in query:
            speak("Good night sir!")
            query = wakeupDetected()
            if "True-Mic" in query:
                speak("Wakeup Detected!!")
            else:
                pass
        elif "time" in query:
            speak(f"Sir, the time now is {int(datetime.datetime.now().hour)} hours, {int(datetime.datetime.now().minute)} minutes and {int(datetime.datetime.now().second)} seconds")
        elif "date" in query:
            speak(f"Sir, the date today is {datetime.datetime.now().date()}")
        elif "bye" in query:
            speak("Goodbye sir!")
            exit()
        else:
            # reply = replyBrain(query)
            speak("Command not understood")