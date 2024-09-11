import numpy as np
# making a class called game_map
class game_map:

    def __init__(self, map_file, guard_file):
        try: # try to open the map file
            file_handler = open(map_file)
        # if the file does not exist, exit the program to avoid crashing
        except:
            exit()
        # this reads each line in the file and initializes it
        self.grid = file_handler.readlines()
        # printing the lines in the map file
        for line in self.grid:
            print(line.rstrip())
        # creating a 2D list of the map file and initializes it
        self.grid = [[c for c in line.rstrip()] for line in self.grid]
        # try to open the guard file
        try:
            file_handler_2 = open(guard_file)
        # if the file does not exist, exist the program instead of crashing
        except:
            exit()
        # assigning the string of the lines of the guard file to a variable
        list_of_guards = file_handler_2.readlines()

        # initializing the player's position and the exit square's position as None
        self.player_pos = None
        self.exit_pos = None
        # for a row in the 2D list
        for row in range(len(self.grid)):
            # for a column in the 2D list
            for col in range(len(self.grid[row])):
                # if that row and column is the letter P
                if self.grid[row][col] == "P":
                    # store the player's position at this row and column
                    self.player_pos = (row, col)
                # if that row and column is the letter E
                elif self.grid[row][col] == "E":
                    # store the player's position at this row and column as the exit position
                    self.exit_pos = (row, col)

        # populating guard list with guard objects and updating grid with guards
        self.guards_list = []
        for line in list_of_guards:
            # i represents each string character in the guard file
            i = line.split()
            # the first string in the line is converted into an int which is the row in the guard class
            # the second string in the line is converted into an int which is the column of the guard class
            # the third string until the rest of the string in the line is the movement of the guard
            guard_object = guard(int(i[0]), int(i[1]), int(i[2]), i[3:])
            # initializing all the guard objects in a list
            self.guards_list.append(guard_object)

    def get_grid(self):
        # create a copy of the 2D list of the map grid and replace guard positions with "G"
        grid_copy = [row[:] for row in self.grid]
        for guard in self.guards_list:
            guard_row, guard_col = guard.get_location()
            grid_copy[guard_row][guard_col] = "G"
        return grid_copy
    def get_guards(self):
        # returns a stored variable that contains the list of guards as objects
        return self.guards_list
    def update_guards(self):
        # for each guard object in the guard object list
        for guard in self.guards_list:
            # move each guard using the move method
            guard.move(self.get_grid())
    def update_player(self, direction):
        # the player's position
        player_row, player_col = self.player_pos

        # update the player's position based on the given direction
        if direction == "L" and player_col > 0 and self.grid[player_row][player_col - 1] != "#":
            # if the player chooses left, and the players column is within bounds, and to the left of them is not a wall
            self.grid[player_row][player_col - 1] = "P"
            # the player moves one square left
            self.grid[player_row][player_col] = " "
            # the previous position they were in is replaced with an empty space
            self.player_pos = (player_row, player_col - 1)
            # the new position of that player is saved at this row and colomn
        elif direction == "R" and player_col < len(self.grid[0]) - 1 and self.grid[player_row][player_col + 1] != "#":
            # if the player chooses right, and the players column is within bounds, and to the right of them is not a wall
            self.grid[player_row][player_col + 1] = "P"
            # the player moves one square to the right
            self.grid[player_row][player_col] = " "
            # the previous position they were in is replaced with an empty space
            self.player_pos = (player_row, player_col + 1)
            # the new position of that player is saved at this row and column
        elif direction == "U" and player_row > 0 and self.grid[player_row - 1][player_col] != "#":
            # if the player chooses up, and the players row is within bounds, and in that direction there is no wall
            self.grid[player_row - 1][player_col] = "P"
            # the player moves one square up
            self.grid[player_row][player_col] = " "
            # the previous position they were in is replaced with an empty space
            self.player_pos = (player_row - 1, player_col)
            # the new position of that player is saved at this row and column
        elif direction == "D" and player_row < len(self.grid) - 1 and self.grid[player_row + 1][player_col] != "#":
            # if the player chooses down, and the players row is within bounds, and in that direction there is no wall
            self.grid[player_row + 1][player_col] = "P"
            # the player moves one square down
            self.grid[player_row][player_col] = " "
            # the previous position they were in is replaced with an empty space
            self.player_pos = (player_row + 1, player_col)
            # the new position of that player is saved at this row and column
    def player_wins(self):
        # check if player is on the end square
        if (self.player_pos == self.exit_pos):
            # if the player is on the end square, the player wins
            return True
        # if the player is not on the end square, the player does not win
        return False
    def player_loses(self):
        # check if the player is in the guard range
        for guard in self.guards_list:
            player_row, player_col = self.player_pos
            if guard.enemy_in_range(player_row, player_col):
                return True
        return False
# creating a class called guard
class guard:
    def __init__(self, row, col, attack_range, movements):
        # initializing the row, column, attack range, and movements of the guard
        self.row = row
        self.col = col
        self.attack_range = attack_range
        self.movements = movements
    def get_location(self):
        # returns the row and the column of the guard
        return (self.row, self.col)
    def move(self,current_grid):
        # get the next movement command from the movements list
        next_move = self.movements[0]
        # update the guard's position based on the next movement command
        if next_move == "L" and self.col > 0 and current_grid[self.row][self.col - 1] != "#":
            # if the next move is "L" representing left, and the left of the guard is not a wall
            self.col -= 1
            # move the guard one square to the left
        # if the next move is "R" representing right, and to the right of them is not a wall
        elif next_move == "R" and self.col < len(current_grid[0]) - 1 and current_grid[self.row][self.col + 1] != "#":
            # the guard moves one square to the right
            self.col += 1
        # if the next move is "U" representing up, and above them is not a wall
        elif next_move == "U" and self.row > 0 and current_grid[self.row - 1][self.col] != "#":
            # the guard moves one square above them
            self.row -= 1
        # if the next move is "D" representing down, and above them is not a wall
        elif next_move == "D" and self.row < len(current_grid) - 1 and current_grid[self.row + 1][self.col] != "#":
            # the guard moves one square below them
            self.row += 1
        # move to the next movement command
        self.movements = self.movements[1:] + [next_move]
    def enemy_in_range(self,enemy_row,enemy_col):
        # if the distance between the guard and the player is within the attack range of the guard
        if abs(enemy_row - self.row) + abs(enemy_col - self.col) <= self.attack_range:
            # the player is within the range and should be eliminated
            return True
        # if the distance is greater than the attack range of the guard, the player should not be eliminated
        else:
            return False
