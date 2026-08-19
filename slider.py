import pygame as pg

class Slider:
    def __init__(self, x, y, width, height, width_handle, height_handle, min_val, max_val, start_val, label="" ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.width_handle = width_handle
        self.height_handle = height_handle
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.label = label
        self.is_dragging = False

        self.font = pg.font.SysFont("Arial", 20)

    def draw(self,screen):
        pg.draw.rect(screen, (60,60,60), (self.x,self.y,self.width,self.height), border_radius = 3)

        procent = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.x + (self.width // 2) - (self.width_handle // 2)
        handle_y = self.y + int((1-procent) * self.height) - (self.height_handle // 2)
        pg.draw.rect(screen, (100, 100, 100), (handle_x, handle_y, self.width_handle, self.height_handle), border_radius=8)

        label = self.font.render(self.label, 1, (80, 80, 80))
        screen.blit(label, (self.x-(self.font.size(self.label)[0]//2)+self.width//2, self.y-self.font.size(self.label)[1]-self.height_handle//2))

        value_text = self.font.render(f'{self.value:.2f}', 1, (80, 80, 80))
        screen.blit(value_text, (self.x - (self.font.size(f'{self.value:.2f}')[0] // 2) + self.width//2,
                           self.y + self.font.size(self.label)[1] + self.height))

    def handle_event(self,event):
        mouse_pos = pg.mouse.get_pos()
        percent_current = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.x + (self.width // 2) - (self.width_handle // 2)
        handle_y = self.y + int((1-percent_current) * self.height) - (self.height_handle // 2)

        handle_rect = pg.Rect(handle_x, handle_y, self.width_handle, self.height_handle)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if handle_rect.collidepoint(mouse_pos):
                    self.is_dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False

        elif event.type == pg.MOUSEMOTION:
            if self.is_dragging:
                bounded_y = max(self.y, min(mouse_pos[1], self.y + self.height))
                relative_y = bounded_y - self.y
                percent_new = 1 - (relative_y / self.height)

                self.value = self.min_val + percent_new * (self.max_val - self.min_val)

    def get_value(self):
        return self.value
