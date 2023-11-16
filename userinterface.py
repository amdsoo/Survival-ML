
from declaration import *

pygame.font.init()
# basic font for user typed
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_small_font = pygame.font.SysFont('Comic Sans MS', 15)

button_width = tile_size*0.8
button_height =tile_size*0.8


class MouseHandler:
    def __init__(self):
        self.right_click = False
        self.start_pos = None
        self.end_pos = None

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.right_click = False
                self.end_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.right_click = True
                self.start_pos = event.pos

    def reset(self):
        self.right_click = False
        self.start_pos = None
        self.end_pos = None


class Button:
    def __init__(self, button_class, x, y):
        self.button_class = button_class
        self.color = LIGHTSHADE
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.state = "depressed"
        self.parent = "parent"

        # default image

        if self.button_class == "Predator":
            self.image = pygame.transform.scale(predator_img , (self.width, self.height))
            self.image_ns = pygame.transform.scale(predator_ns_img , (self.width, self.height))

        if self.button_class == "Prey":
            self.image = pygame.transform.scale(prey_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(prey_ns_img, (self.width, self.height))

        if self.button_class == "Plant":
            self.image = pygame.transform.scale(plant_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(plant_ns_img, (self.width, self.height))

        if self.button_class == "Delete":
            self.image = pygame.transform.scale(delete_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(delete_ns_img, (self.width, self.height))

        if self.button_class == "Simulation":
            self.image = pygame.transform.scale(simu_on_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(simu_off_img, (self.width, self.height))

        if self.button_class == "save":
            self.image = pygame.transform.scale(save_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(save_ns_img, (self.width, self.height))

        if self.button_class == "open":
            self.image = pygame.transform.scale(open_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(open_ns_img, (self.width, self.height))


    def draw(self, screen):
        # Call this method to draw the button on the screen if visible.
        if self.state == "depressed":
            self.color = LIGHTSHADE
            screen.blit(self.image_ns, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x , self.y))


    def click (self):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y) :
            print ("button clicked -> ", "Status before change", self.state)
            # special treatment for Simulation
            if self.button_class == "simulation":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            elif self.button_class == "delete":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            elif self.button_class == "save":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            elif self.button_class == "open":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            else:
                # if this is the creation button
                if self.state == "pressed":  # the button was pressed, so now we must be depressed it and hide all
                    print("this button becomes inactive")
                    self.state = "depressed"
                    '''for button in button_list:
                        button.state = "depressed"'''
                else:
                    print("this button becomes active")
                    self.state = "pressed"


def menu_reset (button_list):
    for button in button_list:
        button.state = "depressed"


def menu_selection_frombutton (button_list):
    object_class_pressed = ""
    for button in button_list:
        if button.state == "pressed":
            object_class_pressed = button.button_class
    return object_class_pressed


def menu_state_from_event (button_list):

    placement_type = ""
    for button in button_list:
        button.click()
        if button.state == "pressed":
            placement_type = button.button_class
    return placement_type


def menu_create (button_list):
    # create the buttons of the Interface
    button_position_x = 6 * tile_size + tile_size / 10
    button_position_y = tile_size / 10

    button_position_x = button_position_x + tile_size
    button_predator = Button("Predator", button_position_x, button_position_y)
    button_list.append(button_predator)

    button_position_x = button_position_x + tile_size
    button_prey = Button("Prey", button_position_x, button_position_y)
    button_list.append(button_prey)

    button_position_x = button_position_x + tile_size
    button_plant = Button("Plant", button_position_x, button_position_y)
    button_list.append(button_plant)


    return button_list
