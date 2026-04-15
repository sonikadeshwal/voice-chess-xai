# Voice-Controlled Explainable Chess AI Using Search Optimization and Neural Networks

This project presents a smart chess system that combines voice recognition, artificial intelligence, and explainable decision-making. Players can give moves using voice commands, and the system converts speech into structured chess input. The AI engine uses search optimization (Minimax with Alpha–Beta pruning and optional Neural Network evaluation) to choose strong moves.

What makes this system unique is its **explainability**—after each move, the AI generates a clear and human-friendly explanation showing why the move was selected, including threat analysis, positional evaluation, and piece importance. The project offers an interactive interface, speech feedback, and real-time game logging, creating an intuitive, accessible, and intelligent chess-playing experience.

## Main Project Objectives

1. **Develop a Fully Functional Voice-Controlled Chess Interface**
   To implement accurate speech-to-text recognition so users can play chess hands-free by giving spoken commands such as "move knight to F3." This objective ensures accessibility, real-time processing, and natural interaction.

2. **Build an AI Engine with Search Optimization and Neural Network Evaluation**
   To design and integrate a smart chess engine using Minimax and Alpha-Beta pruning for efficient move calculation, enhanced with a neural-network-based board evaluation model for improved decision-making strength.

3. **Implement Explainable AI (XAI) to Justify Each Move**
   To create an explanation system that provides human-readable reasoning for the AI's moves, including evaluations of threats, safety, positional advantages, and alternative move comparisons, improving transparency and understanding.

## Features Currently Implemented

- **Interactive Streamlit Interface**: Beautiful UI visualizing the board.
- **Voice Recognition Integration**: Native `st.audio_input` passing to `SpeechRecognition` translating spoken words into UCI/SAN chess moves.
- **AI Engine (Minimax with Alpha-Beta)**: Computes the best moves efficiently up to configurable depths.
- **Explainable AI (XAI) Logs**: Justifies positional control, checks, captures, and development for both human and AI moves dynamically.

## How to Run Locally

1. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit Application:
   ```bash
   streamlit run app.py
   ```

## Deployment

Deploy this project on Streamlit Community Cloud directly by linking this GitHub repository! Streamlit's native `st.audio_input` will capture microphone audio directly via the browser securely.
