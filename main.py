import pygame, sys, random, copy

pygame.init()

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption('Connect Four')

font = pygame.font.SysFont('comicsans', 60)

# red = (255, 0, 68)
# yellow = (255, 220, 78)
# blue = (22, 0, 68)

def render_board(screen, board, colors, res):
    for i in range(len(board)):
        for j in range(len(board[i])):
            pygame.draw.rect(screen, (22, 0, 68), (j*res, i*res+res, res, res))
            pygame.draw.circle(screen, (0,0,0), ((j+0.5)*res, (i+1.5)*res), res/2-5)

            if board[i][j] == 1:
                pygame.draw.circle(screen, colors[0], ((j+0.5)*res, (i+1.5)*res), res/2-5)
            elif board[i][j] == 2:
                pygame.draw.circle(screen, colors[1], ((j+0.5)*res, (i+1.5)*res), res/2-5)

def render_hovering_circle(screen, current_color, res):
    pygame.draw.circle(screen, current_color, (pygame.mouse.get_pos()[0], res/2), res/2-5)

def is_valid(board, j):
    col = [board[i][j] for i in range(len(board))]
    return 0 in col

def add_piece(board, j, turn):
    if j == None:
        valid_locations = get_valid_locations(board)
        j = random.choice(valid_locations)

    for i in range(len(board)-1):
        if board[i][j] == 0 and board[i+1][j] != 0:
            board[i][j] = turn+1
            return

    board[len(board)-1][j] = turn+1

def get_valid_locations(board):
    valid_locations = []

    for i in range(len(board[0])):
        if is_valid(board, i):
            valid_locations.append(i)

    return valid_locations

def check_for_win(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            piece = board[i][j]

            if piece == 0:
                continue

            for dir in [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (1,1), (0,1), (1,1)]:
                for k in range(1, 4):
                    i2 = i+(dir[1]*k)
                    j2 = j+(dir[0]*k)

                    if (i2 < 0 or i2 > len(board)-1) or (j2 < 0 or j2 > len(board[0])-1):
                        break

                    other_piece = board[i2][j2]

                    if other_piece == piece:
                        if k == 3:
                            return piece-1, True
                    else:
                        break

    return None, False

def check_for_tie(board):
    board_1d = []

    for row in board:
        board_1d.extend(row)

    return 0 not in board_1d

def main():
    rows = 6
    cols = 7
    res = 100
    turn = 0
    colors = [(255, 0, 68), (255, 220, 78)]
    players = ['RED', 'YELLOW']

    board = [[0 for j in range(cols)] for i in range(rows)]

    game_over = False

    while not game_over:
        current_color = colors[turn]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_valid(board, event.pos[0]//res):
                    add_piece(board, event.pos[0]//res, turn)
                    turn += 1
                    turn %= 2

        screen.fill((0,0,0))

        render_board(screen, board, colors, res)
        render_hovering_circle(screen, current_color, res)

        pygame.display.update()

        winner, game_won = check_for_win(board)
        game_tied = check_for_tie(board)

        if game_won:
            i = 0
            while i < 5000:
                label = font.render(f'{players[winner]} won the game!', 1, (255, 109, 73))
                screen.blit(label, (screen.get_width()/2-label.get_width()/2, 10))
                pygame.display.update()
                i += 1

        if game_tied:
            i = 0
            while i < 5000:
                label = font.render('The game has been tied...', 1, (255, 109, 73))
                screen.blit(label, (screen.get_width()/2-label.get_width()/2, 10))
                pygame.display.update()
                i += 1

        game_over = game_won or game_tied

    main()

def is_terminal_node(board):
    return check_for_win(board)[1] or check_for_tie(board)

#Minimax algorithm with alpha beta pruning, Not working good current due to random move picking...

# def minimax_ab(board, depth=100, alpha=-float('inf'), beta=float('inf'), maximising=True):
#     valid_locations = get_valid_locations(board)
#     is_terminal = is_terminal_node(board)
#
#     if is_terminal:
#         if check_for_win(board)[0] == 1:
#             return float('inf'), None
#         elif check_for_win(board)[0] == 0:
#             return -float('inf'), None
#         else:
#             return 0, None
#
#     if depth == 0:
#         return 0, None
#
#     if maximising:
#         value = -float('inf')
#         best_col = random.choice(valid_locations)
#
#         for col in valid_locations:
#             board_copy = copy.deepcopy(board)
#             add_piece(board_copy, col, 1)
#
#             eval = minimax_ab(board_copy, depth-1, alpha, beta, False)[0]
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#
#             if eval > value:
#                 value = eval
#                 best_col = col
#
#         return value, best_col
#
#     else:
#         value = float('inf')
#         best_col = random.choice(valid_locations)
#
#         for col in valid_locations:
#             board_copy = copy.deepcopy(board)
#             add_piece(board_copy, col, 0)
#
#             eval = minimax_ab(board_copy, depth-1, alpha, beta, True)[0]
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#
#             if eval < value:
#                 value = eval
#                 best_col = col
#
#         return value, best_col

def minimax(board, depth=5, maximising=True):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if is_terminal:
        if check_for_win(board)[0] == 1:
            return float('inf'), None
        elif check_for_win(board)[0] == 0:
            return -float('inf'), None
        else:
            return 0, None

    if depth == 0:
        return 0, None

    if maximising:
        value = -float('inf')
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            board_copy = copy.deepcopy(board)
            add_piece(board_copy, col, 1)

            eval = minimax(board_copy, depth-1, False)[0]

            if eval > value:
                value = eval
                best_col = col

        return value, best_col

    else:
        value = float('inf')
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            board_copy = copy.deepcopy(board)
            add_piece(board_copy, col, 0)

            eval = minimax(board_copy, depth-1, True)[0]

            if eval < value:
                value = eval
                best_col = col

        return value, best_col

def main_ai():
    rows = 6
    cols = 7
    res = 100
    turn = 0
    colors = [(255, 0, 68), (255, 220, 78)]
    players = ['YOU', 'AI']

    board = [[0 for j in range(cols)] for i in range(rows)]

    game_over = False

    while not game_over:
        current_color = colors[turn]

        if turn == 1:
            best_col = minimax(board, 5)[1]

            add_piece(board, best_col, turn)

            turn += 1
            turn %= 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    if is_valid(board, event.pos[0]//res):
                        add_piece(board, event.pos[0]//res, turn)
                        turn += 1
                        turn %= 2

        #Render
        screen.fill((0,0,0))

        render_board(screen, board, colors, res)
        render_hovering_circle(screen, current_color, res)

        pygame.display.update()

        #Check board
        winner, game_won = check_for_win(board)
        game_tied = check_for_tie(board)

        if game_won:
            i = 0
            while i < 5000:
                label = font.render(f'{players[winner]} won the game!', 1, (255, 109, 73))
                screen.blit(label, (screen.get_width()/2-label.get_width()/2, 10))
                pygame.display.update()
                i += 1

        if game_tied:
            i = 0
            while i < 5000:
                label = font.render('The game has been tied...', 1, (255, 109, 73))
                screen.blit(label, (screen.get_width()/2-label.get_width()/2, 10))
                pygame.display.update()
                i += 1

        game_over = game_won or game_tied

    #Restart game
    main_ai()

main_ai()
