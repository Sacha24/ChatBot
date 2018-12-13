"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json

@route('/', method='GET')
def index():
    return template("chatbot.html")


def hello(name):
    return "Hi {0} ! What can I do for you ?".format(name)


def question():
    return "That's an interesting question ! Maybe you should search it on google"


def swear_words():
    return "Please stay polite !"


counter = 0


def handle_answers(answer):
    list_sw = ["fuck", "bitch", "son of bitch", "asshole", "dick", "pussy", "bastard",
               "cunt", "shit", "holy shit", "motherfucker", "nigga", "nigger"]
    user_message = request.POST.get('msg')
    global counter
    for swear_word in list_sw:
        if counter == 0:
            counter += 1
            return hello(answer)
        elif swear_word.lower() or swear_word.upper() in user_message:
            return swear_words()
        elif counter == 1 and user_message.endswith("?"):
            return question()
        else:
            return "Sorry I can't help you with that ..."



@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": handle_answers(user_message)})


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
