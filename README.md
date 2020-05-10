# Preparing

`pip install -r requirements.txt --user`

# Testing

`python -m unittest`

# Running

`python main.py "Team Name"`

The application listens for other copies to startup on the same
network. This can be both from another computer or even a second 
copy on the same computer. 

> If a Firewall popup appears, asking if this application should be allowed to talk to other computers on the network, check the networks, and click Allow.

Click on the team name that appears and click start to begin taking turns.

If you are experimenting with the project and only have one copy running, you can use the Debug Mode that is described in the next section.

# Developing in Debug Mode

`python main.py debug`

This mode allows placing of pieces on the board without 
having to start a game with another copy of the application.
