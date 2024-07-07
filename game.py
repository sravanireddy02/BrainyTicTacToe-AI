import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
background_color = pygame.Color("#CBC3E3")
button_x_color = pygame.Color("#0000FF")
button_o_color = pygame.Color("#FF0000")
text_color = pygame.Color("#000000")
board_line_color = pygame.Color("#000000")
x_color = pygame.Color("#FF0000")
o_color = pygame.Color("#0000FF")
pastel_green = pygame.Color("#77DD77")  # Pastel green for the "Play Again" button

screen = pygame.display.set_mode(size)

# Creating font objects
mediumFont = pygame.font.SysFont('arial', 28)
largeFont = pygame.font.SysFont('arial', 40)
moveFont = pygame.font.SysFont('arial', 60)
headingFont = pygame.font.SysFont('arial', 50)  # Font for the heading

# Game variables
player_name = ""
user = None
board = ttt.initial_state()
ai_turn = False
name_input_active = True
user_choice_active = False
cursor_visible = True
cursor_time = 0

input_box = pygame.Rect(width / 2 - 100, height / 2 - 30, 200, 50)
play_x_button = pygame.Rect(width / 8, height / 2 + 50, width / 4, 50)
play_o_button = pygame.Rect(5 * (width / 8), height / 2 + 50, width / 4, 50)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if name_input_active and input_box.collidepoint(event.pos):
                name_input_active = True
            else:
                name_input_active = False
            if user_choice_active and play_x_button.collidepoint(event.pos):
                user = ttt.X
                user_choice_active = False
            elif user_choice_active and play_o_button.collidepoint(event.pos):
                user = ttt.O
                user_choice_active = False
        if event.type == pygame.KEYDOWN:
            if name_input_active:
                if event.key == pygame.K_RETURN:
                    name_input_active = False
                    user_choice_active = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

    screen.fill(background_color)

    # Display heading
    if name_input_active:
        draw_text('BrainyTictactoe-AI', headingFont, text_color, screen, width / 2, 40)

    if name_input_active:
        draw_text('Enter your name:', mediumFont, text_color, screen, width / 2, height / 2 - 50)
        pygame.draw.rect(screen, pygame.Color("#FFFFFF"), input_box)
        draw_text(player_name, mediumFont, pygame.Color("#000000"), screen, width / 2, height / 2)

        cursor_time += pygame.time.get_ticks()
        if cursor_time >= 500:
            cursor_visible = not cursor_visible
            cursor_time = 0

        if cursor_visible:
            cursor = mediumFont.render('|', True, pygame.Color("#000000"))
            screen.blit(cursor, (input_box.x + input_box.w / 2 + mediumFont.size(player_name)[0] / 2, input_box.y + 10))
    elif user_choice_active:
        draw_text(f'Hello, {player_name}!', largeFont, text_color, screen, width / 2, height / 3 - 30)
        draw_text('Choose your side:', mediumFont, text_color, screen, width / 2, height / 3 + 30)

        pygame.draw.rect(screen, button_x_color, play_x_button)
        draw_text('Play as X', mediumFont, text_color, screen, play_x_button.centerx, play_x_button.centery)

        pygame.draw.rect(screen, button_o_color, play_o_button)
        draw_text('Play as O', mediumFont, text_color, screen, play_o_button.centerx, play_o_button.centery)
    else:
        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, board_line_color, rect, 3)
                if board[i][j] != ttt.EMPTY:
                    color = x_color if board[i][j] == ttt.X else o_color
                    move = moveFont.render(board[i][j], True, color)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = "Game Over: Tie."
            elif winner == user:
                title = f"Game Over: {player_name} wins!"
            else:
                title = "Game Over: AI wins."
        elif user == player:
            title = f"{player_name}'s turn ({user})"
        else:
            title = "AI's turn"
        title_surface = largeFont.render(title, True, text_color)
        title_rect = title_surface.get_rect()
        title_rect.center = (width / 2, 30)
        screen.blit(title_surface, title_rect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = ttt.result(board, (i, j))

        if game_over:
            again_button = pygame.Rect(width / 3, height - 65, width / 3, 50)
            pygame.draw.rect(screen, pastel_green, again_button)  # Pastel green for "Play Again" button
            draw_text("Play Again", mediumFont, text_color, screen, again_button.centerx, again_button.centery)
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if again_button.collidepoint(mouse):
                    time.sleep(0.2)
                    player_name = ""
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                    name_input_active = True

    pygame.display.flip()
