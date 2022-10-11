import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from random import choice
from utils import opening_text
from pprint import pprint


USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init()

# Set Rate
engine.setProperty('rate', 210)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty("voice", "brazil")
engine.setProperty("languages", [b'\x05pt-br'])

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


# Greet the user
def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Bom dia {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Boa tarde {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Boa tarde {USERNAME}")
    speak(f"Eu sou {BOTNAME}. Como posso ajudar?")

# Takes Input from User
def chama_severino():
    pass
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='pt-br')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


if __name__ == '__main__':
    greet_user()
    while 1:
        query = take_user_input().lower()
        if 'severino' in query:
            speak('Sim Senhor!')
            while 1:
                query = take_user_input().lower()
                if 'open notepad' in query:
                    open_notepad()

                elif 'open discord' in query:
                    open_discord()

                elif 'open command prompt' in query or 'open cmd' in query:
                    open_cmd()

                elif 'open camera' in query:
                    open_camera()

                elif 'open calculator' in query:
                    open_calculator()

                elif 'ip address' in query:
                    ip_address = find_my_ip()
                    speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    print(f'Your IP Address is {ip_address}')

                elif 'wikipedia' in query:
                    speak('What do you want to search on Wikipedia, sir?')
                    search_query = take_user_input().lower()
                    results = search_on_wikipedia(search_query)
                    speak(f"According to Wikipedia, {results}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(results)

                elif 'youtube' in query:
                    speak('What do you want to play on Youtube, sir?')
                    video = take_user_input().lower()
                    play_on_youtube(video)

                elif 'pesquise no google' in query:
                    speak('What do you want to search on Google, sir?')
                    query = take_user_input().lower()
                    search_on_google(query)

                elif "send whatsapp message" in query:
                    speak(
                        'On what number should I send the message sir? Please enter in the console: ')
                    number = input("Enter the number: ")
                    speak("What is the message sir?")
                    message = take_user_input().lower()
                    send_whatsapp_message(number, message)
                    speak("I've sent the message sir.")

                elif "send an email" in query:
                    speak("On what email address do I send sir? Please enter in the console: ")
                    receiver_address = input("Enter email address: ")
                    speak("What should be the subject sir?")
                    subject = take_user_input().capitalize()
                    speak("What is the message sir?")
                    message = take_user_input().capitalize()
                    if send_email(receiver_address, subject, message):
                        speak("I've sent the email sir.")
                    else:
                        speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

                elif 'joke' in query:
                    speak(f"Hope you like this one sir")
                    joke = get_random_joke()
                    speak(joke)
                    speak("For your convenience, I am printing it on the screen sir.")
                    pprint(joke)

                elif "advice" in query:
                    speak(f"Here's an advice for you, sir")
                    advice = get_random_advice()
                    speak(advice)
                    speak("For your convenience, I am printing it on the screen sir.")
                    pprint(advice)

                elif "filme" in query:
                    speak(f"Uma boa dica de filmes é: {get_trending_movies()}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(*get_trending_movies(), sep='\n')

                elif 'notícias' in query:
                    speak(f"Vou procurar as manchetes do dia, Senhor")
                    speak(get_latest_news())
                    speak("Estou imprimindo na tela o resultado da consulta, senhor, caso seja melhor para o senhor.")
                    print(*get_latest_news(), sep='\n')

                elif 'clima' in query:
                    ip_address = find_my_ip()
                    city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                    speak(f"Consultando a previsão do tempo para {city}")
                    weather, temperature, feels_like, pressure, humidity, wind, sunrise, sunset = get_weather_report(city)
                    speak(f"A temperatura atual é {temperature}, e tem a sensação de {feels_like}")
                    speak(f"A pressão atmosférica está em {pressure} milibares")
                    speak(f"A umidade relativa do ar está em {humidity} porcento")
                    speak(f"O vento está soprando de a uma velocidade de {wind} quilômetros por hora")
                    speak(f"O sol nasce às {sunrise} e se põe às {sunset}")
                    speak(f"Além disso, a previsão fala de {weather}")
                    speak("Estou imprimindo na tela o resultado da consulta, senhor, caso seja melhor para o senhor.")
                    print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
