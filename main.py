import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import google.generativeai as genai  # Import the Gemini API library
import pyaudio
import os



genai.configure(api_key="AIzaSyCfnKsEBuvWgsT0cSWZA9vWJzmG9y2AfEI") # Replace with your Gemini API key

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Speech service is down.")
        speak("Speech service is down.")
        return ""


def get_gemini_response(command):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')  # Or the correct model name
        response = model.generate_content(command) # Correct usage of generate_content
        return response.text.strip()

    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        return "Sorry, I encountered an error with Gemini."
def respond_to_command(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")

    elif " open wikipedia" in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results, please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("No results found.")

    elif "open youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("http://www.youtube.com")

    elif "open spotify" in command:
        speak("Opening Spotify...")
        webbrowser.open("http://www.spotify.com")

    elif "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    else:
        chat_response = get_gemini_response(command)
        print(f"Gemini says: {chat_response}")
        speak(chat_response)


        speak("thank you")


if __name__ == "__main__":
    speak("Hello I am JARVIS .")
    while True:
        user_command = listen()
        if user_command:
            respond_to_command(user_command)