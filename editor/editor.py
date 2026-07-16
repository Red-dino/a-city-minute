import pygame
import glob
from enum import Enum, auto
import json
from tkinter import filedialog

class BoxType(Enum):

    platform = auto()
    ceiling = auto()
    wall = auto()
    door = auto()

class Object:

    def __init__(self, tex_path, font, new = True):
        self.self_path = ""
        self.tex_path = tex_path
        self.name = Object.get_name(tex_path)
        self.font = font
        self.edited = new

        self.tex = pygame.image.load(self.tex_path).convert_alpha()
        self.size = self.tex.get_size()
        self.base_thumbnail = pygame.transform.scale(self.tex, (100, 100))
        self.update_thumbnail()

        self.platforms = []
        self.ceilings = []
        self.walls = []
        self.doors = []

        self.pos = (400, 400)
        self.scale = 0
        self.zoom(5)

    def has_been_saved(self):
        return self.self_path

    def update_data_path(self, new_path):
        self.self_path = new_path
        self.name = Object.get_name(new_path)
        self.update_thumbnail()

    def update_thumbnail(self):
        self.thumbnail = self.base_thumbnail.copy()
        self.thumbnail.blit(self.base_thumbnail, (0, 0))

        rendered_name = self.name
        if self.edited:
            rendered_name = "* " + self.name

        self.font.render_to(self.thumbnail, (4, 4), rendered_name, (255, 255, 255))

    def get_rect(self):
        return pygame.Rect(self.pos, self.scaled.get_size())

    def drag(self, new_pos, last_pos):
        x = new_pos[0] - last_pos[0] + self.pos[0]
        y = new_pos[1] - last_pos[1] + self.pos[1]
        self.pos = (x, y)

    def zoom(self, amount, rel=None):
        old_scale = self.scale
        self.scale += amount
        self.scale = min(max(self.scale, 1), 20)
        self.scaled = pygame.transform.scale(self.tex, (self.size[0] * self.scale, self.size[1] * self.scale))

        # (mx - x1) / w1 = (mx - x2) / w2
        # x2 = mx - (w2 * (mx - x1) / w1)
        if rel:
            x = rel[0] - (self.size[0] * self.scale * (rel[0] - self.pos[0]) / self.size[0] / old_scale)
            y = rel[1] - (self.size[1] * self.scale * (rel[1] - self.pos[1]) / self.size[1] / old_scale)
            self.pos = (x, y)

    def zoom_to(self, value):
        self.scale = value
        self.zoom(0)

    def add(self, rect, box_type):
        box_list = []
        if box_type == BoxType.platform:
            box_list = self.platforms
        elif box_type == BoxType.ceiling:
            box_list = self.ceilings
        elif box_type == BoxType.wall:
            box_list = self.walls
        elif box_type == BoxType.door:
            box_list = self.doors

        delete = False
        copied = []
        for plat in box_list:
            if plat.contains(rect):
                delete = True
            elif not rect.contains(plat):
                copied.append(plat)
        if not delete:
            copied.append(rect)

        if box_type == BoxType.platform:
            self.platforms = copied
        elif box_type == BoxType.ceiling:
            self.ceilings = copied
        elif box_type == BoxType.wall:
            self.walls = copied
        elif box_type == BoxType.door:
            self.doors = copied

        if not self.edited:
            self.edited = True
            self.update_thumbnail()

    def boxes(self):
        for box in self.platforms:
            yield box, BoxType.platform
        for box in self.ceilings:
            yield box, BoxType.ceiling
        for box in self.walls:
            yield box, BoxType.wall
        for box in self.doors:
            yield box, BoxType.door

    def get_name(path):
        s = ""
        past_period = False
        for c in path[::-1]:
            if past_period:
                if c == "\\" or c == "/":
                    return s
                s = c + s 
            elif c == ".":
                past_period = True
        print("weird path: ", path, "parsed: ", s)
        return s

    def save(self, data_path):
        self.update_data_path(data_path)
        d = {
            'name' : self.name,
            'path' : self.tex_path,
            'platforms' : [tuple(i for i in x) for x in self.platforms],
            'ceilings' : [tuple(i for i in x) for x in self.ceilings],
            'walls' : [tuple(i for i in x) for x in self.walls],
            'doors' : [tuple(i for i in x) for x in self.doors],
        }
        j = json.dumps(d)
        with open(data_path, 'w') as f:
            f.write(j)

        self.edited = False
        self.update_thumbnail()

    def load(data_path, font):
        data = dict()
        with open(data_path, 'r') as f:
            data = json.load(f)

        self = Object(data['path'], font, new=False)

        self.update_data_path(data_path)
        self.platforms = [pygame.Rect(x) for x in data['platforms']]
        self.ceilings = [pygame.Rect(x) for x in data['ceilings']]
        self.walls = [pygame.Rect(x) for x in data['walls']]
        self.doors = [pygame.Rect(x) for x in data['doors']]

        return self

    def new(image_path, font):
        return Object(image_path, font)

