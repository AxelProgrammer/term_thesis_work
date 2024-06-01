# машинное обучения
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

import os  # работа с файловой системой (file system operations)
import tkinter as tk #графика
from tkinter import scrolledtext #графика
import wave  # создание и чтение аудиофайлов формата wav (creation and reading of WAV audio files)
import json  # работа с json-файлами и json-строками (working with JSON files and JSON strings)
import traceback  # вывод traceback без остановки работы программы при отлове исключений (outputting traceback without stopping program execution when catching exceptions)
import webbrowser  # работа с использованием браузера по умолчанию (открывание вкладок с web-страницей) (interaction with the default web browser - opening tabs with web pages)
import random  # генератор случайных чисел (random number generator)
import wikipediaapi  # поиск определений в Wikipedia (searching for definitions on Wikipedia)
import pyttsx3  # синтез речи (Text-To-Speech) (speech synthesis - Text-To-Speech)
import googletrans  # использование системы Google Translate (utilization of the Google Translate system)
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text) (speech recognition - Speech-To-Text)
from dotenv import load_dotenv  # загрузка информации из .env-файла (loading information from .env files)
from termcolor import colored  # вывод цветных логов (для выделения распознанной речи) (displaying colored logs - for highlighting recognized speech)
from pyowm import OWM  # использование OpenWeatherMap для получения данных о погоде (utilizing OpenWeatherMap to retrieve weather data)
from googlesearch import search  # поиск в Google (performing searches on Google)
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk (offline speech recognition by Vosk)

load_dotenv()
class Translation:
    with open("translations.json", "r", encoding="UTF-8") as file:
        translations = json.load(file)

    def get(self, text: str):
        if text in self.translations:
            return self.translations[text][assistant.speech_language]
        else:
            # в случае отсутствия перевода происходит вывод сообщения об этом в логах и возврат исходного текста
            print(colored("Not translated phrase: {}".format(text), "red"))
            return text


class OwnerPerson:
    # Информация о владельце
    name = ""
    home_city = ""
    native_language = ""
    target_language = ""


class VoiceAssistant:
    # Настройки голосового ассистента
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""


def setup_assistant_voice():
    # Установка голоса по умолчанию
    voices = ttsEngine.getProperty("voices")

    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            # Microsoft Zira Desktop
            ttsEngine.setProperty("voice", voices[1].id)
        else:
            # Microsoft David Desktop
            ttsEngine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru-RU"
        # Microsoft Irina Desktop
        ttsEngine.setProperty("voice", voices[0].id)


def record_and_recognize_audio(*args: tuple):
    # Запись и распознавание аудио
    with microphone:
        recognized_data = ""
        # запоминание шумов окружения для последующей очистки звука от них
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            play_voice_assistant_speech(translator.get("Can you check if your microphone is on, please?"))
            traceback.print_exc()
            return

        # использование online-распознавания через Google (высокое качество распознавания)
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language=assistant.recognition_language).lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print(colored("Trying to use offline recognition...", "cyan"))
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    # Переключение на оффлайн-распознавание речи
    recognized_data = ""
    try:
        # проверка наличия модели на нужном языке в каталоге приложения
        if not os.path.exists("models/vosk-model-small-" + assistant.speech_language + "-0.4"):
            print(colored("Please download the model from:\n"
                          "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.",
                          "red"))
            exit(1)

        # анализ записанного в микрофон аудио
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("models/vosk-model-small-" + assistant.speech_language + "-0.4")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                # получение данных распознанного текста из JSON-строки
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        traceback.print_exc()
        print(colored("Sorry, speech service is unavailable. Try again later", "red"))

    return recognized_data


def play_voice_assistant_speech(text_to_speech):
    # Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def play_failure_phrase(*args: tuple):
    # в случае ошибки распознания
    failure_phrases = [
        translator.get("Can you repeat, please?"),
        translator.get("What did you say again?")
    ]
    play_voice_assistant_speech(failure_phrases[random.randint(0, len(failure_phrases) - 1)])


