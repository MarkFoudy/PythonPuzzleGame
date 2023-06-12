from turtle import *
from time import *
from random import randint
from puzzle_utilities import draw_rec
from datetime import datetime


def open_file(filename, use_mode):
    '''
    Opens filename using the supplied mode
    '''
    try:
        file = open(filename, mode =use_mode)
        return file
    except IOError:
        # caller will handle the error
        return None
        
def leader_read(filename, xpos, ypos, player_name):
    '''
    Reads in the leaderboard file and display contents on screen.
    Creates a dictionary to hold score updates.
    '''
    try:
        file = open(filename, mode ="r")
        lead_dict = {}
        lead_str = "Leaders:\n\n"
        for line in file:
            line_list = line.strip().split(",")
            player_name = line_list[0]
            player_score = line_list[1]
            lead_str = lead_str + player_name + ": " + player_score + "\n"
            lead_dict[player_name] = int(player_score)
        
        t = Turtle()
        t.up()
        t.hideturtle()
        t.color("blue")
        n = len(lead_dict)
        ypos = ypos - (n+1) * 34
        t.setposition(xpos,ypos)
        t.write(lead_str,font=("Arial",12,"bold"))
        file.close()
        return (lead_dict, t)
    except IOError:
        print("Can't open leaderboard file!")


def leader_write(filename, lead_dict):
    '''
    Writes the leaderboard dictionary to leaderboard filename.
    
    '''
    try:
        with open("leaderboard.txt", mode="w") as lw:
            tup_list = list(lead_dict.items())
            tup_list.sort(key=lambda t: t[1])
            for player,score in tup_list:
                lw.write(player + "," + str(score) + "\n")
            
    except IOError:
        print("Can't open/write to leaderboard file!")


def bad_file(win, error_file, error_message):
    '''
    Writes error message to error_file and displays the 'file_error.gif.'
    '''
    current = str(datetime.now().strftime("%c"))
    error_file.write(current + error_message + "\n")
    t = Turtle()
    t.up()
    t.setposition(0,0)
    win.addshape("Resources/file_error.gif")
    t.shape("Resources/file_error.gif")
    sleep(3)
    t.hideturtle()
    return

def get_moves_allowed(win, error_file):
    '''
    Prompt in display for the number of moves the user selects.
    Ensures user selection is within specified range.
    '''
    
    num_moves = win.numinput("CS5001 Puzzle Slide - Moves", "Enter the number of moves (chances) you want (5-200)?", \
                50, minval=5, maxval=200)
    return int(num_moves)

def is_solved(loc_dict, grid):
    '''
    Checks to see if puzzle is solved by checking its current location in the grid
    against the dictionary of correct positions for a solved puzzle.
    '''
    for row in range(len(grid)):
        for col in range(len(grid)):
            file_no,t,image_name = grid[row][col] # this is a tuple            
            if loc_dict[file_no][0] != (row,col):
                return False
    return True

