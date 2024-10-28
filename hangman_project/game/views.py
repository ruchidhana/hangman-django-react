from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Game
from .serializers import GameSerializer, GuessSerializer

class NewGameView(views.APIView):
    """
    View for creating a new game.
    Handles POST requests to initialize a new game instance.
    """
    def post(self, request):
        game = Game()
        game.initialize_game()
        return Response({'id': game.id}, status=status.HTTP_201_CREATED)

class GameStateView(views.APIView):
    """
    View for retrieving the current state of a game.
    Handles GET requests to fetch game details by game ID.
    """
    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data)

class GuessView(views.APIView):
    """
    View for processing a player's guess.
    Handles POST requests to make a guess in an ongoing game.
    """
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        
        # Check if the game is still in progress
        if game.status != 'InProgress':
            return Response(
                {"error": "Game is already finished"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GuessSerializer(data=request.data)

        # Validate the incoming guess data using the GuessSerializer
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Process the guess and update the game state
        guess_correct = game.make_guess(serializer.validated_data['letter'])
        
        # Return the result of the guess along with the updated game state
        return Response({
            'correct': guess_correct,
            'game_state': GameSerializer(game).data
        })