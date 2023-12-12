import tkinter as tk
from gtts import gTTS
import os
import speech_recognition as sr
from pydub import AudioSegment
from tkinter import filedialog


class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech and Speech-to-Text App")

        # initialize variables
        self.dark_mode = tk.BooleanVar()
        self.dark_mode.set(False)
        self.recognizer = sr.Recognizer()
        self.microphone_list = sr.Microphone.list_microphone_names()

        # initialize variables
        self.output_formats = ["mp3", "wav"]
        self.selected_format = tk.StringVar(value=self.output_formats[0])

        # create GUI
        self.create_widgets()

    def create_widgets(self):
        # text input
        self.text_input = tk.Text(self.root, wrap=tk.WORD, width=50, height=10)
        self.text_input.pack(pady=10)

        # speech to text buttons
        stt_button = tk.Button(self.root, text="Start Speech to Text", command=self.start_speech_to_text)
        stt_button.pack(side=tk.LEFT, padx=5)

        stop_button = tk.Button(self.root, text="Stop Speech to Text", command=self.stop_speech_to_text)
        stop_button.pack(side=tk.LEFT, padx=5)

        # microphone selection
        mic_label = tk.Label(self.root, text="Select Microphone:")
        mic_label.pack(side=tk.LEFT, padx=5)
        self.selected_microphone = tk.StringVar()
        mic_dropdown = tk.OptionMenu(self.root, self.selected_microphone, *self.microphone_list)
        mic_dropdown.pack(side=tk.LEFT, padx=5)
        self.selected_microphone.set(self.microphone_list[0])  # Default selection

        # text to speech button
        tts_button = tk.Button(self.root, text="Text to Speech", command=self.text_to_speech)
        tts_button.pack()

        # Dark/Light mode toggle
        mode_button = tk.Button(self.root, text="🌞", command=self.toggle_mode)
        mode_button.pack()

        # text to speech button (fix)
        tts_button = tk.Button(self.root, text="Text to Speech", command=self.text_to_speech)
        tts_button.pack()

        # import button
        import_button = tk.Button(self.root, text="Import Audio File", command=self.import_audio_file)
        import_button.pack()

        # format selection
        format_label = tk.Label(self.root, text="Select Output Format:")
        format_label.pack(side=tk.LEFT, padx=5)
        format_dropdown = tk.OptionMenu(self.root, self.selected_format, *self.output_formats)
        format_dropdown.pack(side=tk.LEFT, padx=5)

    def start_speech_to_text(self):
        with sr.Microphone(device_index=self.microphone_list.index(self.selected_microphone.get())) as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio)
                self.text_input.insert(tk.END, text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    def stop_speech_to_text(self):
        try:
            self.recognizer.thread.join()
        except sr.UnknownValueError:
            print("Google speech could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        print("Speech-to-Text stopped.")



    def text_to_speech(self):
        text = self.text_input.get("1.0", tk.END).strip()

        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        os.system("start output.mp3")  

    def toggle_mode(self):
        self.dark_mode.set(not self.dark_mode.get())
        mode = "Dark" if self.dark_mode.get() else "Light"
        self.root.configure(bg="#1e1e1e" if self.dark_mode.get() else "white")
        print(f"Switched to {mode} mode.")

    def import_audio_file(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.mp4;*.mpeg;*.mpga;*.m4a;*.wav;*.webm")])
        if file_path:
            self.play_audio_file(file_path)

    def play_audio_file(self, file_path):
        self.convert_audio_format(file_path)

    def convert_audio_format(self, input_path):
        sound = AudioSegment.from_file(input_path)
        output_format = self.selected_format.get()
        output_path = f"output.{output_format}"
        sound.export(output_path, format=output_format)
        os.system(f"start {output_path}")  


if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