def display_tiles(puz_file, win):
    '''
    Displays puzzle tiles and creates the data structures needed to hold information regarding
    the tiles and current state of play.
    '''
    
    # get configuration information from *.puz file
    name,puz_name = puz_file.readline().split()
    num,num_tiles = puz_file.readline().split()
    size,puz_size = puz_file.readline().split()
    tn,thumbnail_file = puz_file.readline().split()
    num_tiles = int(num_tiles)
    puz_size = int(puz_size)
        
    # determine the number of rows/cols based on the size of num_tiles
    if num_tiles == 16:
        rows = 4
        cols = 4
    elif num_tiles == 9:
        rows = 3
        cols = 3
    elif num_tiles == 4:
        rows = 2
        cols = 2
    else:
        # log error in error file
        error_file = game_repository[7]
        bad_file(win, error_file, ":Error: Malformed puzzle " + puz_name + ". LOCATION: display_tiles()" )
        return
            
    # create location dictionary
    t_grid = []
    loc_dict = {}
    pos_dict = {}
    counter = num_tiles
    # starting positions for grid locations unscrambled
    xpos_start = -260
    ypos = 300
    for row in range(rows):
        xpos = xpos_start
        ypos = ypos - puz_size
        new_row = []
        for col in range(cols):
            order_num, image_name = puz_file.readline().split()
            order_num = int(order_num.strip(":"))
            t = Turtle()
            loc_dict[counter] = ((row,col),t,image_name)
            win.addshape(image_name)            
            new_row.append((counter, t, image_name))
            # enter the solved location of this turtle to the pos dictionary
            pos_dict[counter] = ((xpos,ypos))
            counter = counter - 1
            xpos = xpos + puz_size
        t_grid.append(new_row)     

    #scramble the puzzle
    scramble(t_grid, num_tiles)    
    
    # adjust starting location of initial tile
    xpos_start = -260
    ypos = 300

    # display scrambled puzzle
    for row in range(rows):
        xpos = xpos_start
        ypos = ypos - puz_size
        for col in range(cols):
            # a grid element is a tuple:(image_number, turtle, image_name)
            counter, t, image_name = t_grid[row][col]
            t.up()
            t.setposition(xpos, ypos)
            t.shape(image_name)            
            xpos = xpos + puz_size
    t_thumbnail = display_thumb(win, 270, 300, thumbnail_file)
                   
    return t_grid,loc_dict,pos_dict,puz_size,t_thumbnail

def swap(t_grid,i,j,k,l):
    '''
    Swaps two elements in the 2d list of puzzle elements.
    '''
    temp = t_grid[i][j]
    t_grid[i][j] = t_grid[k][l]
    t_grid[k][l] = temp


def display_thumb(win, xpos, ypos, thumbnail_file):
    '''
    Displays thumbnail image of the current puzzle on the edge of the leaderboard.
    '''
    t = Turtle()
    t.up()
    t.setposition(xpos,ypos)
    win.addshape(thumbnail_file)            
    t.shape(thumbnail_file)
    return t
    

