from termcolor import colored  # Вывод цветных логов
from googlesearch import search  # Google
from googletrans import Translator
import requests
import os  # файловая система
import wave  # аудиофайлы WAV
import tkinter as tk
from tkinter import filedialog
import json  # JSON
import traceback  # работа программы без остановки при отлове исключений
import webbrowser  # Работа с браузера
import random  # рандом
import wikipediaapi  # Wikipedia
import pyttsx3  # Синтез речи
import speech_recognition  # Распознавание речи

# Использование машинного обучения
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

class User:
    # Пользователь
    name = "Аксель"
    native_l = "ru"
    target_l = "en"

class Helper:
    # Голосовой помощник
    name = "Nova"
    sex = "female"
    speech_l = "ru"
    recognition_l = ""

class Interpretation:
    # Получение перевода
    with open("words.json", "r", encoding="UTF-8") as file:
        vocabulary = json.load(file)
    def extract(self, message: str):
        if message in self.vocabulary:
            return self.vocabulary[message][helper.speech_l]
        else:
            # если слово не найдено, выводится сообщение в консоль и возвращается исходное сообщение
            print(colored("The term was not found", "red"))
            return message



def configure_assistant_voice():
    # Установка голоса
    voice_options = tts_eng.getProperty("voices")
    if helper.speech_l == "en":
        helper.recognition_l = "en-US"
        if helper.sex == "female":
            tts_eng.setProperty("voice", voice_options[1].id)
        else:
            tts_eng.setProperty("voice", voice_options[2].id)
    else:
        helper.recognition_l = "ru-RU"
        tts_eng.setProperty("voice", voice_options[0].id)

