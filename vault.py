import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageSequence
import threading
import time
import speech_recognition as sr
import pygame

# --- CONFIGURATIONS ---
VOICE_PASSWORD = "open my vault"
BACKGROUND_MP3 = "theme.mp3"
UNLOCKED_WAV = "voice.mp3"
LOCK_ANIMATION_GIF = "lock.gif"

# --- PLAY BACKGROUND MUSIC ---
def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load(BACKGROUND_MP3)
    pygame.mixer.music.play(-1)  # Loop forever

# --- PLAY UNLOCKED MESSAGE ---
def play_unlocked_voice():
    effect = pygame.mixer.Sound(UNLOCKED_WAV)
    effect.play()

# --- HANDLE VOICE INPUT ---
def listen_for_password():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎙️ Listening for your command...")
        root.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            print("Recognized:", text)  # For debugging
            if text == VOICE_PASSWORD:
                status_label.config(text="✅ Password matched. Unlocking vault...")
                root.update()
                threading.Thread(target=unlock_vault).start()
            else:
                status_label.config(text=f"❌ Incorrect password: {text}")
        except Exception as e:
            status_label.config(text=f"⚠️ Could not recognize. {str(e)}")

# --- UNLOCK SEQUENCE ---
def unlock_vault():
    play_unlocked_voice()
    play_gif_animation()
    show_personal_info()

# --- PLAY GIF FRAME BY FRAME ---
def play_gif_animation():
    global lock_gif
    for frame in ImageSequence.Iterator(lock_gif):
        frame_image = ImageTk.PhotoImage(frame.resize((window_width, window_height)))
        gif_label.config(image=frame_image)
        gif_label.image = frame_image
        time.sleep(0.04)

# --- SHOW PERSONAL INFO ---
def show_personal_info():
    gif_label.pack_forget()
    status_label.pack_forget()
    speak_button.pack_forget()

    details_frame = tk.Frame(root, bg="#1a1a1a")
    details_frame.pack(fill="both", expand=True)

    tk.Label(details_frame, text="🔓 Vault Unlocked", font=("Segoe UI", 28, "bold"), fg="white", bg="#1a1a1a").pack(pady=30)

    info_lines = [
        "Name: Rachamalla Murari",
        "Email: rachamallamurari@email.com",
        "DOB: 03-Oct-2002",
        "Phone: 9347557573",
        "Location: Hyderabad",
        "Role: House - Son",
        "Siblings:Sister",
        "Interests:Tech",
        "           Movies",
        "           Trekking"
    ]

    for line in info_lines:
        tk.Label(details_frame, text=line, font=("Consolas", 16), fg="white", bg="#1a1a1a", justify="left").pack(pady=6)

# --- GUI SETUP ---
root = tk.Tk()
root.title("VoiceLock Vault")
root.configure(bg="#1a1a1a")
root.attributes("-fullscreen", True)

# Full screen size
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

# Load the GIF
lock_gif = Image.open(LOCK_ANIMATION_GIF)
frame = ImageTk.PhotoImage(lock_gif.resize((window_width, window_height)))
gif_label = tk.Label(root, image=frame, bg="#1a1a1a")
gif_label.pack()

# Status text
status_label = tk.Label(root, text="", fg="white", bg="#1a1a1a", font=("Segoe UI", 16))
status_label.place(relx=0.5, rely=0.05, anchor="n")

# Speak Button
speak_button = tk.Button(root, text="🔊 Tap to Speak Passkey", command=listen_for_password,
                         font=("Segoe UI", 14, "bold"), bg="#333", fg="white", padx=20, pady=10)
speak_button.place(relx=0.5, rely=0.75, anchor="center")

# Start background music
threading.Thread(target=play_background_music, daemon=True).start()

# Start the app
root.mainloop()
