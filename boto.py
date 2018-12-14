"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
from random import randint
import webbrowser
import json

counter = 0

list_sw = ["fuck", "fucking", "bitch", "son of bitch", "asshole", "dick", "pussy",
           "bastard", "cunt", "shit", "holy shit", "motherfucker", "nigga", "nigger"]

jokes_list = ["What is the difference between a snowman and a snowwoman? - Snowballs.",
              "Doctor says to his patient: 'You have cancer and Alzheimer.' - Patient: 'At least I don't have cancer.'",
              "Mother: 'How was school today, Patrick?' Patrick: 'It was really great mum! Today we made explosives!' Mother: 'Ooh, they do very fancy stuff with you these days. And what will you do at school tomorrow?' Patrick: 'What school?'",
              "'My wife suffers from a drinking problem.' - 'Oh is she an alcoholic?' - 'No, I am, but she’s the one who suffers.'",
              "Son: 'Dad what do you think about abortion ?' Dad: 'Ask your sister' Son: 'But I don't have ...' Dad: 'Exactly'"]

keys_words = ["weather", "cinema", "news", "facebook", "youtube"]

getting_info = ["info on", "information on", "about", "details on"]


@route('/', method='GET')
def index():
    return template("chatbot.html")


def hello(name):
    get_name = name.split()
    get_name = get_name[-1].capitalize()
    return "exciting", "Hi {0} ! What can I do for you ?".format(get_name)


def question():
    return "confused", "That's an interesting question ! Maybe you should search it on google"


def swear_words():
    return "no", "Please stay polite !"


def tell_joke():
    r = randint(0, 4)
    return "laughing", "Ok I'm sure you're gonna like this one ! {0}".format(jokes_list[r])


def get_services(user_demand):
    user_demand = user_demand.split()
    url = "https://www.google.com/search?q="
    for i in keys_words:
        if i in user_demand:
            webbrowser.open_new_tab(url + i)
            return "ok", "You asked for {0}, right ?".format(i)
    return "bored", "Sorry I can't help you with that ..."


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
    elif user_message.endswith("?"):
        return question()
    elif "joke" in user_message:
        return tell_joke()
    elif any(info in user_message for info in getting_info):
        return get_infos(user_input)
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
