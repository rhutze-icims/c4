# Preparing

`pip install -r requirements.txt --user`

# Testing

`python -m unittest`

# Running

`python main.py "Team Name"`

The application listens for other copies to startup on the same
network. This can be both from another computer or even a second 
copy on the same computer. Click on the team name that appears and
click start to begin taking turns.

# Developing in Debug Mode

`python main.py debug`

This mode allows placing of pieces on the board without 
having to start a game with another copy of the application.

# TODO:

- Create second column when lots of team selection buttons
- Protect network protocol from user-entered pipes
- Keyboard grid selection and space/click confirmation
