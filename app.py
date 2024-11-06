from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Game state
game_state = {
    'board': ['' for _ in range(9)],
    'current_player': 'X',
    'game_over': False,
    'winner': None
}

def check_winner(board):
    # Winning combinations
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    
    for line in lines:
        if board[line[0]] and board[line[0]] == board[line[1]] == board[line[2]]:
            return board[line[0]]
    
    if '' not in board:
        return 'draw'
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    if game_state['game_over']:
        return jsonify({'error': 'Game is over'}), 400

    position = request.json.get('position')
    
    if not isinstance(position, int) or position < 0 or position > 8:
        return jsonify({'error': 'Invalid position'}), 400
        
    if game_state['board'][position]:
        return jsonify({'error': 'Position already taken'}), 400

    # Make the move
    game_state['board'][position] = game_state['current_player']
    
    # Check for winner
    winner = check_winner(game_state['board'])
    if winner:
        game_state['game_over'] = True
        game_state['winner'] = winner
    else:
        # Switch player
        game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'

    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset_game():
    game_state['board'] = ['' for _ in range(9)]
    game_state['current_player'] = 'X'
    game_state['game_over'] = False
    game_state['winner'] = None
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True)
