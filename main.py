import pygame, random, sys

pygame.init()


class DInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    # (192, 178, 231)
    BACKGROUND_COLOR = (241, 237, 222)
    GRADIENTS = [
        (146, 126, 233),
        (102, 69, 101),
        (182, 165, 157),
    ]
    SIDE_PAD = 100
    TOP_PAD = 150
    FIXED_FOR_MIN = 10
    lst = []
    min_val = max_val = block_width = block_height = start_x = 0

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) - 5
        self.max_val = max(lst) + 5
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2


class Button:
    gui_font = pygame.font.Font(None, 30)

    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.screen = pygame.display.get_surface()
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.original_x_pos = pos[0]
        self.width = width
        self.height = height

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text_surf = self.gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click(pygame.mouse.get_pos())

    def check_click(self, mouse):
        if self.top_rect.collidepoint(mouse):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                return True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    return True
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'
        return False


class DropDown:
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))
        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break
        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1


def insertion_sort(draw_info):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current
            if not ascending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst


def generate_lst(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def draw(info, lists, buttons):
    info.window.fill(info.BACKGROUND_COLOR)
    draw_list(info)
    for i in lists:
        i.draw(pygame.display.get_surface())
    for i in buttons:
        i.draw()
    pygame.display.update()


def bubble_sort(draw_info):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if num1 > num2:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True


def merge_sort(draw_info):
    for idx, i in enumerate(merge_sort_yield(draw_info.lst)):
        draw_info.set_list(i)
        yield True
        draw_list(draw_info, {}, True)


def merge_sort_yield(arr):
    def merge_sort_rec(start, end):
        if end - start > 1:
            middle = (start + end) // 2
            yield from merge_sort_rec(start, middle)
            yield from merge_sort_rec(middle, end)
            left = arr[start:middle]
            right = arr[middle:end]
            a = 0
            b = 0
            c = start
            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    arr[c] = left[a]
                    a += 1
                else:
                    arr[c] = right[b]
                    b += 1
                c += 1

            while a < len(left):
                arr[c] = left[a]
                a += 1
                c += 1

            while b < len(right):
                arr[c] = right[b]
                b += 1
                c += 1
            yield arr

    yield from merge_sort_rec(0, len(arr))


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                      draw_info.width + 10 - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
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


def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 10
    max_val = 70
    lst = generate_lst(n, min_val, max_val)
    draw_info = DInformation(800, 800, lst)
    btn_start = Button('Start', 80, 30, (680, 32), 5)
    btn_stop = Button('Stop', 80, 30, (680, 82), 5)
    btn_generate = Button('Generate', 100, 30, (555, 52), 5)
    select_mode = DropDown(
        [(100, 80, 255), (100, 200, 255)],
        [(255, 100, 100), (255, 150, 150)],
        50, 50, 150, 30,
        pygame.font.SysFont(None, 30),
        "Select Mode", ["Bubble Sort", "Insertion Sort", "Merge Sort"])
    num_of_blocks = DropDown(
        [(100, 80, 255), (100, 200, 255)],
        [(255, 100, 100), (255, 150, 150)],
        240, 50, 150, 30,
        pygame.font.SysFont(None, 30),
        "Num of Blocks", ["10", "20", "30", "40","50"])
    speed = DropDown(
        [(100, 80, 255), (100, 200, 255)],
        [(255, 100, 100), (255, 150, 150)],
        430, 50, 100, 30,
        pygame.font.SysFont(None, 30),
        "Speed", ["Slow", "Medium", "Fast"])
    lists = [select_mode, speed, num_of_blocks]
    buttons = [btn_start, btn_stop, btn_generate]
    sorting_algorithm = None
    sorting_algorithm_generator = None
    sorting = False
    frm_speed = 20
    while run:
        clock.tick(frm_speed)
        event_list = pygame.event.get()
        for event in event_list:
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.check_click(mouse):
                    if sorting_algorithm != None and frm_speed != 20:
                        sorting_algorithm_generator = sorting_algorithm(draw_info)
                        sorting = True
                elif btn_stop.check_click(mouse):
                    sorting = False
                elif btn_generate.check_click(mouse):
                    lst = generate_lst(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
        select_sort = select_mode.update(event_list)
        select_speed = speed.update(event_list)
        select_num_blocks = num_of_blocks.update(event_list)
        if select_sort >= 0:
            if select_sort == 0:
                sorting_algorithm = bubble_sort
                sorting = False
            elif select_sort == 1:
                sorting_algorithm = insertion_sort
                sorting = False
            elif select_sort == 2:
                sorting_algorithm = merge_sort
                sorting = False
            select_mode.main = select_mode.options[select_sort]
        if select_speed >= 0:
            if select_speed == 0:
                sorting = False
                frm_speed = 15
            elif select_speed == 1:
                sorting = False
                frm_speed = 40
            elif select_speed == 2:
                sorting = False
                frm_speed = 100
            speed.main = speed.options[select_speed]
        if select_num_blocks >= 0:
            if select_num_blocks == 0:
                n = 10
                draw_info.set_list(generate_lst(n, min_val, max_val))
            elif select_num_blocks == 1:
                n = 20
                draw_info.set_list(generate_lst(n, min_val, max_val))
            elif select_num_blocks == 2:
                n = 30
                draw_info.set_list(generate_lst(n, min_val, max_val))
            elif select_num_blocks == 3:
                n = 40
                draw_info.set_list(generate_lst(n, min_val, max_val))
            elif select_num_blocks == 4:
                n = 50
                draw_info.set_list(generate_lst(n, min_val, max_val))
            num_of_blocks.main = num_of_blocks.options[select_num_blocks]
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, lists, buttons)
    pygame.quit()


if __name__ == "__main__":
    main()