def scramble(t_grid,num_tiles):
    '''
    Scrambles the tiles by randomly swapping elements in the tile grid.
    '''
    n = len(t_grid)
    # randomly swap half the tiles
    for x in range(num_tiles//2):
        # get random indices to swap
        i = randint(0, n-1)
        j = randint(0, n-1)
        k = randint(0, n-1)
        l = randint(0, n-1)
        # swap elements
        swap(t_grid,i,j,k,l)
        
                
def get_zero_neighbor(grid,i,j):
    '''
    Checks to see if the grid location of a tile is next to a blank tile,
    horizontally or vertically.
    '''
    # check to see if blank tile is adjacent to grid[i][j]
    size = len(grid)
    # left
    if j-1 >= 0:
        num,t,image_name = grid[i][j-1]
        if 'blank' in image_name:
            return (i, j-1)
    # right
    if j+1 < size:
        num,t,image_name = grid[i][j+1]
        if 'blank' in image_name:
            return (i, j+1)
    # up
    if i-1 >= 0:
        num,t,image_name = grid[i-1][j]
        if 'blank' in image_name:
            return (i-1, j)
    # down
    if i+1 < size:
        num,t,image_name = grid[i+1][j]
        if  'blank' in image_name:
            return (i+1, j)
    # if there is no blank neighbor
    return (-1, -1)

def init_user_control_board(win):
    '''
    Creates user control board layout and displays clickable images
    allowing the user to reset, load or quit the game.
    '''
    # displays reset button
    t1 = Turtle()
    t1.up()
    t1.setposition(60.0,-300.0)
    win.addshape("Resources/resetbutton.gif")            
    t1.shape("Resources/resetbutton.gif")
    
    # displays load button
    t2 = Turtle()
    t2.up()
    t2.setposition(158.0,-301.0)
    win.addshape("Resources/loadbutton.gif")            
    t2.shape("Resources/loadbutton.gif")
   
    # displays quit button
    t3 = Turtle()
    t3.up()
    t3.setposition(250.0,-300.0)
    win.addshape("Resources/quitbutton.gif")            
    t3.shape("Resources/quitbutton.gif")
    
    return (t1,t2,t3)


def end_game(win,image_file):
    '''
    Displays winner's message and also displays the ending credits.
    '''
    t = Turtle()
    t.up()
    t.setposition(0,0)
    win.addshape(image_file)            
    t.shape(image_file)

    # display ending credits
    sleep(2) 
    t = Turtle()
    t.up()
    t.setposition(0,-10)
    win.addshape("Resources/credits.gif")            
    t.shape("Resources/credits.gif")
    sleep(4) 
    win.bye()


def play_game():
    '''
    Main driver in game containing within it nested functions which are excuted on clicks.
    These functions are nested within play_game for the purpose of sharing game playing data structures.
    '''
    
    def do_reset(xpos,ypos):
        '''
        Resets game board to default and unscrambled positions for the tiles.
        '''
        t_grid = game_repository[0]
        loc_dict = game_repository[1]
        pos_dict = game_repository[8]
        
        keys_list = list(loc_dict.keys())
        keys_list.sort(reverse=True)

        for num in keys_list:
            grid_position,t,image_name = loc_dict[num]
            
            # get where the turtle should be placed in the grid
            i,j  = grid_position
              
            # get where the turtle should be placed in the display
            xpos,ypos = pos_dict[num]

            # move the turtle to its correct postions in the grid and on the display
            t.hideturtle()
            t.setposition(xpos,ypos)
            t.shape(image_name)
            t.showturtle()
            # num, t, image_name
            t_grid[i][j] = (num,t,image_name)

        # update the game_repository
        game_repository[0] = t_grid
            

    def do_load(xpos,ypos):
        '''
        Activated when user clicks and provides menu allowing user to select different
        puzzle games.
        '''
        # prompt user selection options
        f_names = "Enter the name of the puzzle you wish to load. Choices are:\n" + \
                  "luigi.puz\nsmiley.puz\nfifteen.puz\nyoshi.puz\nmario.puz"
        
        user_selection = win.textinput("Load Puzzle", f_names)
        puz_file = open_file(user_selection, "r")
        
        # if puzzle filename is incorrect display error image and write to error file
        if puz_file == None:
            error_file = game_repository[7]
            bad_file(win, error_file, ":Error: Could not open file " + user_selection + ". LOCATION: do_load()" )
        else:
            grid = game_repository[0]
            t_thumbnail = game_repository[9]
            t_thumbnail.up()
            t_thumbnail.hideturtle()
            # clear the current puzzle
            for row in range(len(grid)):
                for col in range(len(grid)):
                    num,t,imf = grid[row][col]
                    t.up()
                    t.hideturtle()
                    
            # display new puzzle
            t_grid,loc_dict,pos_dict,puz_size,t_thumbnail = display_tiles(puz_file, win)
            
            # update the game data repository
            game_repository[0] = t_grid
            game_repository[1] = loc_dict
            game_repository[2] = puz_size
            game_repository[8] = pos_dict
            game_repository[9] = t_thumbnail


    def do_quit(xpos,ypos):
        '''
        Displays quitmsg.gif and closes the game.
        '''
        error_file = game_repository[7]
        error_file.close()
        t = Turtle()
        t.up()
        t.setposition(0,20)
        win.addshape("Resources/quitmsg.gif")            
        t.shape("Resources/quitmsg.gif")
        sleep(2) 
        win.bye()

    def do_board_click(xpos, ypos):
        '''
        Accepts user clicks and determines if clicks are within game board tiles.
        For clicks on tiles next to a blank the tiles are swapped and the number of player moves
        are incremented and displayed.  If clicked tile is not next to a blank tile no action is taken.
        '''
        
        # get game_repository assests out
        grid = game_repository[0]
        loc_dict = game_repository[1]
        puz_size = game_repository[2]
        moves_allowed,moves_made = game_repository[3]
        tm = game_repository[4]
        lead_dict = game_repository[5]
        player_name = game_repository[6]

        if moves_made == moves_allowed:
            end_game(win, "Resources/Lose.gif")
            return
                
        delta = puz_size//2
        # check for mouse click within board tiles
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                num,t_obj,image_name = grid[i][j]
                x,y = t_obj.position()
                if x - delta  <=  xpos <= x + delta and y - delta <= ypos <= y + delta:
                    # is this tile next to the blank?
                    i_b,j_b = get_zero_neighbor(grid,i,j)
                    if i_b != -1 and j_b != -1:
                        num_b,t_b,image_name_b = grid[i_b][j_b]
                        x_b,y_b = t_b.position()
                       
                        # move the blank
                        t_b.clear()
                        t_b.setposition(x,y)
                        t_b.shape(image_name_b)

                        # move the other tile.
                        t_b.clear()
                        t_obj.setposition(x_b,y_b)
                        t_obj.shape(image_name)

                        # swap respective grid elements 
                        swap(grid,i,j,i_b,j_b)             
                        
                        moves_made = moves_made + 1
                        game_repository[3] = (moves_allowed,moves_made)
                        tm.clear()
                        tm.write("Player Moves: " + str(moves_made), font=("Arial",18,"bold"))

                        if is_solved(loc_dict,grid): 
                            #  update leader score and write to leader file
                            lead_dict[player_name] = lead_dict[player_name] + moves_made
                            leader_write("leaderboard.txt", lead_dict)
                            end_game(win, "Resources/winner.gif")       

    game_repository = []    
    
    # create the display window 
    setup(800,800)
    win = Screen()
    
    # splash page
    t = Turtle()
    t.up()
    t.setposition(0,0)
    win.addshape("Resources/splash_screen.gif")            
    t.shape("Resources/splash_screen.gif")
    sleep(4) 
    win.clearscreen()

    error_file = open_file("5001_puzzle.err", "a")
           
    # get player name
    t = Turtle()
    player_name = win.textinput("CS5001 Puzzle Slide", "Your Name:")    

    # default puzzle to be loaded at startup
    puzzle_name = "mario.puz"
    sleep(1)

    # prompt user for how many moves per game
    moves_allowed = get_moves_allowed(win, error_file)
    sleep(1) 
         
    # create boarder for game board
    draw_rec(t,-340.0,300.0,450,500,7,"black")

    # create boarder for leaderboard
    draw_rec(t,140.0,300.0,185,500,7,"blue")
    
    # read in leaderboard file
    lead_dict,t_lead = leader_read("leaderboard.txt",160,270,player_name)
    
    # create rectangle to house user controls.
    draw_rec(t,-340.0,-250.0,665,100,7,"black")

    # create and display the control buttons   
    reset,load,quit_game = init_user_control_board(win)

    # create and display default mario puzzle
    puz_file = open_file(puzzle_name, "r")
    t_grid,loc_dict,pos_dict,puz_size,t_thumbnail = display_tiles(puz_file, win)      
         
    # check to see if leader file was empty
    # put current player in the dictionary
    if not player_name in lead_dict:
        lead_dict[player_name] = 0

    # create move turtle
    tm = Turtle()
    tm.hideturtle()
    tm.up()
    tm.setposition(-295,-310)

    # initialize the game repository
    game_repository.append(t_grid)
    game_repository.append(loc_dict)
    game_repository.append(puz_size)
    game_repository.append((int(moves_allowed),0))
    game_repository.append(tm)
    game_repository.append(lead_dict)
    game_repository.append(player_name)
    game_repository.append(error_file)
    game_repository.append(pos_dict)
    game_repository.append(t_thumbnail)

    # bind the functions for clicking on the control buttons
    reset.onclick(do_reset)
    load.onclick(do_load)
    quit_game.onclick(do_quit)

    # bind the function for clicking on the board tiles
    win.onclick(do_board_click)
    win.mainloop()
    error_file.close()
   
def main():
    play_game()
main()
        
