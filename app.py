import streamlit as st
import chess
import chess.svg
import base64
from engine import get_best_move
from explain import explain_move
from voice import parse_voice_to_move
import io

st.set_page_config(page_title="Voice-Controlled XAI Chess", layout="wide", initial_sidebar_state="expanded")

def render_board(board):
    """Render the chess board as an SVG image."""
    boardsvg = chess.svg.board(board=board, size=450)
    b64 = base64.b64encode(boardsvg.encode('utf-8')).decode('utf-8')
    html = f'<div style="display: flex; justify-content: center;"><img src="data:image/svg+xml;base64,{b64}"></div>'
    st.markdown(html, unsafe_allow_html=True)

# Initialize Session State
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
if 'logs' not in st.session_state:
    st.session_state.logs = []

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("Adjust AI configurations here.")
    depth = st.slider("AI Search Depth (Minimax)", min_value=1, max_value=4, value=3)
    if st.button("New Game", type="primary"):
        st.session_state.board = chess.Board()
        st.session_state.logs = []
        st.rerun()

st.title("🎙️ Voice-Controlled Explainable Chess AI")
st.markdown("Play hands-free chess! The AI uses Minimax optimization and explains the reasoning behind each move.")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Chess Board")
    render_board(st.session_state.board)
    
    if st.session_state.board.is_game_over():
        st.error(f"Game Over! Result: {st.session_state.board.result()}")

with col2:
    st.subheader("Controls")
    
    tabs = st.tabs(["🗣️ Voice Command", "⌨️ Manual Entry"])
    
    with tabs[0]:
        st.markdown("**Speak your move (e.g., 'e2 to e4' or 'knight to f3')**")
        audio_val = st.audio_input("Record Move")
        if audio_val and st.session_state.board.turn == chess.WHITE and not st.session_state.board.is_game_over():
            with st.spinner("Processing voice command..."):
                # Pass file-like object to voice handler
                move, text = parse_voice_to_move(audio_val, st.session_state.board)
                if move:
                    st.success(f"Recognized: '{text}' -> Interpreted as {move.uci()}")
                    explanation = explain_move(st.session_state.board, move)
                    st.session_state.board.push(move)
                    st.session_state.logs.append(f"👨‍🦱 **Human (Voice):** {move.uci()} \n\n*Reasoning:* {explanation}")
                    st.rerun()
                else:
                    st.warning(f"Could not interpret a valid move. Transcribed speech: '{text}'")
                    
    with tabs[1]:
        manual_move = st.text_input("Enter Move (UCI format, e.g., e2e4):")
        if st.button("Submit Manual Move") and st.session_state.board.turn == chess.WHITE and not st.session_state.board.is_game_over():
            try:
                move = chess.Move.from_uci(manual_move)
                if move in st.session_state.board.legal_moves:
                    explanation = explain_move(st.session_state.board, move)
                    st.session_state.board.push(move)
                    st.session_state.logs.append(f"👨‍🦱 **Human:** {move.uci()} \n\n*Reasoning:* {explanation}")
                    st.rerun()
                else:
                    st.error("Illegal Move")
            except:
                st.error("Invalid Format")

    st.divider()
    st.subheader("Explainable AI (XAI) Logs")
    
    # Render XAI logs in a scrollable container
    log_container = st.container(height=350)
    with log_container:
        for log in reversed(st.session_state.logs):
            st.info(log)

# AI Turn Execution
if st.session_state.board.turn == chess.BLACK and not st.session_state.board.is_game_over():
    with st.spinner("AI Engine is thinking..."):
        best_move = get_best_move(st.session_state.board, depth=depth)
        explanation = explain_move(st.session_state.board, best_move)
        st.session_state.board.push(best_move)
        st.session_state.logs.append(f"🤖 **AI Engine:** {best_move.uci()} \n\n*XAI Reasoning:* {explanation}")
        st.rerun()
