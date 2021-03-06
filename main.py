import pygame
import random
import math
pygame.init()

class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0

    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160,160,160),
        (192,192,192)
    ]

    FONT = pygame.font.SysFont('comicsans',20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100 #100 pixel padding left and right
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.set_list(lst)
        #Create pygame window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


class Checkbox:
    def __init__(self, surface, x, y, idnum, color=(230, 230, 230),
                 caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
                 font_size=22, font_color=(0, 0, 0),
                 text_offset=(28, 1), font='Ariel Black'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        # identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 +
                         self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)


def generate_starting_list(n, min_val, max_val):
    #n is the number of values in the list
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 ,5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 ,38))


    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 68))


    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 68))


    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending) :
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1,len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i-1
            lst[i]=current
            draw_list(draw_info,{i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def selection_sort(draw_info, ascending):
    lst = draw_info.lst

    for i in range(len(lst)):
        min_idx = i
        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j

        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
        yield True
    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(800,600, lst)


    sorting = False
    ascending = True
    # merge_sort(draw_info, ascending)
    # quickSort(draw_info)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60) #max frame rate the display can work in
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)


        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if x at top right corner clicked
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"

    pygame.quit()

if __name__ == "__main__":
    main()