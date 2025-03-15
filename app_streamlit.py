import os
import tempfile
import base64
import streamlit as st
from google.cloud import texttospeech
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar a chave da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Título da aplicação
st.set_page_config(
    page_title="Conversor de Texto para Áudio com Emoções",
    page_icon="🎙️",
    layout="wide"
)

# Configuração das emoções disponíveis para Google TTS
EMOTIONS_GOOGLE = {
    'neutral': {'nome': 'Neutro', 'pitch': 0.0, 'speaking_rate': 1.0},
    'happy': {'nome': 'Feliz', 'pitch': 3.0, 'speaking_rate': 1.2},
    'sad': {'nome': 'Triste', 'pitch': -2.0, 'speaking_rate': 0.8},
    'excited': {'nome': 'Animado', 'pitch': 4.0, 'speaking_rate': 1.5},
    'dynamic': {'nome': 'Dinâmico', 'pitch': 2.0, 'speaking_rate': 1.3},
    'serious': {'nome': 'Sério', 'pitch': -1.0, 'speaking_rate': 0.9},
    'whisper': {'nome': 'Sussurro', 'pitch': 1.5, 'speaking_rate': 0.7},
    'dramatic': {'nome': 'Dramático', 'pitch': -1.5, 'speaking_rate': 0.9},
    'robotic': {'nome': 'Robótico', 'pitch': -4.0, 'speaking_rate': 0.9},
    'gentle': {'nome': 'Suave', 'pitch': 1.0, 'speaking_rate': 0.7},
    'assertive': {'nome': 'Assertivo', 'pitch': 0.0, 'speaking_rate': 1.3},
    'storytelling': {'nome': 'Narração', 'pitch': 0.5, 'speaking_rate': 0.85},
}

# Configuração das vozes OpenAI
VOICES_OPENAI = {
    'alloy': 'Alloy (Equilibrado)',
    'echo': 'Echo (Suave)',
    'fable': 'Fable (Expressivo)',
    'onyx': 'Onyx (Potente)',
    'nova': 'Nova (Amigável)',
    'shimmer': 'Shimmer (Otimista)'
}

def google_text_to_speech(text, emotion='neutral', language_code="pt-BR", voice_name="pt-BR-Wavenet-A", gender="FEMALE"):
    """Converte texto em fala usando a API Google Cloud Text-to-Speech com a emoção especificada."""
    try:
        # Inicializa o cliente do Text-to-Speech
        client = texttospeech.TextToSpeechClient()
        
        # Configura o texto de entrada
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Configura a voz
        gender_enum = getattr(texttospeech.SsmlVoiceGender, gender)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=gender_enum
        )
        
        # Obtém parâmetros de emoção
        emotion_params = EMOTIONS_GOOGLE.get(emotion, EMOTIONS_GOOGLE['neutral'])
        
        # Configura os parâmetros de áudio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            pitch=emotion_params['pitch'],
            speaking_rate=emotion_params['speaking_rate']
        )
        
        # Realiza a síntese de fala
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        return response.audio_content, None
    except Exception as e:
        return None, str(e)

def openai_text_to_speech(text, voice='nova', model="tts-1"):
    """Converte texto em fala usando a API OpenAI TTS."""
    try:
        response = openai.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        # OpenAI retorna o áudio como um objeto de bytes
        audio_data = response.content
        
        return audio_data, None
    except Exception as e:
        return None, str(e)

def create_download_link(audio_data, filename="audio.mp3"):
    """Cria um link de download para o arquivo de áudio."""
    b64 = base64.b64encode(audio_data).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Clique aqui para baixar o áudio</a>'
    return href

