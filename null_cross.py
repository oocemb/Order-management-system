from enum import Enum
import pygame


CELL_SIZE = 40

class Cell(Enum):
    VOID = 0
    CROSS = 1
    NULL = 0

class Player:
    """
    Класс игрока
    """
    def __init__(self, name, storona : Cell):
        self.name = name
        self.storona = storona

class GameRound:
    """
    Менеджер игры, запускающий все процессы
    """
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1,player2]
        self.field = GameField()
    def handle_click(self):
        pass

class GameField:
    def __init__(self) -> None:
        self.height = 3
        self.width = 3
        self.cells = ([Cell.VOID]*self.width for i in range(self.height))

class GameFieldView:
    def __init__(self,field) -> None:
        #Viget igrovogo polia, otobj pole na ekrane i mesto click , картинки значков клеток
        #отобразить первичное состояние
        self.field = field
        self.height = field.hiegth * CELL_SIZE
        self.width = field.width * CELL_SIZE
        pass
    def draw(self):
        pass
    def check_coords_correct(self,x,y):
        pass
    def get_coords(self,x,y):
        return(0,0)

class GameWindow:
    def __init__(self):
        self.field_widged = GameFieldView(field1)
        player1, player2 = Player("Петя", Cell.CROSS,), Player("Ваня", Cell.NULL)
        self.game_manager = GameRound(player1,player2)
        pygame.init()
        self.SIZE = (800,600) # window
        self.TITLE = "Крестики нолики"
        screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_captoin(self.TITLE)

        

    def main_loop(self):
        finished = False
        clock = pygame.time.Clock() # timer игра не экш, можно убрать
        refresh_rate = 60
        while not finished:
            for event in pygame.events_get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.x, event.y
                    if self.field_widged.check_coords_correct(x, y):
                        i, j = self.field_widged.get_coords(x, y)
                        self.game_manager.handle_click(i,j)
            pygame.display.flip()
            clock.tick(refresh_rate)

def main():
    window = GameWindow()
    window.main_loop()
    print("game over!")


if __name__ == "__main__":
    main()
