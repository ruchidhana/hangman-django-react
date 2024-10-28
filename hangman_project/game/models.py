from django.db import models
import random
import math

class Game(models.Model):

    # List of possible words for the game
    WORD_CHOICES = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]
    
    # Game status choices
    GAME_STATUS = [
        ('InProgress', 'InProgress'),
        ('Lost', 'Lost'),
        ('Won', 'Won'),
    ]
    
    # Fields of the Game model
    word = models.CharField(max_length=100) # The word to be guessed
    guessed_letters = models.CharField(max_length=26, default='')
    incorrect_guesses = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=GAME_STATUS,
        default='InProgress'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def initialize_game(self):
        """
        Initialize the game with a random word and reset the state.
        This function is called to start a new game.
        """
        self.word = random.choice(self.WORD_CHOICES)
        self.guessed_letters = ''
        self.incorrect_guesses = 0
        self.status = 'InProgress'
        self.save()

    def get_word_state(self):
        """
        Return the current state of the word with guessed letters revealed
        and unguessed letters as underscores.
        """
        return ''.join(
            letter if letter.lower() in self.guessed_letters.lower() else '_'
            for letter in self.word
        )

    def get_max_incorrect_guesses(self):
        """
        Calculate the maximum number of incorrect guesses allowed
        based on the length of the word.
        """
        return math.ceil(len(self.word) / 2)

    def get_remaining_guesses(self):
        """
        Return the number of remaining incorrect guesses.
        """
        return self.get_max_incorrect_guesses() - self.incorrect_guesses

    def make_guess(self, letter):
        """
        Process the player's guess.
        Update the guessed letters and game state based on the guess.
        """
        letter = letter.lower()
        if letter in self.guessed_letters:
            return False # If letter was already guessed, return False

        self.guessed_letters += letter
        
        if letter not in self.word.lower():
            self.incorrect_guesses += 1
            if self.incorrect_guesses >= self.get_max_incorrect_guesses():
                self.status = 'Lost'
        elif '_' not in self.get_word_state():
            self.status = 'Won'  
        self.save()
        return letter in self.word.lower() # Return True if the guess was correct