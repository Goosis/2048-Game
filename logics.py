import random

# Function to print the grid in a nice format
def pretty_print(mas):
    print('-'*10)  # Just a separator for readability
    for row in mas:
        print(*row)  # Prints each row on a new line
    print('-'*10)

# Function to get the number (1-16) from row and column indices
def get_number_from_index(i, j):
    return i * 4 + j + 1  # Formula to convert 2D index to 1D number

# Function to get the row and column indices from a number (1-16)
def get_index_from_number(num):
    num -= 1  # Adjust to 0-based indexing
    x, y = num // 4, num % 4  # Divide for row, modulus for column
    return x, y

# Function to randomly insert 2 or 4 into the grid
def insert_2_or_4(mas, x, y):
    if random.random() <= 0.75:  # 75% chance for a 2
        mas[x][y] = 2
    else:  # 25% chance for a 4
        mas[x][y] = 4
    return mas

# Function to find all empty cells in the grid
def get_empty_list(mas):
    empty = []  # List to store empty positions
    for i in range(4):  # Loop through rows
        for j in range(4):  # Loop through columns
            if mas[i][j] == 0:  # If the cell is empty
                num = get_number_from_index(i, j)  # Get its 1D number
                empty.append(num)  # Add to the list
    return empty

# Function to check if there are any zeros in the grid
def is_zero_in_mas(mas):
    for row in mas:
        if 0 in row:  # If any row has a zero
            return True
    return False  # No zeros found

# Function to move all cells left and merge them
def move_left(mas):
    delta = 0  # Score gained in this move
    for row in mas:
        while 0 in row:  # Remove all zeros
            row.remove(0)
        while len(row) != 4:  # Add zeros to the right
            row.append(0)
    for i in range(4):  # Merge cells
        for j in range(3):
            if mas[i][j] == mas[i][j+1] and mas[i][j] != 0:  # If two cells are the same
                mas[i][j] *= 2  # Double the value
                delta += mas[i][j]  # Add to score
                mas[i].pop(j+1)  # Remove the merged cell
                mas[i].append(0)  # Add a zero at the end
    return mas, delta

# Function to move all cells right and merge them
def move_right(mas):
    delta = 0  # Score gained in this move
    for row in mas:
        while 0 in row:  # Remove all zeros
            row.remove(0)
        while len(row) != 4:  # Add zeros to the left
            row.insert(0, 0)
    for i in range(4):  # Merge cells
        for j in range(3, 0, -1):  # Start from the right
            if mas[i][j] == mas[i][j-1] and mas[i][j] != 0:  # If two cells are the same
                mas[i][j] *= 2  # Double the value
                delta += mas[i][j]  # Add to score
                mas[i].pop(j-1)  # Remove the merged cell
                mas[i].insert(0, 0)  # Add a zero at the start
    return mas, delta

# Function to move all cells up and merge them
def move_up(mas):
    delta = 0  # Score gained in this move
    for j in range(4):  # Loop through columns
        column = []  # Temporary list to store non-zero values
        for i in range(4):  # Loop through rows
            if mas[i][j] != 0:  # If the cell is not empty
                column.append(mas[i][j])
        while len(column) != 4:  # Add zeros at the bottom
            column.append(0)
        for i in range(3):  # Merge cells
            if column[i] == column[i+1] and column[i] != 0:  # If two cells are the same
                column[i] *= 2  # Double the value
                delta += column[i]  # Add to score
                column.pop(i+1)  # Remove the merged cell
                column.append(0)  # Add a zero at the end
        for i in range(4):  # Write back to the grid
            mas[i][j] = column[i]
    return mas, delta

# Function to move all cells down and merge them
def move_down(mas):
    delta = 0  # Score gained in this move
    for j in range(4):  # Loop through columns
        column = []  # Temporary list to store non-zero values
        for i in range(4):  # Loop through rows
            if mas[i][j] != 0:  # If the cell is not empty
                column.append(mas[i][j])
        while len(column) != 4:  # Add zeros at the top
            column.insert(0, 0)
        for i in range(3, 0, -1):  # Merge cells from bottom to top
            if column[i] == column[i-1] and column[i] != 0:  # If two cells are the same
                column[i] *= 2  # Double the value
                delta += column[i]  # Add to score
                column.pop(i-1)  # Remove the merged cell
                column.insert(0, 0)  # Add a zero at the start
        for i in range(4):  # Write back to the grid
            mas[i][j] = column[i]
    return mas, delta

# Function to check if any moves are possible
def can_move(mas):
    for i in range(3):  # Loop through rows except the last one
        for j in range(3):  # Loop through columns except the last one
            if mas[i][j] == mas[i][j+1] or mas[i][j] == mas[i+1][j]:  # Check horizontal or vertical neighbors
                return True  # There is at least one possible move
    return False  # No moves left
