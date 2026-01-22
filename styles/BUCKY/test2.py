import speech_recognition as sr
import pyttsx3
import os
import subprocess
import webbrowser
from pytube import Search  # For YouTube search
import nltk
from nltk.tokenize import word_tokenize

# Initialize speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Configurable search directories (add your common folders here to speed up; e.g., home dir)
SEARCH_DIRS = [os.path.expanduser('~'), os.path.expanduser('~/Downloads'), os.path.expanduser('~/Videos')]

# Optional: Your YouTube channel name for filtering (change this if needed)
YOUR_CHANNEL = "YourChannelNameHere"  # Set to None if not filtering by channel

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Speech service is down.")
            return None

def parse_command(command):
    tokens = word_tokenize(command)
    action = None
    target = " ".join(tokens[1:])  # Simple: assume first word is action, rest is target name

    if "play" in tokens:
        action = "play"
    elif "open" in tokens:
        action = "open"
    elif "run" in tokens:
        action = "run"
    else:
        speak("Invalid action. Say play, open, or run.")
        return None, None

    return action, target

def search_local_file(target_name):
    for root_dir in SEARCH_DIRS:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if target_name.lower() in file.lower():  # Fuzzy match; adjust for exact if needed
                    return os.path.join(root, file)
            for dir in dirs:
                if target_name.lower() in dir.lower():
                    return os.path.join(root, dir)  # Return folder path if it's a folder
    return None

def handle_local(action, path):
    if path is None:
        speak("File or folder not found.")
        return

    try:
        if action == "open" or action == "play":
            # Cross-platform open/play
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.call(['open', path])  # macOS; use 'xdg-open' for Linux
        elif action == "run":
            # For executables/scripts
            subprocess.Popen(path, shell=True)
        speak(f"{action.capitalize()}ing {os.path.basename(path)}.")
    except Exception as e:
        speak(f"Error: {str(e)}")

def handle_youtube(target_name):
    try:
        query = target_name
        if YOUR_CHANNEL:
            query += f" {YOUR_CHANNEL}"  # Append channel for better relevance
        search_results = Search(query).results
        if search_results:
            video = search_results[0]  # Take the first match; you can add logic for best match
            url = video.watch_url
            # Open in browser to "play"
            webbrowser.open(url)
            speak(f"Playing {target_name} on YouTube.")
        else:
            speak("No YouTube video found.")
    except Exception as e:
        speak(f"Error searching YouTube: {str(e)}")

def main():
    speak("Bucky online. How can I help?")
    while True:
        command = listen()
        if command:
            action, target = parse_command(command)
            if action and target:
                # Check if it's likely YouTube (e.g., command mentions "video" or "youtube")
                if "video" in command or "youtube" in command:
                    handle_youtube(target)
                else:
                    # Assume local file/folder
                    path = search_local_file(target)
                    handle_local(action, path)

if __name__ == "__main__":
    main()