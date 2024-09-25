import speech_recognition as sr
import pyttsx3
import time
from googletrans import Translator

translator = Translator()
r=sr.Recognizer()

exit_flag = False

def process_audio(recognizer, audio):
    global exit_flag  # access the exit flag
    try:
        #recognize speech
        MyText = recognizer.recognize_google(audio)
        print(f"Recognized: {MyText}")

        if MyText.lower() == "exit":
            print("Exit command recognized. Stopping...")
            exit_flag = True
        else:
            #put the text in a file output.txt
            output_text(MyText)
            
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

    except sr.UnknownValueError:
        print("Could not understand audio.")



def output_text(text):
    try:

        translated = translator.translate(text, dest='es')  #change 'es' to your target language code
        translated_text = translated.text
        with open("output.txt", "a") as f:
            f.write(f"Original: {text} \n Translated: {translated_text} \n")
    except Exception as e:
        print(f"Error writing to file: {e}")


def start_listening():
    global exit_flag

    mic = sr.Microphone(device_index=1)
    #adjust for ambient noise
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.1)

    print("Listening in the background...")

        #start non-blocking listening in the background
    stop_listening = r.listen_in_background(mic, process_audio)

        #keep the program running until exit is detected
    while not exit_flag:
        time.sleep(0.1)  # Keep the loop running

        #stop the background listener when exit is detected
    stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    #start the background listening
    exit_flag = False
    start_listening()

    print("Program has exited.")