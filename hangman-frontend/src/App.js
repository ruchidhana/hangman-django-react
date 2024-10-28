import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [guess, setGuess] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  //start a new game
  const startNewGame = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/game/new`);
      setGameId(response.data.id);
      await fetchGameState(response.data.id);
      setMessage('New game started! Make your guess.');
    } catch (error) {
      setMessage('Error starting new game.');
    } finally {
      setLoading(false);
    }
  };

  //fetch the current state of the game
  const fetchGameState = async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/game/${id}`);
      setGameState(response.data);
    } catch (error) {
      setMessage('Error fetching game state.');
    }
  };

  // handle the player's guess
  const makeGuess = async (e) => {
    e.preventDefault();
    if (!guess.trim() || guess.length !== 1) {
      setMessage('Please enter a single letter.');
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/game/${gameId}/guess`, {
        letter: guess,
      });
      setGameState(response.data.game_state);
      setMessage(
        response.data.correct
          ? 'Correct guess!'
          : 'Incorrect guess. Try again!'
      );
      setGuess('');
    } catch (error) {
      setMessage(error.response.data.letter);
    } finally {
      setLoading(false);
    }
  };

  // start a new game when gameId is null and not loading
  useEffect(() => {
    if (!gameId && !loading) {
      startNewGame();
    }
  }, [gameId, loading]);

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header bg-primary text-white text-center">
              <h2>Hangman Game</h2>
            </div>
            <div className="card-body text-center">
              {gameState && (
                <>
                  <h3 className="mb-4">{ gameState.word_state.split('').join(' ')}</h3>
                  <div className="mb-3">
                    <p>Status: <span className="fw-bold">{gameState.status}</span></p>
                    <p>Incorrect Guesses: {gameState.incorrect_guesses}</p>
                    <p>Remaining Guesses: {gameState.remaining_guesses}</p>
                  </div>
                  {gameState.status === 'InProgress' && (
                    <form onSubmit={makeGuess} className="mb-3">
                      <div className="input-group">
                        <input
                          type="text"
                          className="form-control"
                          value={guess}
                          onChange={(e) => setGuess(e.target.value.toUpperCase())}
                          maxLength={1}
                          placeholder="Enter a letter"
                          disabled={loading}
                        />
                        <button
                          type="submit"
                          className="btn btn-primary"
                          disabled={loading || !guess}
                        >
                          Guess
                        </button>
                      </div>
                    </form>
                  )}
                </>
              )}
              
              {message && (
                <div className="alert alert-info mt-3" role="alert">
                  {message}
                </div>
              )}
              
              {gameState && gameState.status !== 'InProgress' && (
                <button
                  className="btn btn-success mt-3"
                  onClick={startNewGame}
                  disabled={loading}
                >
                  Start New Game
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;