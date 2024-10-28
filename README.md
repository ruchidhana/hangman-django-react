# Hangman Game 🎉

An interactive Hangman game built with Django REST Framework for the backend and React for the frontend. This project demonstrates the integration of a RESTful API with a modern JavaScript frontend, allowing players to guess letters and reveal words within a classic Hangman interface.

## Features
- **User-friendly interface**: Interactive design with real-time letter updates.
- **API-driven gameplay**: Django REST API handles game logic, state management.
- **Dynamic word generation**: Backend generates a random word each game.
- **Frontend feedback**: Displays correct and incorrect guesses visually.

## Tech Stack
- **Frontend**: React (JavaScript) , react-bootstrap , react-axios
- **Backend**: Django REST Framework
- **API Testing**: Postman

## Setup Instructions

# Backend Setup

1. Ensure Python are installed. (My Python version : 3.12.1)
2. Navigate to the backend directory.
3. Install dependencies. Navigate to hangman_project/game/ and run below
   pip install -r requirements.txt
4. then go back to hangman_project and Run migrations
   python manage.py migrate
5. Start the backend server:
   python manage.py runserver

# Frontend Setup

1. Ensure Node.js(my node version : v20.18.0) and npm (my npm version : 10.8.2) are installed.
2. Navigate to the frontend directory.
3. Install dependencies:
   npm install and 
   npm start

Enjoy playing Hangman! 😊