class Editor:

    box_color_map = {
        BoxType.platform: (50, 50, 150),
        BoxType.ceiling: (150, 50, 50),
        BoxType.wall: (50, 150, 50),
        BoxType.door: (150, 150, 50),
    }

    def __init__(self):
        self.objects = []
        self.current_object = None

        self.dragging = False
        self.last_pos = (0, 0)

        self.drawing = False
        self.fixed_point = (0, 0)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.box_tool_type = BoxType.door

        self.tools = [BoxType.platform, BoxType.ceiling, BoxType.wall, BoxType.door]
        self.tool_names = ["Platform", "Ceiling", "Wall", "Door", "Save"]
        self.hidden_boxes = set()

        self.guy_fresh = True
        self.guy_dragging = False
        self.guy_outline_clicked = False

        self.scroll_y = 0

    def resize(self, new_size):
        self.new_object_area = pygame.Rect(0, 0, 120, 120)
        self.palette_area = pygame.Rect(0, 120, 120, new_size[1] + 120)
        self.tool_area = pygame.Rect(120, new_size[1] - 120, new_size[0] - 120, 120)
        self.object_area = pygame.Rect(120, 0, new_size[0] - 120, new_size[1] - 120)

        self.box_surf = pygame.Surface(self.object_area.size, pygame.SRCALPHA)
        self.box_surf.set_alpha(150)

        self.save_button = pygame.Rect(new_size[0] - 110, new_size[1] - 110, 100, 45)
        self.save_as_button = pygame.Rect(new_size[0] - 110, new_size[1] - 55, 100, 45)

        self.guy_outline_button = pygame.Rect(130, new_size[1] - 280, 30, 150)

        self.viewport_height = new_size[1] - 120

    def load_assets(self):
        self.font = pygame.freetype.SysFont("Consolas", 16)
        for _ in range(1):
            for path in glob.glob("saves/*.data"):
                object = Object.load(path, self.font)
                self.objects.append(object)
        self.scroll_height = 110 * len(self.objects) + 10
        self.new_object_tex = pygame.image.load("tool_assets/plus.png").convert_alpha()
        self.guy_object = Object("tool_assets/guy.png", self.font)
        self.guy_object.pos = (self.object_area.x + 10, self.object_area.height - 160)
        self.guy_outline_tex = pygame.image.load("tool_assets/guy_outline.png").convert_alpha()

    def snap_pos(self, pos, obj):
        x = (pos[0] - obj.pos[0]) // obj.scale
        y = (pos[1] - obj.pos[1]) // obj.scale
        return x, y

    def get_drawn_rect(self, rect, obj):
        x = rect.x * obj.scale + obj.pos[0] - self.object_area.x
        y = rect.y * obj.scale + obj.pos[1] - self.object_area.y
        w = rect.w * obj.scale
        h = rect.h * obj.scale
        return (x, y, w, h)

    def save(self):
        if not self.current_object:
            return

        if self.current_object.has_been_saved():
            f = filedialog.asksaveasfilename(defaultextension=".data", initialdir="saves", initialfile=self.current_object.name, filetypes=[("Data file", "*.data")])
        else:
            f = filedialog.asksaveasfilename(defaultextension=".data", initialdir="saves", filetypes=[("Data file", "*.data")])

        if not f:
            return

        self.current_object.save(f)

    def load(self):
        f = filedialog.askopenfilename(initialdir="assets", filetypes=[("Image file", "*.png;*.jpg;*.jpeg")])

        if not f:
            return

        obj = Object.new(f, self.font)
        self.objects.insert(0, obj)
        self.current_object = obj
        self.scroll_height = 110 * len(self.objects) + 10

    def run(self):
        pygame.init()
        pygame.display.set_caption("A City Minute - Editor")
        screen_size = (1200, 900)
        self.resize(screen_size)
        screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        factor = 1200 // 120

        running = True
        clock = pygame.time.Clock()

        self.load_assets()

        while running:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    screen_size = event.size
                    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    self.resize(screen_size)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.new_object_area.collidepoint(mouse_pos):
                            self.load()
                            self.guy_object.zoom_to(5)
                            self.guy_object.pos = (self.object_area.x + 10, self.object_area.height - 160)
                            self.guy_fresh = True
                        elif self.palette_area.collidepoint(mouse_pos):
                            click_y = mouse_pos[1] - self.palette_area.y - self.scroll_y
                            click_i = click_y // 110
                            if click_i < len(self.objects):
                                self.current_object = self.objects[click_i]
                                self.current_object.zoom_to(5)
                                self.guy_object.zoom_to(5)
                                self.guy_object.pos = (self.object_area.x + 10, self.object_area.height - 160)   
                                self.guy_fresh = True
                        elif self.save_button.collidepoint(mouse_pos):
                            self.save()
                        elif self.tool_area.collidepoint(mouse_pos):
                            click_x = mouse_pos[0] - self.tool_area.x
                            click_i = click_x // 110
                            if click_i < len(self.tools):
                                self.box_tool_type = self.tools[click_i]
                        elif self.guy_object.get_rect().collidepoint(mouse_pos):
                            self.guy_fresh = False
                            self.guy_dragging = True
                            self.last_pos = mouse_pos
                        elif self.guy_outline_button.collidepoint(mouse_pos):
                            self.guy_outline_clicked = True
                        elif self.current_object and self.object_area.collidepoint(mouse_pos):
                            self.dragging = True
                            self.last_pos = mouse_pos
                    elif event.button == 3:
                        if self.object_area.collidepoint(mouse_pos) and self.current_object and not self.drawing:
                            self.drawing = True
                            self.fixed_point = self.snap_pos(mouse_pos, self.current_object)
                            self.rect.topleft = self.fixed_point
                            self.rect.size = (1, 1)
                        elif self.tool_area.collidepoint(mouse_pos):
                            click_x = mouse_pos[0] - self.tool_area.x
                            click_i = click_x // 110
                            if click_i < len(self.tools):
                                tool = self.tools[click_i]
                                if tool in self.hidden_boxes:
                                    self.hidden_boxes.remove(tool)
                                else:
                                    self.hidden_boxes.add(tool)
                    elif event.button == 5:
                        if self.palette_area.collidepoint(mouse_pos):
                            self.scroll_y -= 2
                            self.scroll_y = max(self.scroll_y, self.viewport_height - self.scroll_height)
                            if self.scroll_height <= self.viewport_height:
                                self.scroll_y = 0
                        elif self.current_object and self.object_area.collidepoint(mouse_pos):
                            self.current_object.zoom(0.1, mouse_pos)
                            if self.guy_fresh:
                                self.guy_object.zoom(0.1, self.guy_object.get_rect().bottomleft)
                            else:
                                self.guy_object.zoom(0.1, mouse_pos)
                    elif event.button == 4:
                        if self.palette_area.collidepoint(mouse_pos):
                            self.scroll_y += 2
                            self.scroll_y = min(self.scroll_y, 0)
                            if self.scroll_height <= self.viewport_height:
                                self.scroll_y = 0
                        elif self.current_object and self.object_area.collidepoint(mouse_pos):
                            self.current_object.zoom(-0.1, mouse_pos)
                            if self.guy_fresh:
                                self.guy_object.zoom(-0.1, self.guy_object.get_rect().bottomleft)
                            else:
                                self.guy_object.zoom(-0.1, mouse_pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.guy_outline_clicked and self.guy_outline_button.collidepoint(mouse_pos):
                            zoom = self.current_object.scale if self.current_object else 5
                            self.guy_object.zoom_to(zoom)
                            self.guy_object.pos = (self.object_area.x + 10, self.object_area.height - 10 - self.guy_object.get_rect().height)   
                            self.guy_fresh = True
                        elif self.guy_dragging:
                            self.guy_object.drag(mouse_pos, self.last_pos)
                            self.guy_dragging = False
                        elif self.dragging and self.current_object:
                            self.current_object.drag(mouse_pos, self.last_pos)
                            self.dragging = False
                        self.guy_outline_clicked = False
                    elif event.button == 3:
                        if self.drawing and self.object_area.collidepoint(mouse_pos) and self.current_object:
                            self.drawing = False
                            snap = self.snap_pos(mouse_pos, self.current_object)
                            self.rect.width = abs(snap[0] - self.fixed_point[0]) + 1
                            self.rect.x = min(self.fixed_point[0], snap[0])
                            self.rect.height = abs(snap[1] - self.fixed_point[1]) + 1
                            self.rect.y = min(self.fixed_point[1], snap[1])
                            self.current_object.add(self.rect, self.box_tool_type)
                            self.rect = pygame.Rect(0, 0, 1, 1)
                elif event.type == pygame.MOUSEMOTION:
                    if self.guy_dragging:
                        self.guy_object.drag(mouse_pos, self.last_pos)
                        self.last_pos = mouse_pos
                    elif self.dragging and self.current_object:
                        self.current_object.drag(mouse_pos, self.last_pos)
                        self.last_pos = mouse_pos
                    elif self.drawing and self.current_object:
                        snap = self.snap_pos(mouse_pos, self.current_object)
                        self.rect.width = abs(snap[0] - self.fixed_point[0]) + 1
                        self.rect.x = min(self.fixed_point[0], snap[0])
                        self.rect.height = abs(snap[1] - self.fixed_point[1]) + 1
                        self.rect.y = min(self.fixed_point[1], snap[1])

            screen.fill((255, 255, 255))

            # Object area
            if self.current_object:
                screen.blit(self.current_object.scaled, self.current_object.pos)

                self.box_surf.fill((0, 0, 0, 0))
                if self.drawing:
                    pygame.draw.rect(self.box_surf, Editor.box_color_map[self.box_tool_type], self.get_drawn_rect(self.rect, self.current_object)) # , width=1)
                for box, box_type in self.current_object.boxes():
                    if box_type not in self.hidden_boxes:
                        pygame.draw.rect(self.box_surf, Editor.box_color_map[box_type], self.get_drawn_rect(box, self.current_object)) # , width=1)
                screen.blit(self.box_surf, self.object_area.topleft)

                self.font.render_to(screen, (self.object_area.x + 4, self.object_area.y + 4), self.current_object.name, (0, 0, 0))

            screen.blit(self.guy_object.scaled, self.guy_object.pos)

            if not self.guy_fresh:
                screen.blit(self.guy_outline_tex, self.guy_outline_button)

            # Palette area
            pygame.draw.rect(screen, (200, 200, 200), self.palette_area)

            y = self.palette_area.y + self.scroll_y
            for object in self.objects:
                screen.blit(object.thumbnail, (10, y))
                y += 110

            if self.scroll_height > self.viewport_height:
                percent_shown = self.viewport_height / self.scroll_height
                scroll_bar_height = self.viewport_height * percent_shown
                pygame.draw.rect(screen, (100, 100, 100), (self.palette_area.width - 3, self.palette_area.y - (self.scroll_y * percent_shown), 3, scroll_bar_height))

            # New object
            pygame.draw.rect(screen, (200, 200, 200), self.new_object_area)
            screen.blit(self.new_object_tex, (self.new_object_area.x + 10, self.new_object_area.y + 10))

            # Tool area
            pygame.draw.rect(screen, (150, 150, 150), self.tool_area)

            x = self.tool_area.x + 10
            y = self.tool_area.y + 10
            for i, tool in enumerate(self.tools):
                pygame.draw.rect(screen, Editor.box_color_map[tool], (x, y, 100, 100)) # , width=1)
                if tool == self.box_tool_type:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 100), width=2)

                color = (255, 255, 255) if tool not in self.hidden_boxes else (0, 0, 0)
                self.font.render_to(screen, (x + 4, y + 4), self.tool_names[i], color)
                x += 110

            pygame.draw.rect(screen, (200, 200, 200), self.save_button) # , width=1
            self.font.render_to(screen, (self.save_button.x + 4, self.save_button.y + 4), "Save", (255, 255, 255))

            pygame.draw.rect(screen, (200, 200, 200), self.save_as_button) # , width=1
            self.font.render_to(screen, (self.save_as_button.x + 4, self.save_as_button.y + 4), "Save As", (255, 255, 255))

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    Editor().run()
