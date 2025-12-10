import speech_recognition as sr

# Inicjalizacja rozpoznawacza
r = sr.Recognizer()

# Użycie mikrofonu jako źródła
with sr.Microphone() as source:
    print("Proszę mów...")
    r.adjust_for_ambient_noise(source)  # redukcja szumów
    audio = r.listen(source)

    try:
        # Rozpoznawanie mowy w języku polskim
        text = r.recognize_google(audio, language="pl-PL")
        print("Powiedziałeś: " + text)
    except sr.UnknownValueError:
        print("Nie rozumiem mowy")
    except sr.RequestError as e:
        print(f"Błąd w usłudze rozpoznawania mowy; {e}")
