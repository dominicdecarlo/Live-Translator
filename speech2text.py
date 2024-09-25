import speech_recognition as sr
import pyttsx3
import time
from googletrans import Translator

translator = Translator()
r=sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone(device_index=1) as source:
                r.adjust_for_ambient_noise(source, duration=0.1)
                print("Listening...")

                audio2 = r.listen(source, timeout=5, phrase_time_limit=5)

                MyText = r.recognize_google(audio2)
                print(f"Recognized: {MyText}")

                if MyText.lower() == "exit":
                    print("Exit command recognized. Stopping...")
                    break
                
                return MyText

        except sr.WaitTimeoutError:
            print("Timeout reached, no speech detected. Retrying...")
            return None
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")

        time.sleep(1)


def output_text(text):
    try:

        translated = translator.translate(text, dest='es')  # Change 'es' to your target language code
        translated_text = translated.text
        with open("output.txt", "a") as f:
            f.write(f"Original: {text} \n Translated: {translated_text} \n")
    except Exception as e:
        print(f"Error writing to file: {e}")


while True:
    text = record_text()

    if text.lower() == "exit":
        print("Exiting program.")
        break

    output_text(text)

    time.sleep(1)

    print("Ready for next input.")