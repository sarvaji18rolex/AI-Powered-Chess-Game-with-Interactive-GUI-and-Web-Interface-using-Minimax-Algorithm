import pygame
import chess
from ai import get_best_move
  
WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess AI")

# Sounds
move_sound = pygame.mixer.Sound("assets/move.wav")
capture_sound = pygame.mixer.Sound("assets/capture.wav")

IMAGES = {}

def load_images():
    pieces = ['wp','wr','wn','wb','wq','wk','bp','br','bn','bb','bq','bk']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f"assets/{piece}.png"), (SQ_SIZE, SQ_SIZE)
        )

def draw_board():
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[(row+col)%2]
            pygame.draw.rect(screen, color,
                             pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(board, dragged_piece=None, mouse_pos=None):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)

            piece_str = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()

            if dragged_piece and square == dragged_piece:
                continue

            screen.blit(IMAGES[piece_str],
                        pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Draw dragged piece
    if dragged_piece and mouse_pos:
        piece = board.piece_at(dragged_piece)
        if piece:
            piece_str = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()
            screen.blit(IMAGES[piece_str],
                        pygame.Rect(mouse_pos[0]-SQ_SIZE//2, mouse_pos[1]-SQ_SIZE//2, SQ_SIZE, SQ_SIZE))

def animate_move(start_sq, end_sq, piece_str):
    start_row = 7 - chess.square_rank(start_sq)
    start_col = chess.square_file(start_sq)
    end_row = 7 - chess.square_rank(end_sq)
    end_col = chess.square_file(end_sq)

    frames = 10
    for frame in range(frames):
        draw_board()
        progress = frame / frames

        row = start_row + (end_row - start_row) * progress
        col = start_col + (end_col - start_col) * progress

        screen.blit(IMAGES[piece_str],
                    pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

        pygame.display.flip()
        pygame.time.delay(20)

def main():
    board = chess.Board()
    load_images()

    dragging = False
    selected_square = None
    mouse_pos = None

    running = True

    while running:
        draw_board()
        draw_pieces(board, selected_square, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Start dragging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQ_SIZE
                row = 7 - (y // SQ_SIZE)
                selected_square = chess.square(col, row)

                if board.piece_at(selected_square):
                    dragging = True

            # Dragging
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_pos = pygame.mouse.get_pos()

            # Drop piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    x, y = pygame.mouse.get_pos()
                    col = x // SQ_SIZE
                    row = 7 - (y // SQ_SIZE)
                    target_square = chess.square(col, row)

                    move = chess.Move(selected_square, target_square)

                    if move in board.legal_moves:
                        piece = board.piece_at(selected_square)
                        piece_str = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()

                        # Capture sound
                        if board.is_capture(move):
                            capture_sound.play()
                        else:
                            move_sound.play()

                        animate_move(selected_square, target_square, piece_str)
                        board.push(move)

                        # AI move
                        ai_move = get_best_move(board, 2)
                        if ai_move:
                            piece = board.piece_at(ai_move.from_square)
                            piece_str = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()

                            animate_move(ai_move.from_square, ai_move.to_square, piece_str)
                            move_sound.play()
                            board.push(ai_move)

                    dragging = False
                    selected_square = None
                    mouse_pos = None

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
