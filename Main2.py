from random import random, randrange

VACANT_CELL = -1
FINISH_FAILURE ='Board is unsolvable\n'
NOT_LEGIT = 'Board is not legit!\n'
FINISH_SUCCESS = 'Here is the solved board\n'
NOT_FINISH = 'not finished'


def board_filled(sudoku_board: list) -> bool:
 for i in range(9):
  for j in range(9):
   if sudoku_board[i][j] == VACANT_CELL:
    # If there is a cell that is vacant we'll return false
    return False
 return True

def remain_one_length_cell(possibilities : list) -> bool:
    # Iterating through the entire matrix list possibilities
    for i in range(9):
        for j in range(9):
            if len(possibilities[i][j]) == 1:
                return True

    return False

def is_there_none(possibilities : list) -> bool:
    # Iterating through the entire matrix list possibilities
    for i in range(9):
        for j in range(9):
            if possibilities[i][j] == None:
                return True

    return False


def defect_board(sudoku_board : list) -> bool:
    # Column
    for i in range(9):
        lst_of_nums = []

        for j in range(9):
            lst_of_nums.append(sudoku_board[j][i])

        if len(lst_of_nums) != len(list(set(lst_of_nums))):
            return True

    # Row
    for i in range(9):
        lst_of_nums = []

        for j in range(9):
            lst_of_nums.append(sudoku_board[i][j])

        if len(lst_of_nums) != len(list(set(lst_of_nums))):
            return True

    # Square
    for box_row in range(0, 9, 3):  # Iterate over the starting row of each square
        for box_col in range(0, 9, 3):  # Iterate over the starting column of each square
            subgrid = []
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    subgrid.append(sudoku_board[row][col])
            # Check if the subgrid has duplicates
            if len(subgrid) != len(set(subgrid)):
                return True

    return False




def options(sudoku_board : list, loc : tuple) -> list:

    # Getting row and column location from tuple loc (given argument)
    row_loc = loc[0]
    column_loc = loc[1]

    # If the location already has a number than returning empty list
    if sudoku_board[row_loc][column_loc] != VACANT_CELL:
        return []

    # Creating a dictionary for figuring what square is the location is in
    thirds = {0: 0, 1: 0, 2: 0, 3: 3, 4: 3, 5: 3, 6: 6, 7: 6, 8: 6}

    # Figuring what third is the location in
    start_of_square_row = thirds[row_loc]
    start_of_square_column = thirds[column_loc]

    # This list will hold the number that can't be in the returned list
    list_of_taken_nums = []

    # Iterating through the square which the location is in and adding numbers to the taken numbers list as needed
    for i in range(start_of_square_row, start_of_square_row+3):
        for j in range(start_of_square_column, start_of_square_column+3):
            curr_num = sudoku_board[i][j]
            if sudoku_board[i][j] != VACANT_CELL:
                list_of_taken_nums.append(curr_num)

    # Iterating through the row of the location adding numbers to the taken numbers list as needed
    for i in range(9):
        curr_num = sudoku_board[row_loc][i]
        if curr_num != VACANT_CELL:
            list_of_taken_nums.append(curr_num)

    # Iterating through the column of the location adding numbers to the taken numbers list as needed
    for i in range(9):
        curr_num = sudoku_board[i][column_loc]
        if curr_num != VACANT_CELL:
            list_of_taken_nums.append(curr_num)


    # This list will hold the numbers that can be in the location
    list_of_options = []

    # Adding numbers from 1 to 9 if not in the taken numbers list
    for i in range(1,10):
        if i not in list_of_taken_nums:
            list_of_options.append(i)

    # If the list of numbers that can be in the location is empty then returning None
    if len(list_of_options) == 0:
        return None

    # Returning the list of numbers that can be in the location
    return list_of_options


def possible_digits(sudoku_board : list) -> list:

    # Using the "options" function, creating a 9x9 matrix list that holds in each cell the list of numbers that can be in the location in the sudoku_board variable
    board_of_options = [[options(sudoku_board,(i,j)) for j in range(9)] for i in range(9)]

    # Retuning the matrix list
    return  board_of_options


