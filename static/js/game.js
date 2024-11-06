document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const status = document.getElementById('status');
    const resetButton = document.getElementById('reset');

    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });

    resetButton.addEventListener('click', resetGame);

    async function handleCellClick(event) {
        const position = parseInt(event.target.dataset.index);
        
        try {
            const response = await fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ position }),
            });

            const gameState = await response.json();
            
            if (!response.ok) {
                alert(gameState.error);
                return;
            }

            updateBoard(gameState);
            updateStatus(gameState);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while making the move');
        }
    }

    function updateBoard(gameState) {
        gameState.board.forEach((value, index) => {
            cells[index].textContent = value;
        });
    }

    function updateStatus(gameState) {
        if (gameState.game_over) {
            if (gameState.winner === 'draw') {
                status.textContent = "Game Over - It's a Draw!";
            } else {
                status.textContent = `Game Over - ${gameState.winner} Wins!`;
            }
        } else {
            status.textContent = `Current player: ${gameState.current_player}`;
        }
    }

    async function resetGame() {
        try {
            const response = await fetch('/reset', {
                method: 'POST',
            });
            const gameState = await response.json();
            
            updateBoard(gameState);
            updateStatus(gameState);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while resetting the game');
        }
    }
});