def save_temp_audio(audio_data):
    """Salva o áudio em um arquivo temporário e retorna o caminho."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file.write(audio_data)
    temp_file.close()
    return temp_file.name

def main():
    st.title("🎙️ Conversor de Texto para Áudio com Emoções")
    st.subheader("Transforme seu texto em português em fala com diferentes emoções")
    
    # Seleção da API
    api_option = st.sidebar.radio(
        "Selecione a API de conversão:",
        options=["Google Cloud TTS", "OpenAI TTS"],
        index=0
    )
    
    # Área de texto para entrada do usuário
    text_input = st.text_area("Digite seu texto em português:", height=150)
    
    # Seleção de emoção/voz baseada na API escolhida
    if api_option == "Google Cloud TTS":
        # Opções adicionais para Google TTS
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_emotion = st.selectbox(
                "Selecione a emoção:",
                options=list(EMOTIONS_GOOGLE.keys()),
                format_func=lambda x: EMOTIONS_GOOGLE[x]['nome']
            )
        
        with col2:
            voice_gender = st.selectbox(
                "Gênero da voz:",
                options=["FEMALE", "MALE", "NEUTRAL"],
                format_func=lambda x: {"FEMALE": "Feminina", "MALE": "Masculina", "NEUTRAL": "Neutra"}[x],
                index=0
            )
        
        with col3:
            voice_type = st.selectbox(
                "Tipo de voz:",
                options=["pt-BR-Wavenet-A", "pt-BR-Wavenet-B", "pt-BR-Wavenet-C"],
                format_func=lambda x: x.replace("pt-BR-Wavenet-", "Tipo "),
                index=0
            )
        
        # Informações sobre a emoção selecionada
        st.info(f"**{EMOTIONS_GOOGLE[selected_emotion]['nome']}**: Pitch={EMOTIONS_GOOGLE[selected_emotion]['pitch']}, Velocidade={EMOTIONS_GOOGLE[selected_emotion]['speaking_rate']}")
        
    else:  # OpenAI TTS
        selected_voice = st.selectbox(
            "Selecione a voz:",
            options=list(VOICES_OPENAI.keys()),
            format_func=lambda x: VOICES_OPENAI[x],
            index=0
        )
        
        model = st.selectbox(
            "Modelo:",
            options=["tts-1", "tts-1-hd"],
            format_func=lambda x: "Padrão" if x == "tts-1" else "Alta Definição",
            index=0
        )
        
        st.info("Nota: A API OpenAI atualmente não suporta ajustes de entonação específicos, mas oferece vozes com diferentes características.")
    
    # Botão para converter
    if st.button("Converter para Áudio", type="primary", use_container_width=True):
        if not text_input:
            st.error("Por favor, digite algum texto para converter.")
        else:
            with st.spinner("Gerando áudio..."):
                if api_option == "Google Cloud TTS":
                    audio_data, error = google_text_to_speech(
                        text_input, 
                        emotion=selected_emotion,
                        gender=voice_gender,
                        voice_name=voice_type
                    )
                else:  # OpenAI TTS
                    audio_data, error = openai_text_to_speech(
                        text_input,
                        voice=selected_voice,
                        model=model
                    )
                
                if error:
                    st.error(f"Erro ao gerar áudio: {error}")
                else:
                    # Salvar o áudio em um arquivo temporário
                    audio_path = save_temp_audio(audio_data)
                    
                    # Mostrar o player de áudio
                    st.subheader("Áudio gerado:")
                    st.audio(audio_path, format="audio/mp3")
                    
                    # Opção de download
                    st.markdown("### Download do áudio")
                    st.markdown(create_download_link(audio_data, "audio_sintetizado.mp3"), unsafe_allow_html=True)
                    
                    # Informações adicionais
                    st.success("Áudio gerado com sucesso!")
                    
    # Informações sobre as APIs
    with st.expander("ℹ️ Sobre as APIs"):
        st.markdown("""
        ### Google Cloud Text-to-Speech
        - Suporte nativo para português brasileiro
        - Permite ajustes detalhados de pitch e velocidade para criar diferentes emoções
        - Requer credenciais da Google Cloud Platform
        
        ### OpenAI Text-to-Speech
        - Vozes naturais e de alta qualidade
        - Não oferece ajustes finos de entonação, mas diferentes vozes têm características distintas
        - Requer chave de API da OpenAI
        """)
    
    # Informações de personalização
    with st.expander("🛠️ Personalização de emoções"):
        st.markdown("""
        ### Como as emoções são criadas
        As emoções na API Google são simuladas alterando dois parâmetros principais:
        
        - **Pitch (Tom)**: Valores positivos tornam a voz mais aguda, valores negativos tornam a voz mais grave
        - **Speaking Rate (Velocidade)**: Valores maiores que 1.0 aceleram a fala, valores menores que 1.0 desaceleram
        
        A combinação desses parâmetros cria diferentes sensações emocionais na voz.
        """)
        
        # Exibir tabela de emoções
        emotion_data = []
        for emotion_id, emotion in EMOTIONS_GOOGLE.items():
            emotion_data.append({
                "Emoção": emotion['nome'],
                "Pitch": emotion['pitch'],
                "Velocidade": emotion['speaking_rate']
            })
        
        st.table(emotion_data)

if __name__ == "__main__":
    main() 