import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
from datetime import datetime

NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
TMDB_API_KEY = config("TMDB_API_KEY")
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")

USERNAME = config('USER')
BOTNAME = config('BOTNAME')


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def play_on_youtube(video):
    kit.playonyt(video)


def search_on_google(query):
    kit.search(query)


def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?apiKey={NEWS_API_KEY}&language=pt").json()
    articles = res["articles"]
    print(f'artigos {articles}')
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_weather_report(city):

    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    print(res)
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    pressure = res["main"]["pressure"]
    humidity = res["main"]["humidity"]
    wind = res["wind"]["speed"]
    sunrise = datetime.fromtimestamp(res["sys"]["sunrise"])
    # sunrise = datetime.fromtimestamp(sunrise)
    sunrise = sunrise.strftime("%H:%M:%S")
    # sunrise = str(datetime.fromtimestamp(sunrise)).split(" ")[1]
    horas = sunrise.split(":")[0]
    minutos = sunrise.split(":")[1]
    sunrise = f"{horas} horas e {minutos} minutos"
    print(sunrise)
    sunset = datetime.fromtimestamp(res["sys"]["sunset"])
    sunset = sunset.strftime("%H:%M:%S")
    # sunset = str(datetime.fromtimestamp(sunset)).split(" ")[1]
    horas = sunset.split(":")[0]
    minutos = sunset.split(":")[1]
    sunset = f"{horas} horas e {minutos} minutos"
    print(sunset)
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃", pressure, humidity, wind, sunrise, sunset


def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']
