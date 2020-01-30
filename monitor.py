from config import *
from board import Board
from network import Network
import pygame
import signal
import sys


def handle_sigint(sig, frame):
    global shutdown_signal
    if sig == signal.SIGINT:
        print('Received Ctrl+C. Shutting down...')
        shutdown_signal = True


if len(sys.argv) < 2 or len(sys.argv[1]) > 20:
    print("\nProvide a team name of up to 20 characters when starting the application." +
          "\nExample: python monitor.py \"My Team Name\"\n")
    sys.exit(1)
our_team = sys.argv[1]

pygame.init()
pygame.display.set_caption('C4 Monitor - %s' % our_team)
screen = pygame.display.set_mode((450, 375))
clock = pygame.time.Clock()

shutdown_signal = False
signal.signal(signal.SIGINT, handle_sigint)

network = Network(our_team, None)
network.update_game_state(STATE_OUR_TURN)
networking_thread = network.start()

images = {
    'black': pygame.image.load('black_chip.png').convert(),
    'red': pygame.image.load('red_chip.png').convert()
}

board = Board(pygame.freetype.Font, GAME_ROWS, GAME_COLS, 0, 0, images)

while not shutdown_signal:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown_signal = True

        elif event.type == pygame.USEREVENT and event.action == ACTION_REFRESH:
            print("Monitor Received: " + str(event))
            cells = event.cells.split('-')
            for row_index in range(len(cells)):
                row = cells[row_index]
                for col_index in range(len(row)):
                    cell = row[col_index]
                    if cell == 'R':
                        board.record_move('red', row_index, col_index)
                    elif cell == 'B':
                        board.record_move('black', row_index, col_index)

    screen.fill(DARK_BLUE)
    board.draw(screen)

    clock.tick(5)
    pygame.display.update()

network.shutdown()
networking_thread.join()

pygame.quit()
sys.exit(0)
