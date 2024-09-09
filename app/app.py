from openai import OpenAI
from dotenv import load_dotenv
from app.config import Config
import streamlit as st


class App:

    def __init__(self) -> None:
        self.config = Config.get_all()
        self.client = OpenAI()
        self.voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def view(self):
        st.title("Generador de Audio con OpenAI")

        input_user = st.text_input("Ingrese el tema:")
        response_topic = self.generate_text(input_user)
        
        text = st.text_area("Ingrese el texto", height=200, value=response_topic)
        voice = st.selectbox("Seleccione la Voz:", self.voices)

        if st.button("Generar audio"):
            if text:
                response = self.client.audio.speech.create(
                    model=self.config["model_audio"],
                    voice=voice,
                    input=text
                )

                audio_path = f"audio_{voice}.mp3"
                with open(audio_path, "wb") as output_file:
                    for chunk in response.iter_bytes():
                        if chunk:
                            output_file.write(chunk)

                st.success(f"Audio generado en {audio_path}")

                audio_file = open(audio_path, "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("Por favor, ingrese un texto")


    def generate_text(self, prompt):
        """Generar texto con el modelo LLM GTP-4o-mini"""

        message = self.client.chat.completions.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            messages=[
                {"role": "system", "content": "Genera un respuesta con maximo 60 palabras"},
                {"role": "user", "content": prompt},
            ],
        )
        return message.choices[0].message.content


if __name__ == "__main__":
    load_dotenv()
