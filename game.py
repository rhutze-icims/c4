from board import Board
from button import Button
from config import *
import pygame
import pygame.freetype
from status_bar import StatusBar
from teams import Teams


class Game:

    def __init__(self, screen, messages_to_send, our_team, who_gets_to_be_red_number, debug_mode):
        self.game_state = STATE_PREPARING

        self.images = {
            'black': pygame.image.load('black_chip.png').convert(),
            'red': pygame.image.load('red_chip.png').convert()
        }

        self.board = Board(pygame.freetype.Font, GAME_ROWS, GAME_COLS, 0, 0, self.images)
        self.debug_mode = debug_mode
        self.messages_to_send = messages_to_send
        self.our_team = our_team
        self.our_team_color = '?'
        self.start_game_button = Button("Start", 10, 450, self.start_game)
        self.screen = screen
        self.selected_their_team = None
        self.selected_their_team_who_gets_to_be_red_number = None
        self.start_game_button.set_enabled(False)
        self.status_bar = StatusBar()
        self.teams = Teams()
        self.their_team = None
        self.their_team_color = '?'
        self.who_gets_to_be_red_number = who_gets_to_be_red_number

        self.status_bar.update_text('Choose your positions, an opponent, and click Start.')

        if self.debug_mode:
            self.our_team_color = 'red'
            self.our_team = 'debug'
            self.their_team = 'otherDebug'
            self.their_team_color = 'black'
            self.change_game_state(STATE_OUR_TURN)

    def can_start_game(self):
        return self.selected_their_team is not None

    def start_game(self):
        self.their_team = self.selected_their_team

        if self.who_gets_to_be_red_number > self.selected_their_team_who_gets_to_be_red_number:
            self.our_team_color = 'red'
            self.their_team_color = 'black'
            self.change_game_state(STATE_OUR_TURN)
        else:
            self.our_team_color = 'black'
            self.their_team_color = 'red'
            self.change_game_state(STATE_THEIR_TURN)

    def change_game_state(self, state):
        self.game_state = state

        if state == STATE_OUR_TURN:
            self.status_bar.update_text("It's your move. Good luck!")
        elif state == STATE_OUR_WIN:
            self.status_bar.update_text("Congratulations! You win!")
        elif state == STATE_THEIR_WIN:
            self.status_bar.update_text("You lost. Maybe next time.")
        else:
            self.status_bar.update_text('Waiting for %s to make their move...' % self.their_team)
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, dict(action=ACTION_GAME_STATE_CHANGED, state=state)))

    def handle_move(self, team, row, col):
        color_of_move = self.our_team_color if team == self.our_team else self.their_team_color
        self.board.record_move(color_of_move, row, col)

        winning_team_color = self.board.is_win()

        if winning_team_color == self.their_team_color:
            self.change_game_state(STATE_THEIR_WIN)
        elif winning_team_color == self.our_team_color:
            self.change_game_state(STATE_OUR_WIN)
        elif team == self.our_team:
            if self.debug_mode:
                self.our_team_color = 'red' if self.our_team_color == 'black' else 'black'
            else:
                self.change_game_state(STATE_THEIR_TURN)
        elif team == self.their_team:
            self.change_game_state(STATE_OUR_TURN)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:

            if self.game_state == STATE_PREPARING:
                self.teams.check_click(event.pos[0], event.pos[1])
                self.start_game_button.check_click(event.pos[0], event.pos[1])
            elif self.game_state == STATE_OUR_TURN:
                self.board.make_move_click(event.pos[0], event.pos[1])

        elif event.type == pygame.USEREVENT:

            if event.action == ACTION_FIND_ME:
                if not event.team == self.our_team:
                    self.teams.found_team(event.team, event.row)

            # A move from the network. Ignore hearing a message from our own team, just in case.
            elif event.action == ACTION_MOVE and event.team == self.their_team:
                self.handle_move(event.team, event.row, event.col)

            # A move on our local board. Ignore clicking our board if it's not our turn.
            elif event.action == ACTION_MAKE_MOVE and self.game_state == STATE_OUR_TURN:
                # Announce to the network what the move was.
                if not self.debug_mode:
                    self.messages_to_send.put('%s|%s|%d|%d' % (self.our_team, ACTION_MOVE, event.row, event.col))
                # Update the board, check for a winner, and change turns.
                self.handle_move(self.our_team, event.row, event.col)
                self.messages_to_send.put('%s|%s|%s' % (self.our_team, ACTION_REFRESH, self.board.state_of_all_cells()))

            elif event.action == ACTION_SELECT_TEAM:
                self.selected_their_team = event.team
                self.selected_their_team_who_gets_to_be_red_number = event.who_gets_to_be_red_number
                self.start_game_button.set_enabled(self.can_start_game())

            elif event.action == ACTION_STATUS:
                self.status_bar.update_text(event.text)

        self.screen.fill(DARK_BLUE)
        self.board.draw(self.screen)
        self.status_bar.draw(self.screen)

        if self.game_state == STATE_PREPARING:
            self.start_game_button.draw(self.screen)
            self.teams.draw(self.screen)

