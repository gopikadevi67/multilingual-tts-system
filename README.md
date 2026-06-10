\# Multilingual Text-to-Speech Application

\## Overview
This project is a multilingual Text-to-Speech (TTS) application developed using Python and Gradio. It supports:

\* English
\* Hindi
\* Tamil
\* Telugu
\* Kannada

Users can enter text, select a language, and generate speech audio through a simple web interface.

Environment Setup

\### 1. Create a Virtual Environment

python -m venv venv

\### 2. Activate the environment:

Windows:

venv\\Scripts\\activate

\### 3. Install dependencies:

pip install -r requirements.txt

\## Model Installation

This project uses the AI4Bharat Indic Parler TTS model.

The model will be downloaded automatically from Hugging Face the first time the application is run:

ai4bharat/indic-parler-tts

An internet connection is required for the initial download. Once downloaded and cached locally, the application can be used offline.

\## Running the Application

Run:
python app.py

The application will start locally and can be accessed through:

http://127.0.0.1:7860

\## Features

\* Multilingual speech synthesis
\* Simple Gradio web interface
\* Audio generation and playback
\* Local execution without internet connection after setup

\## Author
Gopikadevi





