from random import sample
from selection import SelectNumber
from copy import deepcopy

def createLineCordinates(cell_size:int) -> list[list[tuple]]:
    """creates the x,y cordinates for each line in the grid"""
    points = []
    for y in range (1,9):
        #horizontal lines
        temp = []
        temp.append((0, y * cell_size))
        temp.append((810, y * cell_size))
        points.append(temp)
    for x in range (1,10):
        #vertical lines
        temp = []
        temp.append((x * cell_size, 0))
        temp.append((x * cell_size, 810))
        points.append(temp)
    return points

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def patterm(row_num:int,colum_num:int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + colum_num) % GRID_SIZE

def shuffle(samp:range) -> list:
    return sample(samp, len(samp))

def remove_numbers(grid:list[list]) -> None:
    """Randomly set the numbers to zero to create the puzzle"""
    number_of_cells = GRID_SIZE * GRID_SIZE
    empties = number_of_cells * 3 // 6 # 7 is ideal the higher the number the easier the puzzle
    for i in sample(range(number_of_cells),empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0


def createGrid(sub_grid:int) -> list[list]:
    """Creates a 9x9 sodoku grid of random numbers"""
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    columns = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[patterm(r,c)] for c in columns] for r in rows]



class Grid:
    def __init__(self,pygame,font):
        self.cell_size = 90
        self.num_x_offset = 30
        self.num_y_offset = 25
        self.line_cordinates = createLineCordinates(self.cell_size)
        self.grid = createGrid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.ocuupied_cells = self.pre_occupied_cells()
        self.game_font = font
        self.selection = SelectNumber(pygame,self.game_font)
        self.win = False

    def restart(self) -> None:
        """Restart the grid to play again"""
        self.grid = createGrid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.ocuupied_cells = self.pre_occupied_cells()
        self.win = False

    def check_grids(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True
    
    def is_pre_occupied_cell(self,x:int,y:int) -> bool:
        """it return the cell state if it is pre occupied or not"""
        for cell in self.ocuupied_cells:
            if x == cell[1] and y == cell[0]: # x = column , y = row
                return True
        return False

    def get_mouse_click(self,x:int,y:int) -> None:
        if x <= 810:
            grid_x = x // 90
            grid_y = y // 90 
            # print(f"Grid position: ({grid_x},{grid_y})")
            if not self.is_pre_occupied_cell(grid_x,grid_y):
                self.set_cell(grid_x,grid_y,self.selection.selected_number)
        self.selection.button_clicked(x,y)
        if self.check_grids():
            self.win = True

    def pre_occupied_cells(self) -> list[tuple]:
        """Return a list of pre occupied cells in the grid"""
        occupied_cell_cordinates = []
        for y in range (len(self.grid)):
            for x in range (len(self.grid[y])):
                if self.get_cell(x,y) != 0:
                    occupied_cell_cordinates.append((y,x)) # first the row then the column
        return occupied_cell_cordinates
         

    def get_cell(self,x:int,y:int) -> int:
        """Get a cell value at (x,y) position"""
        return self.grid[y][x]
    
    def set_cell(self,x:int,y:int,value:int) -> None:
        """Set a cell value at (x,y) position"""
        self.grid[y][x] = value

    def __drawLine(self,pg,surface) -> None:
        for index,point in enumerate(self.line_cordinates):
            if index == 2 or index == 5 or index == 10 or index == 13:
                pg.draw.line(surface,(255,200,0),point[0],point[1])
            else:
                pg.draw.line(surface,(0,50,0),point[0],point[1])
    
    def __drawNumbers(self,surface) -> None:
        """Draws the grid numbers on the surface"""
        for y in range (len(self.grid)):
            for x in range (len(self.grid[y])):
                if self.get_cell(x,y) != 0:
                    if (y,x) in self.ocuupied_cells:
                        text_surface = self.game_font.render(str(self.get_cell(x,y)),False,(0,200,255))
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x,y)),False,(0,255,0))
                    if self.get_cell(x,y) != self.__test_grid[y][x]:
                        text_surface = self.game_font.render(str(self.get_cell(x,y)),False,(255,0,0))
                    surface.blit(text_surface,(x * self.cell_size + self.num_x_offset, y * self.cell_size + self.num_y_offset))

    def draw_all(self,pg,surface) -> None:
        self.__drawLine(pg,surface)
        self.__drawNumbers(surface)
        self.selection.draw(pg,surface)

    def show(self):
        for cell in self.grid:
            print(cell)


if __name__ == "__main__":
    import pygame
    pygame.init()
    game_font = pygame.font.SysFont('Comic Sans MS', 40)
    grid = Grid(pygame,game_font)
    grid.show()