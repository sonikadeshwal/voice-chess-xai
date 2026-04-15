import speech_recognition as sr
import chess
import re
def parse_voice_to_move(audio_file_like, board):
    """
    Takes an audio file object, performs speech recognition,
    and returns a valid chess move and the transcribed text.
    """
    recognizer = sr.Recognizer()
    try:
        # reset file pointer just in case Streamlit gives it to us at the end of the buffer
        if hasattr(audio_file_like, 'seek'):
            audio_file_like.seek(0)
            
        with sr.AudioFile(audio_file_like) as source:
            audio_data = recognizer.record(source)
            # Use Google Speech Recognition API (requires internet, but no key needed for basic usage)
            text = recognizer.recognize_google(audio_data).lower()
            move = match_move_to_board(text, board)
            return move, text
    except sr.UnknownValueError:
        return None, "Silence or unclear audio detected. Please try speaking closer to the mic, like 'Move pawn to e4'."
    except sr.RequestError as e:
        return None, f"Google Speech API error (check your internet): {e}"
    except ValueError as e:
        return None, f"Audio format error (Browser might have sent an empty or unsupported format): {e}"
    except Exception as e:
        return None, f"Error: {e}"
        
def match_move_to_board(text, board):
    """
    Attempts to extract a valid chess move from transcribed text.
    Supports basic UCI formatted speech like 'e2 to e4' or 'knight to f3'.
    """
    # Clean padding words
    cleaned_text = text.replace(" to ", "").replace(" ", "").replace("-", "")
    
    # Check naive UCI match exactly
    for move in board.legal_moves:
        if move.uci() in cleaned_text:
            return move
            
    # Check naive SAN match
    for move in board.legal_moves:
        san = board.san(move).lower()
        if san in text:
            return move
            
    # Regex extraction for patterns like "e2e4"
    matches = re.findall(r'[a-h][1-8][a-h][1-8]', cleaned_text)
    if matches:
        proposed_uci = matches[0]
        for move in board.legal_moves:
            if move.uci() == proposed_uci:
                return move
                
    return None
