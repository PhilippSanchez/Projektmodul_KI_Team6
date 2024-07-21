import os
import sys
import json
import vosk
import pyaudio
import subprocess


model_path = "vosk-model-de-0.21"


if not os.path.exists(model_path):
    print("Bitte lade das Modell herunter und entpacke es im angegebenen Verzeichnis.")
    sys.exit()

# Modell laden
print("Lade Modell...")
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)
print("Modell erfolgreich geladen.")


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
print("Audio-Stream gestartet. Sprechen Sie jetzt...")


def drucken(text):
    with open("temp_print.txt", "w", encoding="utf-8") as file:
        file.write(text)

    subprocess.run(["lp", "temp_print.txt"])


try:
    gesammelter_text = ""
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            print("Keine Daten erhalten.")
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print(f"Sie haben gesagt: {text}")
                with open("transcription.txt", "a", encoding="utf-8") as file:
                    file.write(text + "\n")
                gesammelter_text += text + " "
                if len(gesammelter_text) >= 196:
                    drucken(gesammelter_text[:196])
                    gesammelter_text = gesammelter_text[196:]
                if "gfghfgfjhfjhdrtfshdsjdruszdtzerur6ertudiudrehdudreeztrerterdrteew" in text.lower():
                    print("Stoppbefehl erkannt. Programm wird beendet.")
                    break
        else:
            partial_result = json.loads(recognizer.PartialResult())
            print(f"Partielles Ergebnis: {partial_result.get('partial', '')}")
except KeyboardInterrupt:
    print("Programm durch Benutzer unterbrochen.")


stream.stop_stream()
stream.close()
p.terminate()
print("Programm beendet.")