def one_stage(sudoku_board : list, possibilities : list):

    #while not board_filled(sudoku_board):
    while True:

        # Iterating through the entire matrix list sudoku_board
        for i in range(9):
            for j in range(9):

                # Getting the current cell list of possible numbers to put in
                curr_cell = possibilities[i][j]

                # If the list is None type then there is an illegal thing in the sudoku_board, and we'll return the constant "FINISH_FAILURE"
                if curr_cell == None:
                    return FINISH_FAILURE

                # If the list has only one number in it:
                if len(curr_cell) == 1:
                    # Getting the number that needs to be added
                    num_to_enter = curr_cell[0]
                    # Entering the number to the location in the sudoku_board
                    sudoku_board[i][j] = num_to_enter

                    # Updating the matrix list of possibilities
                    possibilities = possible_digits(sudoku_board)

        if board_filled(sudoku_board):
            return FINISH_SUCCESS

        if is_there_none(possibilities):
            return FINISH_FAILURE

        if not remain_one_length_cell(possibilities):
            # We'll iterate through the possibilities matrix using the i index for row and the j index for column, searching for the shortest list of possible numbers to add
            i = 0
            j = 0
            # First we'll need to find the first place that isn't filled yet
            while len(possibilities[i][j]) < 2:
                if j == 8:
                    # If reached the end of current row in index i then we enter new row and return j index to 0
                    i += 1
                    j = 0
                j += 1
                # The loop will be assured to stop at some point because we entered this if because the board is not completely filled

            # After reaching the first place where the cell is empty then we mark it as the current location with the shortest list of numbers to add
            min_cor = (i, j)
            min_val = len(possibilities[i][j])

            # Iterating through the possibilities matrix to find minimal list of numbers to add
            for i in range(9):
                for j in range(9):
                    curr_cell_length = len(possibilities[i][j])
                    if 2 <= curr_cell_length < min_val:
                        min_cor = (i, j)
                        min_val = curr_cell_length

            # Returning the location of the best place to start entering numbers (a tuple) and the constant "NOT_FINISH"
            return min_cor, NOT_FINISH


def fill_board(sudoku_board : list, possibilities : list):

    # This variable will hold the result after calling the "one_stage" function
    output = one_stage(sudoku_board, possibilities)

    # If after calling the function "one_stage" the result is the constant "FINISH_FAILURE" then the board is illegal, and we'll return also the constant "FINISH_FAILURE"
    if output == FINISH_FAILURE:
        return FINISH_FAILURE

    # While the sudoku_board is not filled
    while output != FINISH_SUCCESS:

        # We get here if the "one_stage" function output was "NOT_FINISH" and we get a location to continue to fill the board
        # Getting the location: row as x, column as y
        x = output[0][0]
        y = output[0][1]

        # Printing a message to tell the user where is the best place to continue and to enter a number
        print_board(sudoku_board)
        print("Coordinate ("+str(x)+" , "+str(y)+") it is the best option!")
        print("legal number to enter:",possibilities[x][y])

        # Continuously prompt the user until they enter a valid number between 1 and 9
        while True:
            try:
                choice = int(input("Enter number between 1 - 9: "))

                # Check if the choice is within the valid range (1 to 9)
                if choice < 1 or choice > 9:
                    continue  # If the number is not between 1 and 9, keep prompting
                break  # Exit the loop if valid input is entered
            except ValueError:
                continue  # If the input is not an integer, continue asking for a valid number

        # This will hold the list of possible numbers in the location
        options_for_nums_in_coordinate = possibilities[x][y]

        # If the number that the user entered isn't in the list than we get illegal board, and we return the constant "FINISH_FAILURE"
        if choice not in options_for_nums_in_coordinate:
            return FINISH_FAILURE


        # If the number from user is in the list then we enter it to the location
        sudoku_board[x][y] = choice
        # Updating the possibilities matrix
        possibilities = possible_digits(sudoku_board)


        # Trying to fill the sudoku_board using the "one_stage" function
        output = one_stage(sudoku_board, possibilities)
        # If the output from the "one_stage" function was "FINISH_FAILURE" then returning the constant
        if output == FINISH_FAILURE:
            return FINISH_FAILURE
        # Else output holds "FINISH_SUCCESS" or "NOT_FINISH"

    # If we got here, then the sudoku_board is filled completely and we return the constant
    return FINISH_SUCCESS

def create_random_board(sudoku_board : list):

    # Getting a random number from 10 to 20
    N = randrange(10,21)

    # Creating a list in length 81 where in every cell there is tuple of a location
    options_list = []
    for i in range(9):
        for j in range(9):
            options_list.append((i,j))

    # Iterating N times
    for i in range(N):

        # Getting a random number from 0 to the list length - 1
        K = randrange(0,len(options_list))

        # Getting the tuple of location from the K'th element
        loc_of_K = options_list[K]
        row_loc_K = loc_of_K[0]
        column_loc_K = loc_of_K[1]

        # Removing the K'th element from list of available places to enter numbers
        options_list.pop(K)

        # Getting the list of numbers that can be added to the location using function "options"
        list_of_options = options(sudoku_board,loc_of_K)

        # Getting a random index number from 0 to the list of options length
        rnd_index = randrange(0,len(list_of_options))

        # Getting the number from the list of options using the random index
        chosen_rnd_num = list_of_options[rnd_index]

        # Entering the chosen number into the location in the sudoku_board
        sudoku_board[row_loc_K][column_loc_K] = chosen_rnd_num

        # After iterating N times, the sudoku_board will be filled, and we'll return from the function


