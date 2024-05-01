import chess
import chess.engine
import random

STOCKFISH_PATH = 'D:\\stockfish\\stockfish.exe'  # Le chemin du moteur de jeu stockfish

def hill_climbing(engine, board, color):
    # Étape 1: Solution Initiale
    current_best_move = random.choice(list(board.legal_moves))
    board.push(current_best_move)

    # Étape 2: Évaluation de la Solution
    info = engine.analyse(board, chess.engine.Limit(time=0.05))
    board.pop()
    best_score = info["score"].relative.score(mate_score=100000)

    # Étape 3: Recherche Locale
    improved = True
    while improved:
        improved = False
        for move in board.legal_moves:
            board.push(move)
            info = engine.analyse(board, chess.engine.Limit(time=0.05))
            board.pop()
            score = info["score"].relative.score(mate_score=100000)

            # Étape 4: Choix du Meilleur Voisin
            if (color == chess.WHITE and score > best_score) or (color == chess.BLACK and score < best_score):
                best_score = score
                current_best_move = move
                improved = True
                break

    # Étape 5: Répétition
    return current_best_move


# Fonction principale pour faire jouer les deux IA l'une contre l'autre
def play_game():
    board = chess.Board()
    current_player = chess.WHITE

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        while not board.is_game_over():
            move = hill_climbing(engine, board, current_player)
            board.push(move)
            current_player = not current_player

            print("----White move----" if current_player == chess.BLACK else "----Black move----")
            print(board)

    print("Game Over!")
    print("Result: " + board.result())

# Lancer le jeu
play_game()

