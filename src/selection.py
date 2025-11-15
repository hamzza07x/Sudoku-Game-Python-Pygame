class SelectNumber:
    def __init__(self, pygame,font):
        self.pygame = pygame
        self.bt_width = 90
        self.btn_height = 90
        self.my_font = font
        self.selected_number = 0
        self.color_select = (0,255,0) 
        self.color_normal = (200,200,200)
        self.btn_positions = [
            (950,50),
            (1050,50),
            (950,150),
            (1050,150),
            (950,250),
            (1050,250),
            (950,350),
            (1050,350),
            (950,450),
        ]
    def draw(self,pygame,surface):
        for index,position in enumerate(self.btn_positions):
            pygame.draw.rect(surface,self.color_normal,[position[0],position[1],self.bt_width,self.btn_height], width=3,border_radius=10)
            if self.button_hover(position):
                pygame.draw.rect(surface,self.color_select,[position[0],position[1],self.bt_width,self.btn_height], width=3,border_radius=10)
                text_surface = self.my_font.render(str(index+1),False,(0,255,0))
            else:
                text_surface = self.my_font.render(str(index+1),False,(200,200,200))
            if self.selected_number > 0:
                if self.selected_number - 1 == index:
                    pygame.draw.rect(surface,self.color_select,[position[0],position[1],self.bt_width,self.btn_height], width=5,border_radius=10)
                    text_surface = self.my_font.render(str(index+1),False,self.color_select)
            surface.blit(text_surface,(position[0] + 26, position[1]))

    def button_clicked(self,mouse_x:int,mouse_y:int) ->None:
        for index,positions in enumerate(self.btn_positions):
            if self.on_button(mouse_x,mouse_y,positions):
                self.selected_number = index + 1

    def on_button(self,mouse_x:int,mouse_y:int,position:tuple) -> bool:
        return position[0] < mouse_x < position[0] + self.bt_width and position[1] < mouse_y < position[1] + self.btn_height
    
    def button_hover(self,position:tuple) -> bool|None:
        mouse_position = self.pygame.mouse.get_pos()
        if self.on_button(mouse_position[0],mouse_position[1],position):
            return True