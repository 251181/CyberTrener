import pyttsx3

engine = pyttsx3.init()

# Wybór polskiego głosu (jeśli jest dostępny)
for voice in engine.getProperty('voices'):
    if "pl" in voice.id.lower() or "pol" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

# Tekst do wypowiedzenia
engine.say("Cześć! To jest polski głos działający offline.")
engine.runAndWait()