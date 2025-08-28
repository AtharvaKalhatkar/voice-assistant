# ui.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from assistant import process_command, speak
import threading
import speech_recognition as sr
import queue
import sys

# ---------- Config ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # built-in theme

# ---------- Thread-safe UI queue ----------
ui_queue = queue.Queue()

# ---------- Helper: background listener thread ----------
recognizer = sr.Recognizer()
mic = None

def background_listen_loop(running_event):
    """Continuously listen and push commands to ui_queue while running_event is set."""
    global recognizer
    while running_event.is_set():
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=8)
                try:
                    command = recognizer.recognize_google(audio, language="en-in")
                except sr.UnknownValueError:
                    ui_queue.put(("error", "Sorry, I didn't catch that."))
                    continue
                except sr.RequestError:
                    ui_queue.put(("error", "Speech service unavailable."))
                    continue

                ui_queue.put(("user_voice", command))
                # process
                resp = process_command(command)
                ui_queue.put(("assistant", resp))
                if resp == "EXIT":
                    running_event.clear()
                    break
        except sr.WaitTimeoutError:
            # nothing heard within timeout; continue listening
            continue
        except Exception as e:
            ui_queue.put(("error", f"Microphone/listen error: {e}"))
            # small pause to avoid busy loop on errors
            import time
            time.sleep(1)
            continue

# ---------- UI Class ----------
class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✨ Voice Assistant")
        self.geometry("800x650")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # running flag and thread
        self.listener_thread = None
        self.listen_running = threading.Event()

        # Top header
        header_frame = ctk.CTkFrame(self, fg_color="#0f1724")
        header_frame.pack(fill="x", padx=12, pady=12)

        self.logo = ctk.CTkLabel(header_frame, text="★", font=ctk.CTkFont(size=30, weight="bold"), text_color="#00FFB3")
        self.logo.pack(side="left", padx=(10, 8))
        self.title_label = ctk.CTkLabel(header_frame, text="Voice Assistant", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(side="left")

        # Chat area
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.pack(fill="both", expand=True, padx=12, pady=(0,12))

        self.textbox = ctk.CTkTextbox(self.chat_frame, wrap="word", font=("Helvetica", 13))
        self.textbox.pack(fill="both", expand=True, padx=8, pady=8)
        self.textbox.configure(state="disabled")

        # Input area
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=12, pady=(0,16))

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Type a message or press Speak...", width=520)
        self.entry.pack(side="left", padx=(12,8), pady=8, ipady=6, expand=False)

        # Glowing Speak button
        self.speak_btn = ctk.CTkButton(input_frame, text="🎤 Speak (once)", width=150, command=self.speak_once)
        self.speak_btn.pack(side="left", padx=(6,8))

        # Toggle continuous listen
        self.toggle_btn = ctk.CTkButton(input_frame, text="🔴 Start Continuous", width=200, command=self.toggle_listen)
        self.toggle_btn.pack(side="left", padx=(6,12))

        self.send_btn = ctk.CTkButton(input_frame, text="Send", width=100, command=self.send_text)
        self.send_btn.pack(side="right", padx=(0,12))

        # Colors for message types
        self.user_color = "#66d9ff"
        self.assistant_color = "#7bffb2"
        self.system_color = "#ffd166"
        self.error_color = "#ff6b6b"

        # Poll UI queue
        self.after(200, self.process_ui_queue)

        # initial greeting
        self.append_assistant("Hello! I'm ready. Say 'Hey' or press Speak. You can also type below.")

    def append_text(self, tag, text):
        self.textbox.configure(state="normal")
        if tag == "user":
            self.textbox.insert("end", f"You: {text}\n", ("user",))
        elif tag == "assistant":
            if text is None:
                text = ""
            if text == "EXIT":
                self.textbox.insert("end", "Assistant: Goodbye! (closing...)\n", ("assistant",))
            else:
                self.textbox.insert("end", f"Assistant: {text}\n", ("assistant",))
        elif tag == "system":
            self.textbox.insert("end", f"System: {text}\n", ("system",))
        elif tag == "error":
            self.textbox.insert("end", f"Error: {text}\n", ("error",))
        elif tag == "user_voice":
            self.textbox.insert("end", f"You (voice): {text}\n", ("user",))
        self.textbox.configure(state="disabled")
        self.textbox.see("end")

        # configure tags colors (once)
        self.textbox.tag_config("user", foreground=self.user_color)
        self.textbox.tag_config("assistant", foreground=self.assistant_color)
        self.textbox.tag_config("system", foreground=self.system_color)
        self.textbox.tag_config("error", foreground=self.error_color)

    def append_user(self, text):
        self.append_text("user", text)

    def append_assistant(self, text):
        self.append_text("assistant", text)

    def append_system(self, text):
        self.append_text("system", text)

    def append_error(self, text):
        self.append_text("error", text)

    def send_text(self):
        txt = self.entry.get().strip()
        if not txt:
            return
        self.entry.delete(0, "end")
        self.append_user(txt)
        # process synchronously (fast)
        res = process_command(txt)
        if res == "EXIT":
            self.append_assistant("Goodbye! Closing...")
            self.after(700, self.on_close)
            return
        self.append_assistant(res)

    def speak_once(self):
        """Listen once and process."""
        def run_once():
            # disable button while listening
            self.speak_btn.configure(state="disabled")
            self.append_system("Listening...")
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.6)
                    audio = r.listen(source, timeout=6, phrase_time_limit=8)
                    try:
                        text = r.recognize_google(audio, language="en-in")
                        ui_queue.put(("user_voice", text))
                        res = process_command(text)
                        ui_queue.put(("assistant", res))
                        if res == "EXIT":
                            ui_queue.put(("assistant", "EXIT"))
                    except sr.UnknownValueError:
                        ui_queue.put(("error", "Sorry, I didn't catch that."))
                    except sr.RequestError:
                        ui_queue.put(("error", "Speech service unavailable."))
            except Exception as e:
                ui_queue.put(("error", f"Microphone error: {e}"))
            finally:
                self.speak_btn.configure(state="normal")

        threading.Thread(target=run_once, daemon=True).start()

    def toggle_listen(self):
        """Start/stop continuous background listening."""
        if not self.listen_running.is_set():
            # start
            self.listen_running.set()
            self.toggle_btn.configure(text="🟢 Stop Continuous")
            self.append_system("Continuous listening started.")
            self.listener_thread = threading.Thread(target=background_listen_loop, args=(self.listen_running,), daemon=True)
            self.listener_thread.start()
        else:
            # stop
            self.listen_running.clear()
            self.toggle_btn.configure(text="🔴 Start Continuous")
            self.append_system("Continuous listening stopped.")

    def process_ui_queue(self):
        """Check the background queue and update UI accordingly."""
        try:
            while not ui_queue.empty():
                kind, payload = ui_queue.get_nowait()
                if kind == "user_voice":
                    self.append_text("user_voice", payload)
                elif kind == "assistant":
                    if payload == "EXIT":
                        self.append_assistant("Goodbye! Closing...")
                        self.after(800, self.on_close)
                    else:
                        self.append_assistant(payload)
                elif kind == "system":
                    self.append_system(payload)
                elif kind == "error":
                    self.append_error(payload)
                else:
                    self.append_system(str(payload))
        except Exception as e:
            print("UI queue processing error:", e)
        finally:
            # poll again
            self.after(250, self.process_ui_queue)

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the assistant?"):
            # stop background listener if running
            if self.listen_running.is_set():
                self.listen_running.clear()
            self.destroy()
            sys.exit(0)

# ---------- Run app ----------
if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()