def play_greetings(*args: tuple):
    # случайное приветствие
    greetings = [
        translator.get("Hello, {}! How can I help you today?").format(person.name),
        translator.get("Good day to you {}! How can I help you today?").format(person.name)
    ]
    play_voice_assistant_speech(greetings[random.randint(0, len(greetings) - 1)])

def play_joke(*args: tuple):
    # случайное приветствие
    joke = [
        translator.get("Why did the robot get angry? Everyone kept pushing their buttons!").format(person.name),
        translator.get("Be careful of robots! They byte!").format(person.name)
    ]
    play_voice_assistant_speech(joke[random.randint(0, len(joke) - 1)])

def listening(*args: tuple):
    # случайное приветствие
    listening = [
        translator.get("I'm listening").format(person.name),
        translator.get("I'm listening to you carefully").format(person.name)
    ]
    play_voice_assistant_speech(listening[random.randint(0, len(listening) - 1)])

def play_farewell_and_quit(*args: tuple):
    # случайное прощание
    farewells = [
        translator.get("Goodbye, {}! Have a nice day!").format(person.name),
        translator.get("See you soon, {}!").format(person.name)
    ]
    play_voice_assistant_speech(farewells[random.randint(0, len(farewells) - 1)])
    ttsEngine.stop()
    quit()


def search_for_term_on_google(*args: tuple):
    if not args or not args[0]:
        print("obviously, you didn't name the request after the command")
        return

    search_term = " ".join(args[0])

    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)

    search_results = []
    try:
        for result in search(search_term,
                             tld="com",
                             lang=assistant.speech_language,
                             num=1,
                             start=0,
                             stop=1,
                             pause=1.0):
            search_results.append(result)
            webbrowser.get().open(result)

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return

    print("Search results:", search_results)
    print("Here is what I found for '{}' on Google.".format(search_term))

def search_for_video_on_youtube(*args):
    # Поиск видео на YouTube
    if not args or not args[0]:
        print("Вы не ввели запрос:")
        return
    search_term = " ".join(args[0])  # Joining the first element of args assuming it's a list of strings
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    play_voice_assistant_speech(translator.get("Here is what I found for {} on youtube").format(search_term))

def search_for_definition_on_wikipedia(*args: tuple):
    # Поиск в Wikipedia
    if not args[0]: return

    search_term = " ".join(args[0])

    # установка языка
    wiki = wikipediaapi.Wikipedia(assistant.speech_language)

    # поиск страницы по запросу
    wiki_page = wiki.page(search_term)
    try:
        if wiki_page.exists():
            play_voice_assistant_speech(translator.get("Here is what I found for {} on Wikipedia").format(search_term))
            webbrowser.get().open(wiki_page.fullurl)

            # чтение ассистентом первых двух предложений summary со страницы Wikipedia
            play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
        else:
            # открытие ссылки на поисковик в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
            play_voice_assistant_speech(translator.get(
                "Can't find {} on Wikipedia. But here is what I found on google").format(search_term))
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)

    # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    except:
        play_voice_assistant_speech(translator.get("Seems like we have a trouble. See logs for more information"))
        traceback.print_exc()
        return


def get_translation(*args: tuple):
    """
    Получение перевода текста с одного языка на другой (в данном случае с изучаемого на родной язык или обратно)
    :param args: фраза, которую требуется перевести
    """
    if not args[0]: return

    search_term = " ".join(args[0])
    google_translator = googletrans.Translator()
    translation_result = ""

    old_assistant_language = assistant.speech_language
    try:
        # если язык речи ассистента и родной язык пользователя различаются, то перевод выполяется на родной язык
        if assistant.speech_language != person.native_language:
            translation_result = google_translator.translate(search_term,  # что перевести
                                                             src=person.target_language,  # с какого языка
                                                             dest=person.native_language)  # на какой язык

            play_voice_assistant_speech("The translation for {} in Russian is".format(search_term))

            # смена голоса ассистента на родной язык пользователя (чтобы можно было произнести перевод)
            assistant.speech_language = person.native_language
            setup_assistant_voice()

        # если язык речи ассистента и родной язык пользователя одинаковы, то перевод выполяется на изучаемый язык
        else:
            translation_result = google_translator.translate(search_term,  # что перевести
                                                             src=person.native_language,  # с какого языка
                                                             dest=person.target_language)  # на какой язык
            play_voice_assistant_speech("По-английски {} будет как".format(search_term))

            # смена голоса ассистента на изучаемый язык пользователя (чтобы можно было произнести перевод)
            assistant.speech_language = person.target_language
            setup_assistant_voice()

        # произнесение перевода
        play_voice_assistant_speech(translation_result.text)

    # поскольку все ошибки предсказать сложно, то будет произведен отлов с последующим выводом без остановки программы
    except:
        play_voice_assistant_speech(translator.get("Seems like we have a trouble. See logs for more information"))
        traceback.print_exc()

    finally:
        # возвращение преждних настроек голоса помощника
        assistant.speech_language = old_assistant_language
        setup_assistant_voice()

