"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
from random import randint
import math
import webbrowser
import requests
import json

counter = 0
API_weather = "http://api.openweathermap.org/data/2.5/weather?appid=0e813999bfa8d3302e159b20ebdf1b4c&q="

cities_list = ["Berlin", "Barcelona", "Vienne", "Bruxelles", "Sophia", "Zagreb", "Madrid", "Tallinn",
               "Helsinki", "Paris", "Athena", "Budapest", "Dublin", "Rome", "Riga", "Luxembourg", "La Valette",
               "Amsterdam", "Varsovie", "Lisbonne", "Prague", "Bucarest", "London", "Bratislava", "Stockholm"]

list_sw = ["fuck", "fucking", "bitch", "son of bitch", "asshole", "dick", "pussy",
           "bastard", "cunt", "shit", "holy shit", "motherfucker", "nigga", "nigger"]

jokes_list = ["What is the difference between a snowman and a snowwoman? - Snowballs.",
              "Doctor says to his patient: 'You have cancer and Alzheimer.' - Patient: 'At least I don't have cancer.'",
              "Mother: 'How was school today, Patrick?' Patrick: 'It was really great mum! Today we made explosives!' Mother: 'Ooh, they do very fancy stuff with you these days. And what will you do at school tomorrow?' Patrick: 'What school?'",
              "'My wife suffers from a drinking problem.' - 'Oh is she an alcoholic?' - 'No, I am, but she’s the one who suffers.'",
              "Son: 'Dad what do you think about abortion ?' Dad: 'Ask your sister' Son: 'But I don't have ...' Dad: 'Exactly'"]

services = {
    "news": "https://news.google.com",
    "facebook": "https://www.facebook.com",
    "youtube": "https://www.youtube.com",
    "cinema": "https://www.imdb.com/movies-in-theaters"
}

getting_info = ["info on", "information on", "about", "details on"]


@route('/', method='GET')
def index():
    return template("chatbot.html")


def hello(name):
    get_name = name.split()
    get_name = get_name[-1].capitalize()
    if get_name == "Sacha":
        return "inlove", "Hello Master ! Good to see you back ! How can I help you ?"
    else:
        return "afraid", "Hi {0} ! Where is my Master Sacha ?".format(get_name)


def swear_words():
    return "no", "Please stay polite !"


def tell_joke():
    r = randint(0, len(jokes_list)-1)
    return "laughing", "Ok I'm sure you're gonna like this one ! {0}".format(jokes_list[r])


def question(user_question):
    if "your name" in user_question:
        return "dancing", "My name is Boto ! I just told it to you dummy ..."
    elif user_question.startswith("Do you know"):
        return "giggling", "Of course, I know everyone and everything in this universe !"
    elif "you live" in user_question:
        return "dog", "Sorry this is totally confidential"
    elif "How are you" in user_question:
        return "money", "I'm ok, thanks for asking"
    else:
        return "confused", "That's an interesting question !"


def get_services(user_demand):
    user_demand = user_demand.split()
    for s in services:
        if s in user_demand:
            webbrowser.open_new_tab(services[s])
            return "ok", "You asked for {0}, right ?".format(s)
    return "bored", "Sorry I can't help you with that ..."


def get_weather(user_city):
    for city in cities_list:
        if city in user_city:
            json_data = requests.get(API_weather + city).json()
            weather_description = json_data["weather"][0]["main"]
            temperature = int(json_data["main"]["temp"]) - 273.15
            humidity = int(json_data["main"]["humidity"])
            return "waiting", "Weather: " + weather_description + " / Temp: " + str(
                math.floor(temperature)) + "°C / Humidity: " + str(humidity) + "%"


def get_infos(user_demand):
    for info in getting_info:
        if info in user_demand:
            key_word = user_demand.split(info, 1)[1]
            url = "https://en.wikipedia.org/wiki/{0}".format(key_word)
            webbrowser.open_new_tab(url)
            return "giggling", "You asked for infomation about {0}, right ?".format(key_word)


def handle_answers(user_input):
    user_message = request.POST.get('msg')
    global counter
    if counter == 0:
        counter += 1
        return hello(user_input)
    elif any(swear_word in user_message for swear_word in list_sw):
        return swear_words()
    elif any(city in user_message for city in cities_list):
        return get_weather(user_input)
    elif any(info in user_message for info in getting_info):
        return get_infos(user_input)
    elif user_message.endswith("?"):
        return question(user_input)
    elif "joke" in user_message:
        return tell_joke()
    else:
        return get_services(user_input)


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    animation, answer = handle_answers(user_message)
    return json.dumps({"animation": animation, "msg": answer})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
