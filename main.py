import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
from AppOpener import open as open_app, close as close_app

# Text to Speech Function
def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

# Speech Listening Function
def take_command():
    r = sr.Recognizer()
    filename = "temp_audio.wav"
    duration = 5  # 5 seconds recording
    sample_rate = 44100

    print("\n--- Listening now... ---")
    try:
        myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        sf.write(filename, myrecording, sample_rate)

        with sr.AudioFile(filename) as source:
            audio = r.record(source)
            print("Recognizing speech...")
            
            # Try recognizing in English first, then Arabic
            try:
                query = r.recognize_google(audio, language='en-US')
                print(f"User said: {query}\n")
            except Exception:
                query = r.recognize_google(audio, language='ar-SA')
                print(f"User said: {query}\n")

    except Exception:
        query = "None"
    finally:
        if os.path.exists(filename):
            os.remove(filename)

    return query

# Local Question Processing (معالجة الأسئلة محلية بدون جمناي)
def process_local_query(query):
    query = query.lower()

    # Time & Date
    if 'time' in query or 'الوقت' in query or 'الساعة' in query:
        str_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {str_time}")

    elif 'date' in query or 'تاريخ' in query:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today is {today}")

    # General Questions / Greeting
    elif 'how are you' in query or 'كيف حالك' in query:
        speak("I am doing great and ready to help you!")

    elif 'who are you' in query or 'من انت' in query:
        speak("I am your local voice assistant for controlling this PC.")

    elif 'your name' in query or 'اسمك' in query:
        speak("I am your personal Python desktop assistant.")

    # Controlling PC Apps (فتح وأغلاق التطبيقات داخل اللابتوب)
    elif 'open' in query or 'افتح' in query:
        # Extract app name after the word 'open' or 'افتح'
        app_name = query.replace("open", "").replace("افتح", "").strip()
        
        # Web Shortcuts
        if 'youtube' in app_name or 'يوتيوب' in app_name:
            speak("Opening Youtube")
            webbrowser.open("https://www.youtube.com")
        elif 'google' in app_name or 'جوجل' in app_name:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif 'telegram' in app_name or 'تليجرام' in app_name:
            speak("Opening Telegram")
            webbrowser.open("https://web.telegram.org")
        else:
            # Open Installed Software on Laptop (Chrome, Word, Excel, VS Code, Paint, Notepad, etc.)
            speak(f"Opening {app_name}")
            try:
                open_app(app_name, match_closest=True)
            except Exception as e:
                speak(f"Could not find or open application {app_name}")

    # Close Application
    elif 'close' in query or 'أغلق' in query or 'احذف' in query:
        app_name = query.replace("close", "").replace("أغلق", "").strip()
        speak(f"Closing {app_name}")
        try:
            close_app(app_name, match_closest=True)
        except Exception:
            speak(f"Could not close {app_name}")

    # Unrecognized Query
    else:
        speak("Command not recognized in local system.")

# Main Loop
def run_assistant():
    speak("Hello! I am ready to control your PC.")
    
    while True:
        query = take_command().lower()

        if query == "none" or query == "":
            time.sleep(1)
            continue

        # System Exit
        if any(word in query for word in ['exit', 'bye', 'stop', 'close assistant']):
            speak("Goodbye! Have a great day.")
            break

        # Process Query Locally
        process_local_query(query)

if __name__ == "__main__":
    run_assistant()