def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        data = ""

        try:
            print("Слушаю...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())
        except speech_recognition.WaitTimeoutError:
            play_voice(interpretation.extract("Не могли бы вы проверить, включен ли ваш микрофон, пожалуйста?"))
            traceback.print_exc()
            return
        # использование online-распознавания
        try:
            print("Анализ запроса...")
            data = recognizer.recognize_google(audio, language=helper.recognition_l).lower()

        except speech_recognition.UnknownValueError:
            pass

        return data
def play_voice(text_to_speech):
    # Проигрывание речи ответов
    tts_eng.say(str(text_to_speech))
    tts_eng.runAndWait()
def play_phrase(*args: tuple):
    # в случае ошибки распознания
    phrase = [
        interpretation.extract("Can you repeat, please?"),
        interpretation.extract("What did you say again?")
    ]
    play_voice(phrase[random.randint(0, len(phrase) - 1)])


def play_greetings(*args: tuple):
    # случайное приветствие
    greetings = [
        interpretation.extract("Hello, {}! How can I help you today?").format(user.name),
        interpretation.extract("Good day to you {}! How can I help you today?").format(user.name)
    ]
    play_voice(greetings[random.randint(0, len(greetings) - 1)])

def file_translation(*args: tuple):
    # перевод текста
    def translate_file(input_file, output_file, target_language='ru'):
        translator = Translator()
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
            translated_text = translator.translate(text, dest=target_language)
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write(translated_text.text)

    # Пример использования:
    input_file_path = 'input.txt'
    output_file_path = 'output.txt'
    translate_file(input_file_path, output_file_path)

    trans_file = [
        interpretation.extract("The file has been translated and is located in {}").format(output_file_path),
    ]
    play_voice(trans_file[random.randint(0, len(trans_file) - 1)])

def dollar_exchange(*args: tuple):
    # курс доллара
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()

    if 'rates' in data:
        per = f"1 USD = {data['rates']['RUB']} RUB"
        dollar = [
            interpretation.extract("The current dollar exchange rate {}").format(per),
        ]
        play_voice(dollar[0])

def euro_exchange(*args: tuple):
    # курс евра
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()

    if 'rates' in data:
        usd_to_rub = data['rates']['RUB']
        usd_to_eur = data['rates']['EUR']
        eur_to_rub = usd_to_rub / usd_to_eur
        euro_new = f"1 EUR = {eur_to_rub} RUB"
        euro = [
            interpretation.extract("The current euro exchange rate {}").format(euro_new),
        ]
        play_voice(euro[0])

def bitcoin_exchange(*args: tuple):
    # курс биткойна
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    bitcoin_new = f"1 Bitcoin в USD: {data['bitcoin']['usd']}"
    bitcoin = [
        interpretation.extract("The current Bitcoin exchange rate {}").format(bitcoin_new),
    ]
    play_voice(bitcoin[0])

def open_file(*args: tuple):
    if not args or not args[0]:
        return
    # Открыть файл
    filepath = filedialog.askopenfilename()
    if filepath:
        os.system(filepath)
        play_voice(interpretation.extract("The file is open"))


def play_joke(*args: tuple):
    # случайное приветствие
    phrase = [
        interpretation.extract("Why did the robot get angry? Everyone kept pushing their buttons!"),
        interpretation.extract("Be careful of robots! They byte!")
    ]
    play_voice(phrase[random.randint(0, len(phrase) - 1)])

def listening(*args: tuple):
    # случайное приветствие
    phrase = [
        interpretation.extract("I'm listening").format(user.name),
        interpretation.extract("I'm listening to you carefully").format(user.name)
    ]
    play_voice(phrase[random.randint(0, len(phrase) - 1)])

def play_far(*args: tuple):
    # случайное прощание
    phrase = [
        interpretation.extract("Goodbye, {}! Have a nice day!").format(user.name),
        interpretation.extract("See you soon, {}!").format(user.name)
    ]
    play_voice(phrase[random.randint(0, len(phrase) - 1)])
    tts_eng.stop()
    quit()


def search_google(*args: tuple):
    if not args or not args[0]:
        print("obviously, you didn't name the request after the command")
        return

    search_term = " ".join(args[0])

    url = "https://google.com/search?q=" + search_term
    webbrowser.extract().open(url)

    search_results = []
    try:
        for result in search(search_term,
                             tld="com",
                             lang=helper.speech_l,
                             num=1,
                             start=0,
                             stop=1,
                             pause=1.0):
            search_results.append(result)
            webbrowser.extract().open(result)

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return

    print("Search results:", search_results)
    print("Here is what I found for '{}' on Google.".format(search_term))

def search_video(*args):
    # Поиск видео на YouTube
    if not args or not args[0]:
        print("Вы не ввели запрос:")
        return
    search_term = " ".join(args[0])  # Joining the first element of args assuming it's a list of strings
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.extract().open(url)
    play_voice(interpretation.extract("Here is what I found for {} on youtube").format(search_term))

def search_wikipedia(*args: tuple):
    # Поиск в Wikipedia
    if not args[0]: return

    search_term = " ".join(args[0])

    # установка языка
    wiki = wikipediaapi.Wikipedia(helper.speech_l)

    # поиск страницы по запросу
    wiki_page = wiki.page(search_term)
    try:
        if wiki_page.exists():
            play_voice(interpretation.extract("Here is what I found for {} on Wikipedia").format(search_term))
            webbrowser.extract().open(wiki_page.fullurl)

            # чтение ассистентом первых двух предложений summary со страницы Wikipedia
            play_voice(wiki_page.summary.split(".")[:2])
        else:
            # открытие ссылки на поисковик в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
            play_voice(interpretation.extract(
                "Can't find {} on Wikipedia. But here is what I found on google").format(search_term))
            url = "https://google.com/search?q=" + search_term
            webbrowser.extract().open(url)

    # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    except:
        return

def change_language(*args: tuple):
    # Изменение языка
    helper.speech_l = "ru" if helper.speech_l == "en" else "en"
    configure_assistant_voice()
    print(colored("Language switched to " + helper.speech_l, "cyan"))


def play_person(*args: tuple):
    if not args[0]: return

    google_search_term = " ".join(args[0])
    vk_search_term = "_".join(args[0])

    # открытие ссылки на поисковик в браузере
    url = "https://google.com/search?q=" + google_search_term + " site: vk.com"
    webbrowser.extract().open(url)


    # открытие ссылкок на поисковики социальных сетей
    vk_url = "https://vk.com/people/" + vk_search_term
    webbrowser.extract().open(vk_url)

    play_voice(interpretation.extract("Here is what I found for {} on social nets").format(google_search_term))


def coin(*args: tuple):
    """
        Simulates flipping a coin multiple times and determines the winner based on the number of heads and tails.

        Args:
        *args (tuple): Additional arguments (not used in this function).

        Returns:
        None
    """
    flips_count = 3
    heads = sum(random.randint(0, 1) for _ in range(flips_count))
    tails = flips_count - heads
    won = "Tails" if tails > heads else "Heads"
    play_voice(f"{interpretation.extract(won)} {interpretation.extract('won')}")


def prepare_corpus():
    # угадывание намерения пользователя
    body = []
    direction = []
    for intent_name, intent_data in setConfig["aim"].items():
        for example in intent_data["variants"]:
            body.append(example)
            direction.append(intent_name)

    t_vector = vectorizer.fit_transform(body)
    classifier_prob.fit(t_vector, direction)
    classif.fit(t_vector, direction)


def get_intent(request):
    # Получение наиболее вероятного намерения в зависимости от запроса пользователя
    best_intent = classif.predict(vectorizer.transform([request]))[0]

    index_of_best_intent = list(classifier_prob.classes_).index(best_intent)
    probabilities = classifier_prob.predict_proba(vectorizer.transform([request]))[0]

    best_intent_probability = probabilities[index_of_best_intent]

    # близость к предсказанному значению
    if best_intent_probability > 0.157:
        return best_intent


def make_preparations():
    # Подготовка глобальных переменных к запуску приложения
    global recognizer, microphone, tts_eng, user, helper, interpretation, vectorizer, classifier_prob, classif

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    # инициализация инструмента синтеза речи
    tts_eng = pyttsx3.init()

    # настройка данных пользователя и помощника
    user = User()
    helper = Helper()

    # установка голоса по умолчанию
    configure_assistant_voice()
    # добавление возможностей перевода фраз (из заготовленного файла)
    interpretation = Interpretation()
    # подготовка распознавания запросов пользователя
    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    classifier_prob = LogisticRegression()
    classif = LinearSVC()
    prepare_corpus()

def checking_offers(voice_input_parts):
    if len(voice_input_parts) > 1:
        for guess in range(len(voice_input_parts)):
            intent = get_intent((" ".join(voice_input_parts[0:guess])).strip())
            print(intent)
            if intent:
                command_options = [voice_input_parts[guess:len(voice_input_parts)]]
                print(command_options)
                setConfig["aim"][intent]["answer"](*command_options)
                break
            if not intent and guess == len(voice_input_parts) - 1:
                setConfig["failure_phrases"]()

def executing_commands():
    voice_input_parts = voice_in.split(" ")

    # запрос из 1-ого слова
    if len(voice_input_parts) == 1:
        intent = get_intent(voice_in)
        if intent:
            if intent in setConfig["aim"]:
                setConfig["aim"][intent]["answer"]()
            else:
                print("Намерение не распознано:", intent)
                # Обработка нераспознанного намерения
        else:
            print("Намерение не найдено для ввода:", voice_in)
            # Обработка случая, когда намерение не найдено

        if "failure_phrases" in setConfig:
            setConfig["failure_phrases"]()
        else:
            print("Фразы ошибок не настроены")

    # в случае продолжительной фразы
    checking_offers(voice_input_parts)

def checking_the_input(voice_in):
    if os.path.exists("microphone-results.wav"):
        os.remove("microphone-results.wav")

    print(colored(voice_in, "blue"))



# перечень команд для использования
setConfig = {
    "aim": {
        "greeting": {
            "variants": ["привет", "здравствуй", "добрый день",
                         "hello", "good morning"],
            "answer": play_greetings
        },
        "joke": {
            "variants": ["шутка", "скажи шутку", "придумай шутку",
                         "joke", "Tell a joke", "Come up with a joke"],
            "answer": play_joke
        },
        "farewell": {
            "variants": ["пока", "до свидания", "увидимся", "до встречи",
                         "goodbye", "bye", "see you soon"],
            "answer": play_far
        },
        "wikipedia_search": {
            "variants": ["найди определение", "найди на википедии", "википедия",
                         "find on wikipedia", "find definition", "tell about"],
            "answer": search_wikipedia
        },
        "person_search": {
            "variants": ["пробей имя", "найди человека",
                         "find on facebook", " find person", "run person", "search for person"],
            "answer": play_person
        },
        "open_file": {
            "variants": ["открыть файл", "открой файл", "файл",
                         "open a file", "open the file", "file"],
            "answer": open_file
        },
        "toss_coin": {
            "variants": ["подбрось монетку", "подкинь монетку",
                         "toss coin", "coin", "flip a coin"],
            "answer": coin
        },
        "google_search": {
            "variants": ["гугл", "найди в гугл", "гугл",  "гугла",
                         "search on google", "google", "find on google"],
            "answer": search_google
        },
        "youtube_search": {
            "variants": ["найди видео", "покаж видео", "поиск видео", "показывай видео", "покажи видео",
                         "find video", "search on youtube", "find on youtube"],
            "answer": search_video
        },
        "dollar": {
            "variants": ["курс доллара", "доллар", "скажи курс доллара",
                         "dollar exchange rate", "dollar", "Tell me the dollar rate"],
            "answer": dollar_exchange
        },
        "euro": {
            "variants": ["курс евро", "евро", "скажи курс евро",
                         "euro exchange rate", "euro", "Tell me the euro rate"],
            "answer": euro_exchange
        },
        "bitcoin": {
            "variants": ["курс биткойна", "биткойн", "скажи курс биткойна",
                         "bitcoin exchange rate", "bitcoin", "Tell me the bitcoin rate"],
            "answer": bitcoin_exchange
        },
        "trans_file": {
            "variants": ["переведи файл", "файл перевод", "file перевод", "переведи file",
                         "translate the file", "file translation"],
            "answer": file_translation
        },
        "language": {
            "variants": ["язык смена", "смени язык", "поменяй язык", "смена языка",
                         "change speech language", "language"],
            "answer": change_language
        }
    },

    "failure_phrases": play_phrase
}


if __name__ == "__main__":
    make_preparations()
    while True:
        voice_in = record_and_recognize_audio()
        checking_the_input(voice_in)

        if voice_in:
            per = voice_in.split(" ")
            if(per[0] == "о'кей" and per[1] == "нова"):
                print(colored("Активационная команда получена", "green"))
                listening()
                voice_in = record_and_recognize_audio()

                checking_the_input(voice_in)

                if voice_in:
                    executing_commands()
                else:
                    while not voice_in:
                        checking_the_input(voice_in)
                        voice_in = record_and_recognize_audio()
                        if os.path.exists("microphone-results.wav"):
                            os.remove("microphone-results.wav")
                        print(colored(voice_in, "blue"))
                    executing_commands()

            else:
                print(colored("Ожидание активационной команды...", "yellow"))

