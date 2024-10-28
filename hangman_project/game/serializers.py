from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game model.
    It includes additional fields for the current word state and remaining guesses.
    """
    word_state = serializers.SerializerMethodField() # Custom field for displaying the current state of the word
    remaining_guesses = serializers.SerializerMethodField() # Custom field for displaying remaining guesses

    class Meta:
        model = Game
        fields = ['id', 'status', 'word_state', 'incorrect_guesses', 'remaining_guesses']

    def get_word_state(self, obj):
        return obj.get_word_state()

    def get_remaining_guesses(self, obj):
        return obj.get_remaining_guesses()

class GuessSerializer(serializers.Serializer):
    """
    Serializer for validating the player's guess.
    It ensures that the guess is a single letter.
    """
    letter = serializers.CharField(max_length=1, min_length=1)
    
    def validate_letter(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Guess must be a letter")
        return value
