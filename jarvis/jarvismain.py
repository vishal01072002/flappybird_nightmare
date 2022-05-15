from typing import Mapping
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser  # inbuilt
import os  # for music
# install wikipedia
import smtplib


# widows provides an API which uses to take voices
# which (sapi5) is Microsoft speech api
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)  # 2 object
# print(voices[1].id)  # 0 for male and 1 for female
engine.setProperty('voice', voices[1].id)  # set voice of female


# Make a speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    pass


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour > 0 and hour < 12:  # morning
        speak("good morning!")
    elif hour >= 12 and hour < 18:
        speak("good after noon!")
    elif hour >= 18 and hour < 21:
        speak("good evening!")
    else:
        speak("good night!")
    # print(hour)

    speak("i am jarvis, how may i help you")


def takecommand():
    # it takes voice and return string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listining...")
        r.pause_threshold = 1  # space between 2 word during speak will minimum1 sec
        audio = r.listen(source)  # we store voice in audio variable
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("user said : ", query)
    except Exception as e:
        print(e)

        print("sorry, please say that again...")
        return "none"  # return nine string if not able to understand what he speak
    return query  # else return querry (which user said)


# SMTP lib is pythin inbuils package
def sendmail(to, message):
    server = smtplib.SMTP('smtp.gamil.com', 587)
    server.ehlo()
    server.starttls()
    server.login('vishalbavakumar0000@gmail.com', 'password')
    server.sendmail('vishalbavakumar0000@gmail.com', to, message)
    server.close()


if __name__ == "__main__":
    speak("helllo lucifer ")  # sir , how can i help you
    wishme()
    # takecommand()

    while True:
        Query = takecommand().lower()

        # logic to execute tasks on the bases of query
        if "wikipedia" in Query:
            speak("according to wikipedia ")
            # print(Query)
            Query = Query.replace("wikipedia", "")
            result = wikipedia.summary(Query, sentences=2)
            # print(Query)
            speak(result)
            print(result)

        elif "open youtube" in Query:
            webbrowser.open("youtube.com")

        elif "open google" in Query:
            webbrowser.open("google.com")

        elif "play music" in Query:
            music_dir = 'F:\\music'
            # acctual path is --F:\music-- to escape(escape secuence) ->\<- use one more ->\<-

            # make a list of all song
            songs = os.listdir(music_dir)
            print(songs)
            # to start file
            # for random we can play random from 0 to len of songs - 1
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "the time" in Query:
            # strftime is used to give string formate for time
            time_string = datetime.datetime.now().strftime("%H:%M:%S")
            print(time_string)
            speak(f"sir , the time is {time_string}")

        elif "open code" in Query:
            vscode_path = "E:\\vscode\\Microsoft VS Code\\Code.exe"
            os.startfile(vscode_path)

        elif "mail to" in Query:
            try:
                speak("sir, what message should i have to send ?")
                content = takecommand()
                to_send = "vishalbavakumar0000@gmail.com"
                # we can make a dictonary with name and email to send many people

                # function to send mail
                sendmail(to_send, content)
                speak("email has been send")
            except Exception as e:
                print(e)
                speak("email is not send check your internet connection")