def change_language(*args: tuple):
    # Изменение языка
    assistant.speech_language = "ru" if assistant.speech_language == "en" else "en"
    setup_assistant_voice()
    print(colored("Language switched to " + assistant.speech_language, "cyan"))


def run_person_through_social_nets_databases(*args: tuple):
    if not args[0]: return

    google_search_term = " ".join(args[0])
    vk_search_term = "_".join(args[0])
    fb_search_term = "-".join(args[0])

    # открытие ссылки на поисковик в браузере
    url = "https://google.com/search?q=" + google_search_term + " site: vk.com"
    webbrowser.get().open(url)

    url = "https://google.com/search?q=" + google_search_term + " site: facebook.com"
    webbrowser.get().open(url)

    # открытие ссылкок на поисковики социальных сетей в браузере
    vk_url = "https://vk.com/people/" + vk_search_term
    webbrowser.get().open(vk_url)

    fb_url = "https://www.facebook.com/public/" + fb_search_term
    webbrowser.get().open(fb_url)

    play_voice_assistant_speech(translator.get("Here is what I found for {} on social nets").format(google_search_term))


def toss_coin(*args: tuple):
    """
    "Подбрасывание" монетки для выбора из 2 опций
    """
    flips_count, heads, tails = 3, 0, 0

    for flip in range(flips_count):
        if random.randint(0, 1) == 0:
            heads += 1

    tails = flips_count - heads
    winner = "Tails" if tails > heads else "Heads"
    play_voice_assistant_speech(translator.get(winner) + " " + translator.get("won"))


# перечень команд для использования в виде JSON-объекта
config = {
    "intents": {
        "greeting": {
            "examples": ["привет", "здравствуй", "добрый день",
                         "hello", "good morning"],
            "responses": play_greetings
        },
        "joke": {
            "examples": ["шутка", "скажи шутку", "придумай шутку",
                         "joke", "Tell a joke", "Come up with a joke"],
            "responses": play_joke
        },
        "farewell": {
            "examples": ["пока", "до свидания", "увидимся", "до встречи",
                         "goodbye", "bye", "see you soon"],
            "responses": play_farewell_and_quit
        },
        "wikipedia_search": {
            "examples": ["найди определение", "найди на википедии",
                         "find on wikipedia", "find definition", "tell about"],
            "responses": search_for_definition_on_wikipedia
        },
        "person_search": {
            "examples": ["пробей имя", "найди человека",
                         "find on facebook", " find person", "run person", "search for person"],
            "responses": run_person_through_social_nets_databases
        },
        "toss_coin": {
            "examples": ["подбрось монетку", "подкинь монетку",
                         "toss coin", "coin", "flip a coin"],
            "responses": toss_coin
        },
        "google_search": {
            "examples": ["найди в гугл", "гугл",
                         "search on google", "google", "find on google"],
            "responses": search_for_term_on_google
        },
        "youtube_search": {
            "examples": ["найди видео", "покажи видео",
                         "find video", "find on youtube", "search on youtube"],
            "responses": search_for_video_on_youtube
        },
        "translation": {
            "examples": ["выполни перевод", "переведи", "найди перевод",
                         "translate", "find translation"],
            "responses": get_translation
        },
        "language": {
            "examples": ["смени язык", "поменяй язык", "смена языка",
                         "change speech language", "language"],
            "responses": change_language
        }
    },

    "failure_phrases": play_failure_phrase
}


