import gradio as gr
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
import soundfile as sf
import torch
import tempfile
import re

tokenizer = AutoTokenizer.from_pretrained(
    "ai4bharat/indic-parler-tts"
)

model = ParlerTTSForConditionalGeneration.from_pretrained(
    "ai4bharat/indic-parler-tts",
    low_cpu_mem_usage=True
)

def detect_script(text):
    if re.search(r'[\u0B80-\u0BFF]', text):
        return "Tamil"
    elif re.search(r'[\u0C00-\u0C7F]', text):
        return "Telugu"
    elif re.search(r'[\u0C80-\u0CFF]', text):
        return "Kannada"
    elif re.search(r'[\u0900-\u097F]', text):
        return "Hindi"
    elif re.search(r'[A-Za-z]', text):
        return "English"
    return None

def generate_speech(text, language):

    if not text.strip():
        raise gr.Error("Please enter text.")

    detected_language = detect_script(text)

    if detected_language and detected_language != language:
        raise gr.Error(
            f"Selected language is {language}, but the text appears to be {detected_language}."
        )

    description = "A clear and natural speaker."

    input_ids = tokenizer(
        description,
        return_tensors="pt"
    ).input_ids

    prompt_ids = tokenizer(
        text,
        return_tensors="pt"
    ).input_ids

    with torch.no_grad():
        generation = model.generate(
            input_ids=input_ids,
            prompt_input_ids=prompt_ids
        )

    output_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ).name

    sf.write(
        output_file,
        generation.cpu().numpy().squeeze(),
        model.config.sampling_rate
    )

    return output_file

custom_css = """
body {
    font-family: 'Segoe UI', sans-serif;
}

.gradio-container {
    background: linear-gradient(
        135deg,
        #07111F 0%,
        #0F2740 50%,
        #07111F 100%
    ) !important;
}

.title {
    font-size: 34px;
    font-weight: 600;
    color: #F1E2D1;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 16px;
    color: #C8A96B;
    text-align: center;
    margin-bottom: 25px;
}

#generate-btn {
    background: #4DA3FF !important;
    color: white !important;
    font-weight: 600 !important;
}

#clear-btn {
    background: #C8A96B !important;
    color: #07111F !important;
    font-weight: 600 !important;
}
"""

with gr.Blocks(
    css=custom_css,
    title="Multilingual Expressive Text-to-Speech System",
    theme=gr.themes.Soft()
) as demo:

    gr.HTML("""
        <div class="title">
            Multilingual Expressive Text-to-Speech System
        </div>

        <div class="subtitle">
            Generate high-quality speech from text in multiple Indian languages.
        </div>
    """)

    with gr.Row():

        with gr.Column(scale=2):

            language = gr.Dropdown(
                choices=[
                    "English",
                    "Hindi",
                    "Tamil",
                    "Telugu",
                    "Kannada"
                ],
                value="English",
                label="Language"
            )

            text_input = gr.Textbox(
                lines=10,
                label="Text Input",
                placeholder="Type or paste text here..."
            )

            with gr.Row():

                generate_btn = gr.Button(
                    "Generate Speech",
                    elem_id="generate-btn"
                )

                clear_btn = gr.Button(
                    "Clear",
                    elem_id="clear-btn"
                )

        with gr.Column(scale=1):

            audio_output = gr.Audio(
                label="Generated Audio",
                type="filepath"
            )

    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, language],
        outputs=audio_output
    )

    clear_btn.click(
        lambda: ("", "English", None),
        outputs=[
            text_input,
            language,
            audio_output
        ]
    )

demo.launch()
