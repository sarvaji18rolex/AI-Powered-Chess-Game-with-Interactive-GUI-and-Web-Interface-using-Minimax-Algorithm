import streamlit as st
import chess
import chess.svg
from ai import get_best_move

st.set_page_config(layout="wide")
st.title("♟️ Chess AI Web App")

# Initialize session
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.selected = None
    st.session_state.history = []

board = st.session_state.board

# 🎯 Show board with last move highlight
last_move = board.peek() if board.move_stack else None
svg = chess.svg.board(board=board, lastmove=last_move)

st.components.v1.html(svg, height=500)

st.write("### Click source → destination")

# 🎮 Clickable grid
for row in range(8):
    cols = st.columns(8)
    for col in range(8):
        square = chess.square(col, 7 - row)
        label = chess.square_name(square)

        if cols[col].button(label, key=f"{row}{col}"):
            if st.session_state.selected is None:
                st.session_state.selected = square
            else:
                move = chess.Move(st.session_state.selected, square)

                if move in board.legal_moves:
                    board.push(move)
                    st.session_state.history.append(str(move))

                    # AI move
                    if not board.is_game_over():
                        ai_move = get_best_move(board, 2)
                        board.push(ai_move)
                        st.session_state.history.append(str(ai_move))

                st.session_state.selected = None
                st.rerun()

# 📜 Move History
st.subheader("📜 Move History")

for i in range(0, len(st.session_state.history), 2):
    moves = st.session_state.history[i:i+2]
    st.write(f"{i//2 + 1}. {' '.join(moves)}")

# 🔄 Restart
if st.button("🔄 Restart Game"):
    st.session_state.board = chess.Board()
    st.session_state.history = []
    st.session_state.selected = None
    st.rerun()

# 🎯 Game status
if board.is_check():
    st.warning("⚠️ Check!")

if board.is_checkmate():
    st.error("♚ Checkmate!")

if board.is_game_over():
    st.success(f"Game Over: {board.result()}")