import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import os
import geocoder
from geopy.geocoders import Nominatim
import sys

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)

class ConversationTranslator:
    def __init__(self, master):
        self.master = master
        self.master.title("Conversation Translator")
        self.master.geometry("800x400")

        self.translator = Translator()
        self.recognizer = sr.Recognizer()

        self.frame = ttk.Frame(master=self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.heading = ttk.Label(master=self.frame, text="Talkbro-ai", font=("Arial", 24, "bold"))
        self.heading.pack(padx=10, pady=12)

        self.console_output = tk.Text(self.frame, wrap=tk.WORD, height=5, width=50)
        self.console_output.pack(padx=10, pady=12, anchor="w", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.console_output.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.console_output.config(yscrollcommand=self.scrollbar.set)

        self.source_label = ttk.Label(master=self.frame, text="Source Person:")
        self.source_label.pack(padx=10, pady=12)

        self.source_language_var = tk.StringVar()
        self.source_language_menu = ttk.Combobox(master=self.frame, textvariable=self.source_language_var, values=["English", "Tamil", "Kannada"])
        self.source_language_menu.pack(padx=10, pady=12)
        self.source_language_menu.current(0)

        self.source_text = tk.Text(master=self.frame, wrap="word", height=4, width=40)
        self.source_text.pack(padx=10, pady=12)

        self.speech_to_text_button = ttk.Button(master=self.frame, text="Speech to Text", command=self.speech_to_text)
        self.speech_to_text_button.pack(padx=10, pady=12)

        self.target_label = ttk.Label(master=self.frame, text="Target Person:")
        self.target_label.pack(padx=10, pady=12)

        self.target_language_var = tk.StringVar()
        self.target_language_menu = ttk.Combobox(master=self.frame, textvariable=self.target_language_var, values=["English", "Tamil", "Kannada"])
        self.target_language_menu.pack(padx=10, pady=12)
        self.target_language_menu.current(1)  

        self.target_text = tk.Text(master=self.frame, wrap="word", height=4, width=40)
        self.target_text.pack(padx=10, pady=12)

        self.translate_button = ttk.Button(master=self.frame, text="Translate", command=self.translate)
        self.translate_button.pack(padx=10, pady=12)

        self.speak_button = ttk.Button(master=self.frame, text="Speak", command=self.speak)
        self.speak_button.pack(padx=10, pady=12)

        self.clear_button = ttk.Button(master=self.frame, text="Reply", command=self.clear_text)
        self.clear_button.pack(padx=10, pady=12)

        self.geolocation_label = ttk.Label(master=self.frame, text="Geolocation:")
        self.geolocation_label.pack(padx=10, pady=12)

        self.geolocation_text = ttk.Label(master=self.frame, text="Address:")
        self.geolocation_text.pack(padx=10, pady=12)

        self.address_label = ttk.Label(master=self.frame, text="Address:")
        self.address_label.pack(padx=10, pady=12)

        self.address_text = ttk.Label(master=self.frame, text="")
        self.address_text.pack(padx=10, pady=12)

        # Redirect console output to text widget
        sys.stdout = ConsoleRedirector(self.console_output)

        self.get_current_location()

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            self.source_text.insert(tk.END, text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error fetching results; {0}".format(e))

    def translate(self):
        source_language = self.source_language_menu.get()
        target_language = self.target_language_menu.get()
        text = self.source_text.get("1.0", tk.END)

        translated_text = self.translator.translate(text, src=source_language, dest=target_language).text
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert(tk.END, translated_text)

    def speak(self):
        source_language = self.target_language_menu.get()
        target_language = 'en'
        text = self.target_text.get("1.0", tk.END)

        translated_text = self.translator.translate(text, src=source_language, dest=target_language).text
        tts = gTTS(text=translated_text, lang='en')
        tts.save("translated_text.mp3")
        os.system("start translated_text.mp3")

    def clear_text(self):
        self.source_text.delete("1.0", tk.END)
        self.target_text.delete("1.0", tk.END)
        # Swap source and target languages
        current_source = self.source_language_menu.get()
        current_target = self.target_language_menu.get()
        self.source_language_menu.set(current_target)
        self.target_language_menu.set(current_source)

    def get_current_location(self):
        try:
            g = geocoder.ip('me')
            latitude = g.latlng[0]
            longitude = g.latlng[1]
            print('Latitude:', latitude)
            print('Longitude:', longitude)
        
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse((latitude, longitude), language="en")
            self.geolocation_text.config(text=f"Latitude: {latitude}\nLongitude: {longitude}")
            self.address_text.config(text=location.address)
        except Exception as e:
            print("Error fetching location:", e)

def main():
    root = tk.Tk()
    app = ConversationTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
