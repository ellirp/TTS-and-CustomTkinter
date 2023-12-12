import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window title + size
        self.title("Speech to Text and Text to Speech")
        self.geometry(f"{1100}x{580}")

        # layout
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure((3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=9, sticky="nsew") 
        self.sidebar_frame.grid_rowconfigure(9, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Voice Recognition", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        
        self.mic_option = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Microphone 1", "Microphone 2", "Microphone 3"])
        self.mic_option.grid(row=1, column=0, padx=20, pady=(20, 10)) 
        # record and pause buttons
        self.record_button = customtkinter.CTkButton(self.sidebar_frame, text="Record", command=self.record_button_event, state='normal')
        self.record_button.grid(row=2, column=0, padx=20, pady=10)
        self.pause_button = customtkinter.CTkButton(self.sidebar_frame, text="Pause", command=self.pause_button_event, state='disabled')
        self.pause_button.grid(row=3, column=0, padx=20, pady=10)

        self.upload_button = customtkinter.CTkButton(self.sidebar_frame, text="Upload", command=self.upload_button_event)
        self.upload_button.grid(row=4, column=0, padx=20, pady=10)

        #dark/light mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        #UI Scale
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #transcription box
        self.textbox = customtkinter.CTkTextbox(self, width=400)
        self.textbox.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        #audio combobox
        combobox_frame = customtkinter.CTkFrame(self)
        combobox_frame.grid(row=0, column=1, rowspan=5, padx=(20, 20), pady=(20, 240), sticky="nsew")
        combobox_frame.grid_rowconfigure(5, weight=1)

        

        self.choose_output = customtkinter.CTkComboBox(combobox_frame, values=["Mp3", "Mp4", "WAV"])
        self.choose_output.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")

        self.choose_language = customtkinter.CTkComboBox(combobox_frame, values=["English", "Spanish", "Etc."])
        self.choose_language.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="n")

        self.export_button = customtkinter.CTkButton(combobox_frame, text="Export", command=self.export_button_event)
        self.export_button.grid(row=3, column=0, padx=20, pady=10)

        #transcription combobox
        combobox_frame = customtkinter.CTkFrame(self)
        combobox_frame.grid(row=0, column=2, rowspan=5, padx=(20, 20), pady=(20, 240), sticky="nsew")
        combobox_frame.grid_rowconfigure(5, weight=1)

        self.choose_language_text = customtkinter.CTkComboBox(combobox_frame, values=["English", "Spanish", "Etc."])
        self.choose_language_text.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="n")

        self.transcribe_button = customtkinter.CTkButton(combobox_frame, text="Transcribe", command=self.transcribe_button_event)
        self.transcribe_button.grid(row=3, column=0, padx=20, pady=10)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.choose_output.set("Choose Output")
        self.choose_language.set("Choose Language")
        self.choose_language_text.set("Choose Language")
        self.textbox.insert("0.0", "Transcribed Text:\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def record_button_event(self):
        print("Record button clicked")

        self.pause_button.configure(state= 'normal')
        self.record_button.configure(state= 'disabled')

    def pause_button_event(self):
        print("Pause button clicked")

        self.pause_button.configure(state= 'disabled')
        self.record_button.configure(state= 'normal')
    
    def transcribe_button_event(self):
        print("Transcribe button clicked")
        audio_text = self.transcribe_audio()
        self.textbox.delete("1.0", tkinter.END)
        self.textbox.insert(tkinter.END, f"Transcribed Text:\n\n{audio_text}")

    def upload_button_event(self):
        print("Upload button clicked")

    def export_button_event(self):
        print("Export button clicked")

    

if __name__ == "__main__":
    app = App()
    app.mainloop()