def prepare_corpus():
    # Подготовка модели для угадывания намерения пользователя
    corpus = []
    target_vector = []
    for intent_name, intent_data in config["intents"].items():
        for example in intent_data["examples"]:
            corpus.append(example)
            target_vector.append(intent_name)

    training_vector = vectorizer.fit_transform(corpus)
    classifier_probability.fit(training_vector, target_vector)
    classifier.fit(training_vector, target_vector)


def get_intent(request):
    # Получение наиболее вероятного намерения в зависимости от запроса пользователя

    best_intent = classifier.predict(vectorizer.transform([request]))[0]

    index_of_best_intent = list(classifier_probability.classes_).index(best_intent)
    probabilities = classifier_probability.predict_proba(vectorizer.transform([request]))[0]

    best_intent_probability = probabilities[index_of_best_intent]

    # при добавлении новых намерений стоит уменьшать этот показатель
    # близость к предсказанному значению
    # print(best_intent_probability)
    if best_intent_probability > 0.157:
        return best_intent


def make_preparations():
    # Подготовка глобальных переменных к запуску приложения
    global recognizer, microphone, ttsEngine, person, assistant, translator, vectorizer, classifier_probability, classifier

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # настройка данных пользователя
    person = OwnerPerson()
    person.name = "Аксель"
    person.home_city = "Москва"
    person.native_language = "ru"
    person.target_language = "en"

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = "Nova"
    assistant.sex = "female"
    assistant.speech_language = "ru"

    # установка голоса по умолчанию
    setup_assistant_voice()

    # добавление возможностей перевода фраз (из заготовленного файла)
    translator = Translation()

    # загрузка информации из .env-файла (там лежит API-ключ для OpenWeatherMap)
    load_dotenv()

    # подготовка корпуса для распознавания запросов пользователя с некоторой вероятностью (поиск похожих)
    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    classifier_probability = LogisticRegression()
    classifier = LinearSVC()
    prepare_corpus()

def checking_offers(voice_input_parts):
    if len(voice_input_parts) > 1:
        for guess in range(len(voice_input_parts)):
            intent = get_intent((" ".join(voice_input_parts[0:guess])).strip())
            print(intent)
            if intent:
                command_options = [voice_input_parts[guess:len(voice_input_parts)]]
                print(command_options)
                config["intents"][intent]["responses"](*command_options)
                break
            if not intent and guess == len(voice_input_parts) - 1:
                config["failure_phrases"]()

def executing_commands():
    voice_input_parts = voice_input.split(" ")

    # если было сказано одно слово - выполняем команду сразу без дополнительных аргументов
    if len(voice_input_parts) == 1:
        intent = get_intent(voice_input)
        if intent:
            config["intents"][intent]["responses"]()
        else:
            config["failure_phrases"]()

    # в случае длинной фразы - выполняется поиск ключевой фразы и аргументов через каждое слово,
    # пока не будет найдено совпадение
    checking_offers(voice_input_parts)

def checking_the_input(voice_input):
    if os.path.exists("microphone-results.wav"):
        os.remove("microphone-results.wav")

    print(colored(voice_input, "blue"))



if __name__ == "__main__":
    make_preparations()
    while True:
        # старт записи речи
        voice_input = record_and_recognize_audio()
        checking_the_input(voice_input)

        if voice_input:
            per = voice_input.split(" ")
            if(per[0] == "о'кей" and per[1] == "нова"):
                print(colored("Активационная команда получена", "green"))
                listening()
                voice_input = record_and_recognize_audio()

                checking_the_input(voice_input)

                # отделение комманд от дополнительной информации (аргументов)
                if voice_input:
                    executing_commands()
                else:
                    while not voice_input:
                        checking_the_input()
                        voice_input = record_and_recognize_audio()
                        if os.path.exists("microphone-results.wav"):
                            os.remove("microphone-results.wav")
                        print(colored(voice_input, "blue"))
                    executing_commands()

            else:
                print(colored("Ожидание активационной команды...", "yellow"))