def print_board(sudoku_board : list):

    # Printing the first line of the board
    print("---------------------------\n")

    # Iterating 9 times
    for i in range(9):

        # We'll start printing the current row:
        row_string = "|"

        # We'll get all numbers (9) from the current row
        for j in range(9):

            # Getting the number of the current place (in index j)
            curr_num = sudoku_board[i][j]

            # if there is a number in the current place
            if curr_num != VACANT_CELL:
                # Printing the number and a '|'
                row_string += str(curr_num) + " |"
            else:
                # Else, there is no number there, and we'll print " " and "|"
                row_string += " " + " |"

        # After concatenating the full line we'll go down a line
        row_string += "\n"

        # Printing the full line
        print(row_string)

        # After every row there's a line, we'll print it and move to the next row (next iteration)
        print("---------------------------\n")

def print_board_to_file(sudoku_board : list, file_name):

    # Printing the first line of the board
    file_name.write("---------------------------\n")

    # Iterating 9 times
    for i in range(9):

        # We'll start printing the current row:
        row_string = "|"

        # We'll get all numbers (9) from the current row
        for j in range(9):

            # Getting the number of the current place (in index j)
            curr_num = sudoku_board[i][j]

            # if there is a number in the current place
            if curr_num != VACANT_CELL:
                # Printing the number and a '|'
                row_string += str(curr_num) + " |"
            else:
                # Else, there is no number there, and we'll print " " and "|"
                row_string += " " + " |"

        # After concatenating the full line we'll go down a line
        row_string += "\n"

        # Printing the full line
        file_name.write(row_string)

        # After every row there's a line, we'll print it and move to the next row (next iteration)
        file_name.write("---------------------------\n")








# Main:
example_board = [[5,3,-1,-1,7,-1,-1,-1,-1],
 [6,-1,-1,-1,-1,-1,1,-1,-1],
 [-1,-1,9,-1,-1,-1,-1,6,-1],
 [-1,-1,-1,-1,6,-1,-1,-1,3],
 [-1,-1,-1,8,-1,3,-1,-1,1],
 [-1,-1,-1,-1,-1,-1,-1,-1,-1],
 [-1,6,-1,-1,-1,-1,-1,-1,-1],
 [-1,-1,-1,-1,1,-1,-1,-1,-1],
 [-1,-1,-1,-1,8,-1,-1,-1,9]]

perfect_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

impossible_board = [[5,1,6,8,4,9,7,3,2],
 [3,-1,7,6,-1,5,-1,-1,-1],
 [8,-1,9,7,-1,-1,-1,6,5],
 [1,3,5,-1,6,-1,9,-1,7],
 [4,7,2,5,9,1,-1,-1,6],
 [9,6,8,3,7,-1,-1,5,-1],
 [2,5,3,1,8,6,-1,7,4],
 [6,8,4,2,-1,7,5,-1,-1],
 [7,9,1,-1,5,-1,6,-1,8]]

bug_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,9],
 [1,9,8,3,4,2,5,6,7],
 [8,5,9,7,6,1,4,2,3],
 [4,2,6,8,5,3,7,9,1],
 [7,1,3,9,2,4,8,5,6],
 [9,6,1,5,3,7,2,8,4],
 [2,8,7,4,1,9,6,3,5],
 [3,4,5,2,8,6,1,7,9]]

# This board has two solutions - one for 2 and one for 4
interesting_board = [[5,3,4,6,7,8,9,1,2],
 [6,7,2,1,9,5,3,4,8],
 [1,9,8,3,4,2,5,6,7],
 [-1,-1,-1,7,6,1,4,2,3],
 [-1,-1,-1,8,5,3,7,9,1],
 [-1,-1,-1,9,2,4,8,5,6],
 [-1,-1,-1,-1,3,7,2,8,4],
 [-1,-1,-1,-1,1,9,6,3,5],
 [-1,-1,-1,-1,8,6,1,7,9]]


random_board = [[VACANT_CELL for j in range(9)] for i in range(9)]
create_random_board(random_board)

list_of_names = ["example_board:\n","perfect_board:\n","impossible_board:\n","bug_board:\n","interesting_board:\n","random_board:\n"]
list_of_boards = [example_board,perfect_board,impossible_board,bug_board,interesting_board,random_board]

# Writing to the file
with open("solved_sudoku.txt", "w") as file:

    for i in range(len(list_of_boards)):

        file.write(list_of_names[i])

        board = list_of_boards[i]

        if board_filled(board):
            if not defect_board(board):
                file.write(FINISH_SUCCESS)
                print_board_to_file(board, file)
                file.write("\n")
            else: # Defect board
                file.write(NOT_LEGIT)
                file.write("\n")


        else: # If board not filled
            possibilities = possible_digits(board)

            if fill_board(board, possibilities) == FINISH_SUCCESS:
                file.write(FINISH_SUCCESS)
                print_board_to_file(board,file)
                file.write("\n")
            else:
                file.write(FINISH_FAILURE)
                file.write("\n")
