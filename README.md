# Conversor de Texto para Áudio com Emoções (Streamlit)

Este projeto permite converter texto em português do Brasil para áudio com diferentes entonações emocionais, como feliz, triste, animado, dinâmico, entre outros, usando as APIs do Google Cloud e da OpenAI.

## Funcionalidades

- Conversão de texto para fala em português brasileiro
- Seleção entre duas APIs diferentes (Google Cloud e OpenAI)
- 12 opções diferentes de emoções na API do Google (feliz, triste, neutro, animado, dinâmico, sério, sussurro, dramático, robótico, suave, assertivo, narração)
- 6 tipos de vozes diferentes na API da OpenAI
- Interface web amigável usando Streamlit
- Reprodução de áudio diretamente no navegador
- Download do arquivo de áudio gerado

## Requisitos

- Python 3.6 ou superior
- Conta Google Cloud com a API Text-to-Speech habilitada
- Arquivo de credenciais do Google Cloud
- Conta OpenAI com acesso à API Text-to-Speech

## Configuração

1. Clone este repositório:
```
git clone [URL_DO_REPOSITÓRIO]
cd text-to-speech
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Configure as credenciais do Google Cloud:
   - Acesse o [Console do Google Cloud](https://console.cloud.google.com/)
   - Crie um projeto e habilite a API Text-to-Speech
   - Crie uma conta de serviço e baixe o arquivo de credenciais JSON
   - Salve o arquivo como `google-credentials.json` na pasta raiz do projeto

4. Configure a chave da API OpenAI:
   - Acesse o [Portal da OpenAI](https://platform.openai.com/)
   - Obtenha sua chave de API
   - Adicione a chave no arquivo `.env` no campo `OPENAI_API_KEY`

5. Configure as variáveis de ambiente:
   - O arquivo `.env` já contém as configurações básicas
   - Certifique-se de que a variável `GOOGLE_APPLICATION_CREDENTIALS` aponta para o caminho correto do arquivo de credenciais
   - Adicione sua chave API da OpenAI na variável `OPENAI_API_KEY`

## Execução

Execute o aplicativo Streamlit:
```
streamlit run app_streamlit.py
```

O aplicativo será iniciado e abrirá automaticamente no seu navegador padrão (normalmente em http://localhost:8501).

## Como usar

1. Selecione a API que deseja usar (Google Cloud ou OpenAI) no menu lateral
2. Digite o texto em português que deseja converter para áudio
3. Dependendo da API selecionada:
   - **Google Cloud**: Selecione a emoção, gênero da voz e tipo de voz
   - **OpenAI**: Selecione a voz e o modelo (padrão ou alta definição)
4. Clique em "Converter para Áudio"
5. Ouça o áudio gerado diretamente no navegador
6. Use o link de download para salvar o arquivo MP3 em seu dispositivo

## Personalização

### Google Cloud TTS
Para adicionar ou ajustar as emoções disponíveis, edite o dicionário `EMOTIONS_GOOGLE` no arquivo `app_streamlit.py`:

```python
EMOTIONS_GOOGLE = {
    'neutral': {'nome': 'Neutro', 'pitch': 0.0, 'speaking_rate': 1.0},
    'happy': {'nome': 'Feliz', 'pitch': 3.0, 'speaking_rate': 1.2},
    # Adicione novas emoções ou ajuste os parâmetros existentes
}
```

Os principais parâmetros que podem ser ajustados são:
- `pitch`: Altera o tom da voz (valores positivos = mais agudo, valores negativos = mais grave)
- `speaking_rate`: Controla a velocidade da fala (1.0 = velocidade normal)

### OpenAI TTS
Para adicionar novas vozes da OpenAI, edite o dicionário `VOICES_OPENAI` no arquivo `app_streamlit.py`:

```python
VOICES_OPENAI = {
    'alloy': 'Alloy (Equilibrado)',
    'echo': 'Echo (Suave)',
    # Adicione novas vozes conforme disponibilizadas pela OpenAI
}
```

## Comparação entre as APIs

### Google Cloud Text-to-Speech
- **Vantagens**: Permite ajustes detalhados de pitch e velocidade para simular emoções, suporte nativo para português do Brasil
- **Desvantagens**: Pode soar menos natural em algumas configurações extremas

### OpenAI Text-to-Speech
- **Vantagens**: Vozes mais naturais, qualidade superior em algumas situações
- **Desvantagens**: Não permite ajustes finos de entonação, menor controle sobre a expressividade emocional

## Limitações

- As APIs possuem limites de uso gratuito
- Textos muito longos podem ser truncados ou gerar custos adicionais
- A qualidade das emoções na API Google depende dos ajustes de parâmetros de pitch e velocidade
- A API OpenAI não suporta ajustes finos de emoção, apenas vozes com características diferentes

## Licença

[Especifique a licença do projeto] 