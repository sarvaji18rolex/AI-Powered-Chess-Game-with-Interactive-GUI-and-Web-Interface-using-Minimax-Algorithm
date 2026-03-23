import chess
from ai import get_best_move

def main():
    board = chess.Board()

    print("♟️ Welcome to Chess AI!")
    print("Enter moves in format: e2e4")

    while not board.is_game_over():
        print("\nCurrent Board:")
        print(board)

        # Player Move
        try:
            user_move = input("Your move: ")
            move = chess.Move.from_uci(user_move)

            if move in board.legal_moves:
                board.push(move)
            else:
                print("❌ Illegal move. Try again.")
                continue

        except:
            print("❌ Invalid input. Use format like e2e4")
            continue

        if board.is_game_over():
            break

        # AI Move
        print("🤖 AI is thinking...")
        ai_move = get_best_move(board, 2)  # depth = 2

        print("AI plays:", ai_move)
        board.push(ai_move)

    print("\nFinal Board:")
    print(board)
    print("Game Over:", board.result())


if __name__ == "__main__":
    main()