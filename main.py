# A City Minute
from enum import Enum, auto
import pygame
import pygame.freetype
import asyncio

class BuildingType(Enum):
    # Building
    brick = auto()
    awning = auto()
    residential_2_floor = auto()
    office_4_floor = auto()
    office_3_floor = auto()
    office_2_floor = auto()
    residential_stairs = auto()
    residential_stairs_2 = auto()
    residential_stairs_alt = auto()
    boutique = auto()
    boutique_alt = auto()
    hospital = auto()

    # Ground
    road = auto()
    park = auto()
    waterfront = auto()

    # Interiors
    vivo_interior = auto()
    vivo_floor_1 = auto()
    office_4_floor_interior = auto()
    residential_stairs_interior = auto()
    residential_stairs_interior_apt = auto()
    residential_stairs_interior_apt_2 = auto()
    sewer = auto()
    sewer_winged = auto()
    sewer_light_winged = auto()
    boutique_interior = auto()
    boutique_interior_alt = auto()
    hospital_room_start = auto()
    hospital_interior = auto()
    hospital_room = auto()

    # Structures
    watertower = auto()
    streetsign = auto()
    blocker = auto()
    window_washer = auto()
    # lamppost = auto()
    dumpster = auto()
    bench = auto()
    statue = auto()
    statue_platform = auto()
    sewer_cap = auto()
    # eyes = auto()
    # crane_shadow = auto()
    tree = auto()

    # People
    shopkeep = auto()
    mentor = auto()
    client = auto()

class BuildingTextures:
    __type_to_texture_path = {
        BuildingType.brick : "brick_building_1.png",
        BuildingType.awning : "awning1.png",
        BuildingType.residential_2_floor: "residential1.png",
        BuildingType.residential_stairs: "residential_stairs.png",
        BuildingType.residential_stairs_2: "residential_stairs_2.png",
        BuildingType.residential_stairs_alt: "residential_stairs_alt.png",
        BuildingType.residential_stairs_interior: "residential_stairs_interior.png",
        BuildingType.residential_stairs_interior_apt: "residential_stairs_interior_apt.png",
        BuildingType.residential_stairs_interior_apt_2: "residential_stairs_interior_apt_2.png",
        BuildingType.road : "road1.png",
        BuildingType.park : "park.png",
        BuildingType.waterfront : "waterfront.png",
        BuildingType.watertower: "watertower.png",
        BuildingType.office_4_floor: "office1.png",
        BuildingType.office_3_floor: "office3.png",
        BuildingType.office_2_floor: "office2.png",
        BuildingType.streetsign: "streetsign.png",
        BuildingType.blocker: "blocker.png",
        BuildingType.sewer_cap: "sewer_cap.png",
        BuildingType.sewer: "sewer_dark.png",
        BuildingType.sewer_winged: "sewer_dark_winged.png",
        BuildingType.sewer_light_winged: "sewer_light_winged.png",
        BuildingType.vivo_interior: "residential1_interior.png",
        BuildingType.vivo_floor_1: "vivo_floor1.png",
        BuildingType.boutique: "store.png",
        BuildingType.boutique_alt: "store_alt.png",
        BuildingType.boutique_interior: "store_interior.png",
        BuildingType.boutique_interior_alt: "store_interior_alt.png",
        BuildingType.hospital_room_start: "hospital_room_start.png",
        BuildingType.office_4_floor_interior: "office_interior.png",
        BuildingType.hospital: "hospital.png",
        BuildingType.bench: "bench.png",
        BuildingType.statue: "statue.png",
        BuildingType.statue_platform: "statue_platform.png",
        BuildingType.shopkeep: "shopkeep.png",
        BuildingType.mentor: "sitting.png",
        BuildingType.client: "client.png",
        BuildingType.hospital_interior: "hospital_interior.png",
        BuildingType.hospital_room: "hospital_room.png",
        BuildingType.tree: "tree.png",
        BuildingType.dumpster: "dumpster.png",
        BuildingType.window_washer: "window_washer.png",
    }

    __textures = {
    }

    def load(building_type):
        img = pygame.image.load("assets/" + BuildingTextures.__type_to_texture_path[building_type]).convert_alpha()
        BuildingTextures.__textures[building_type] = pygame.transform.scale(img, (img.get_width() * 10, img.get_height() * 10))

    def get(building_type):
        if building_type not in BuildingTextures.__textures:
            BuildingTextures.load(building_type)
        return BuildingTextures.__textures[building_type]

class Building:
    def __init__(self, building_type):
        self.building_type = building_type
        self.platforms = []
        self.ceilings = []
        self.walls = []
        # alley
        self.doors = []
        # id -> (rect, lambda game_phase: log message)
        self.interactions = {}
        self.visual_box = pygame.Rect((0, 0), (0, 0))
        self.silhouette = True

    def move(self, d_x, d_y):
        self.visual_box.move_ip(d_x, d_y)
        for p in self.platforms:
            p.move_ip(d_x, d_y)
        for c in self.ceilings:
            c.move_ip(d_x, d_y)
        for d in self.doors:
            d.box.move_ip(d_x, d_y)
        for d in self.interactions.values():
            d[0].move_ip(d_x, d_y)
        return self

    def move_0(self, d_x):
        return self.move(d_x, -self.visual_box.height)

    def change_interaction(self, id, log_lambda):
        rect, _ = self.interactions[id]
        self.interactions[id] = (rect, log_lambda)
        return self

    def animation_transition(self):
        pass

    def visual_loc(self, rel):
        x, y = rel
        return self.visual_box.x * 10 + x, self.visual_box.y * 10 + y

    def visual_size(self):
        return self.visual_box.w * 10, self.visual_box.h * 10

    def update_size(self, w, h):
        self.visual_box.size = (w, h)

    def get_building_by_type(building_type):
        if building_type == BuildingType.brick:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 0, 57, 5),
            ])
            b.update_size(57, 89)
            return b
        elif building_type == BuildingType.road:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 0, 90, 20),
            ])
            b.update_size(90, 20)
            b.silhouette = False
            return b
        elif building_type == BuildingType.park:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 5, 90, 20),
            ])
            b.update_size(90, 25)
            b.silhouette = False
            return b
        elif building_type == BuildingType.waterfront:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 0, 90, 20),
            ])
            b.update_size(90, 20)
            b.silhouette = False
            return b
        elif building_type == BuildingType.awning:
            b = Building(building_type)
            b.platforms.extend([
                # Awning
                pygame.Rect(13, 15, 20, 3),
                # Roof
                pygame.Rect(0, 0, 40, 3),
            ])
            b.update_size(40, 33)
            return b
        elif building_type == BuildingType.residential_2_floor:
            b = Building(building_type)
            b.platforms.extend([
                # Awning
                pygame.Rect(8, 55, 24, 3),
                # lower a/c
                pygame.Rect(28, 40, 6, 4),
                # upper a/c
                pygame.Rect(28, 20, 6, 4),
                # lower balcony
                pygame.Rect(2, 37, 18, 3),
                # upper balcony
                pygame.Rect(2, 17, 18, 3),

                # Roof
                pygame.Rect(0, 0, 40, 3),
            ])
            b.doors.extend([
                Alley(pygame.Rect(17, 59, 6, 12), StreetType.vivo, None)
            ])
            b.update_size(40, 70)
            return b
        elif building_type == BuildingType.residential_stairs or building_type == BuildingType.residential_stairs_2:
            b = Building(building_type)
            b.platforms.extend([
                # Planter
                pygame.Rect(0, 72, 41, 8),
                # Plant
                pygame.Rect(35, 65, 4, 7),
                # Balcony 1
                pygame.Rect(5, 49, 50, 3),
                # Balcony 2
                pygame.Rect(5, 33, 50, 3),
                # Balcony 3
                pygame.Rect(5, 17, 50, 3),

                # Roof
                pygame.Rect(0, 0, 60, 3),
            ])
            b.doors.extend([
                Alley(pygame.Rect(41, 64, 16, 17), StreetType.residential_stairs_interior, None),
            ])
            b.update_size(60, 80)
            return b
        elif building_type == BuildingType.residential_stairs_alt:
            b = Building(building_type)
            b.platforms.extend([
                # Planter
                pygame.Rect(0, 72, 41, 8),
                # Plant
                pygame.Rect(35, 65, 4, 7),
                # Balcony 1
                pygame.Rect(5, 49, 50, 3),
                # Balcony 2
                pygame.Rect(5, 33, 50, 3),
                # Balcony 3
                pygame.Rect(5, 17, 50, 3),

                # Roof
                pygame.Rect(0, 0, 60, 3),
            ])
            b.doors.extend([
            ])
            b.update_size(60, 80)
            return b
        elif building_type == BuildingType.residential_stairs_interior:
            b = Building(building_type)
            b.platforms.extend([
                # Floor 1
                pygame.Rect(7, 49, 52, 3),
                # Floor 2
                pygame.Rect(1, 33, 52, 3),
                # Floor 3
                pygame.Rect(7, 17, 52, 3),

                # Floor
                pygame.Rect(0, 80, 60, 100),
            ])
            b.ceilings.extend([
                # Top ceiling
                pygame.Rect(0, -10, 60, 11),
                # Floor 1
                pygame.Rect(7, 49, 52, 3),
                # Floor 2
                pygame.Rect(1, 33, 52, 3),
                # Floor 3
                pygame.Rect(7, 17, 52, 3),
            ])
            b.doors.extend([
                Alley(pygame.Rect(41, 64, 16, 17), None, StreetType._back),
                Alley(pygame.Rect(43, 5, 10, 13), StreetType.residential_stairs_interior_apt, None)
            ])
            b.update_size(60, 81)
            return b
        elif building_type == BuildingType.residential_stairs_interior_apt or building_type == BuildingType.residential_stairs_interior_apt_2:
            b = Building(building_type)
            b.platforms.extend([
                # Shoulders
                pygame.Rect(11, 12, 6, 5),

                # Floor
                pygame.Rect(0, 17, 18, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(0, -10, 18, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(1, 5, 10, 13), None, StreetType._back)
            ])
            b.interactions = {
                0: (pygame.Rect(11, 7, 6, 10), LogEntryText.friend_lines)
            }
            b.update_size(40, 23)
            return b
        elif building_type == BuildingType.vivo_interior:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(8, 45, 31, 3),
                pygame.Rect(8, 23, 31, 3),

                # Floor
                pygame.Rect(0, 67, 40, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(0, -10, 40, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(17, 56, 6, 12), None, StreetType._back),
                Alley(pygame.Rect(30, 34, 6, 12), StreetType.vivo_apt_1, None)
            ])
            b.update_size(40, 68)
            return b
        elif building_type == BuildingType.vivo_floor_1:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(8, 16, 8, 3),
                pygame.Rect(3, 19, 5, 3),

                # Floor
                pygame.Rect(0, 22, 40, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(0, -10, 40, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(30, 11, 6, 12), None, StreetType._back)
            ])
            b.update_size(40, 23)
            return b
        elif building_type == BuildingType.office_4_floor:
            b = Building(building_type)
            b.platforms.extend([
                # Steps
                pygame.Rect(18, 139, 24, 3),

                # Roof
                pygame.Rect(0, 0, 60, 3),
            ])
            b.doors.extend([
                Alley(pygame.Rect(25, 124, 10, 16), StreetType.office_4_floor_interior, None)
            ])
            b.update_size(60, 140)
            return b
        elif building_type == BuildingType.office_2_floor:
            b = Building(building_type)
            b.platforms.extend([
                # Lip
                pygame.Rect(0, 58, 70, 3),

                # Windows
                pygame.Rect(6, 47, 16, 3),
                pygame.Rect(27, 47, 16, 3),
                pygame.Rect(48, 47, 16, 3),
                pygame.Rect(6, 23, 16, 3),
                pygame.Rect(27, 23, 16, 3),
                pygame.Rect(48, 23, 16, 3),

                # Roof
                pygame.Rect(0, 0, 70, 3),
            ])
            b.interactions = {
                0: (pygame.Rect(27, 64, 16, 16), lambda p: LogEntryType.smalldosegames_door)
            }
            b.update_size(70, 80)
            return b
        elif building_type == BuildingType.office_3_floor:
            b = Building(building_type)
            b.platforms.extend([
                # Windows
                pygame.Rect(6, 47, 16, 3),
                pygame.Rect(27, 47, 16, 3),
                pygame.Rect(48, 47, 16, 3),
                pygame.Rect(6, 23, 16, 3),
                pygame.Rect(27, 23, 16, 3),
                pygame.Rect(48, 23, 16, 3),
                pygame.Rect(6, 71, 16, 3),
                pygame.Rect(27, 71, 16, 3),
                pygame.Rect(48, 71, 16, 3),

                # Roof
                pygame.Rect(0, 0, 70, 3),
            ])
            b.interactions = {
                0: (pygame.Rect(27, 64, 16, 16), lambda p: LogEntryType.smalldosegames_door)
            }
            b.update_size(70, 104)
            return b
        elif building_type == BuildingType.watertower:
            b = Building(building_type)
            b.platforms.extend([
                # Awning
                pygame.Rect(0, 11, 10, 3),
            ])
            b.update_size(11, 22)
            return b
        elif building_type == BuildingType.streetsign:
            b = Building(building_type)
            b.platforms.extend([
                # sign
                pygame.Rect(0, 1, 10, 4),
            ])
            b.update_size(10, 17)
            return b
        elif building_type == BuildingType.blocker:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 0, 6, 3),
            ])
            b.update_size(6, 6)
            return b
        elif building_type == BuildingType.sewer_cap:
            b = Building(building_type)
            b.doors.extend([
                Alley(pygame.Rect(0, -1, 8, 2), StreetType.sewer, None)
            ])
            b.update_size(8, 4)
            return b
        elif building_type == BuildingType.sewer or building_type == BuildingType.sewer_winged or building_type == BuildingType.sewer_light_winged:
            b = Building(building_type)
            b.platforms.extend([
                # Floor
                pygame.Rect(0, 19, 50, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(0, -10, 50, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(42, 1, 5, 19), None, StreetType._back),
            ])
            b.interactions = {
                0: (pygame.Rect(5, 0, 20, 20), LogEntryText.hamster_lines)
            }
            b.update_size(50, 20)
            return b
        elif building_type == BuildingType.boutique or building_type == BuildingType.boutique_alt:
            b = Building(building_type)
            b.platforms.extend([
                # Roof
                pygame.Rect(0, 0, 50, 3),
            ])
            b.doors.extend([
                Alley(pygame.Rect(4, 12, 9, 13), StreetType.boutique_interior, None),
            ])
            b.update_size(50, 24)
            return b
        elif building_type == BuildingType.boutique_interior or building_type == BuildingType.boutique_interior_alt:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(16, 21, 32, 3),

                # Floor
                pygame.Rect(0, 24, 50, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(0, -10, 50, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(4, 12, 9, 13), None, StreetType._back),
            ])
            b.update_size(50, 25)
            return b
        elif building_type == BuildingType.hospital_room_start:
            b = Building(building_type)
            b.update_size(30, 16)
            return b
        elif building_type == BuildingType.office_4_floor_interior:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(42, 26, 14, 6),

                # Floor
                pygame.Rect(0, 32, 60, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(0, -10, 60, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(25, 18, 10, 15), None, StreetType._back),
            ])
            b.interactions = {
                0: (pygame.Rect(46, 22, 6, 10), lambda p: LogEntryType.guard_1)
            }
            b.update_size(60, 30)
            return b
        elif building_type == BuildingType.hospital:
            b = Building(building_type)
            b.platforms.extend([
                # Roof
                pygame.Rect(0, 0, 75, 3),
            ])
            b.doors.extend([
                Alley(pygame.Rect(49, 45, 22, 15), StreetType.hospital_interior, None),
            ])
            b.interactions = {
                0: (pygame.Rect(46, 22, 6, 10), lambda p: LogEntryType.hospital)
            }
            b.update_size(75, 60)
            return b
        elif building_type == BuildingType.bench:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(1, 5, 13, 3)
            ])
            b.update_size(15, 9)
            return b
        elif building_type == BuildingType.statue:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(2, 30, 14, 3),
                pygame.Rect(0, 32, 2, 3),
                pygame.Rect(16, 32, 2, 3),
                pygame.Rect(0, 12, 18, 3),
                pygame.Rect(3, 3, 3, 3),
                pygame.Rect(6, 0, 6, 3),
            ])
            b.update_size(18, 40)
            return b
        elif building_type == BuildingType.statue_platform:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 2, 5, 3),
                pygame.Rect(5, 1, 5, 3),
                pygame.Rect(10, 0, 20, 3),
                pygame.Rect(30, 1, 5, 3),
                pygame.Rect(35, 2, 5, 3),
            ])
            b.update_size(40, 10)
            return b
        elif building_type == BuildingType.shopkeep:
            b = Building(building_type)
            b.platforms.extend([
            ])
            b.interactions = {
                0: (pygame.Rect(0, 0, 6, 10), LogEntryText.shopkeep_lines)
            }
            b.update_size(6, 10)
            return b
        elif building_type == BuildingType.mentor:
            b = Building(building_type)
            b.platforms.extend([
            ])
            b.interactions = {
                0: (pygame.Rect(0, 0, 6, 10), LogEntryText.mentor_lines)
            }
            b.update_size(6, 10)
            return b
        elif building_type == BuildingType.client:
            b = Building(building_type)
            b.platforms.extend([
            ])
            b.interactions = {
                0: (pygame.Rect(0, 0, 6, 10), LogEntryText.client_lines)
            }
            b.update_size(6, 10)
            return b
        elif building_type == BuildingType.hospital_interior:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(32, 38, 42, 3),
                pygame.Rect(1, 38, 20, 3),
                pygame.Rect(1, 18, 63, 3),

                # Desk
                pygame.Rect(32, 54, 14, 3),

                # bed
                pygame.Rect(60, 34, 11, 3),

                # Floor
                pygame.Rect(0, 60, 75, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(32, 38, 42, 3),
                pygame.Rect(1, 38, 20, 3),
                pygame.Rect(1, 18, 63, 3),
                pygame.Rect(0, -10, 75, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(49, 45, 22, 15), None, StreetType._back),
                Alley(pygame.Rect(6, 4, 9, 15), StreetType.hospital_room, None),
            ])
            b.interactions = {
                0: (pygame.Rect(36, 47, 6, 13), LogEntryText.nurse_lines),
                1: (pygame.Rect(6, 50, 12, 10), lambda p: LogEntryType.hospital)
            }
            b.update_size(75, 61)
            return b
        elif building_type == BuildingType.hospital_room:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(3, 11, 7, 3),

                # Floor
                pygame.Rect(0, 15, 30, 100),
            ])
            b.ceilings.extend([
                pygame.Rect(0, -10, 30, 11),
            ])
            b.doors.extend([
                Alley(pygame.Rect(20, 4, 8, 12), None, StreetType._back),
            ])
            b.interactions = {
                0: (pygame.Rect(2, 3, 8, 12), LogEntryText.patient_lines)
            }
            b.update_size(30, 16)
            return b
        elif building_type == BuildingType.tree:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(8, 0, 15, 3),
                pygame.Rect(0, 9, 4, 5),
                pygame.Rect(3, 2, 5, 3),
                pygame.Rect(25, 5, 2, 3),
            ])
            b.update_size(27, 31)
            return b
        elif building_type == BuildingType.dumpster:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 3, 18, 3),
            ])
            b.update_size(18, 12)
            return b
        elif building_type == BuildingType.window_washer:
            b = Building(building_type)
            b.platforms.extend([
                pygame.Rect(0, 8, 22, 3),
            ])
            b.interactions = {
                0: (pygame.Rect(0, 0, 22, 14), lambda p: LogEntryType.window_washer)
            }
            b.update_size(22, 14)
            return b

class Alley:
    def __init__(self, box, up_street_type, down_street_type):
        self.box = box
        self.up_street_type = up_street_type
        self.down_street_type = down_street_type

        self.up_name = StreetNames.street_type_to_name.get(up_street_type, None)
        self.down_name = StreetNames.street_type_to_name.get(down_street_type, None)

    def get_up_street(self):
        return Street.get_street_by_type(self.up_street_type)

    def get_down_street(self):
        return Street.get_street_by_type(self.down_street_type)

class StreetType(Enum):

    # Used to make interior streets replicatable.
    _back = auto()

    # Streets
    ocean_drive = auto()
    main_street = auto()
    park_lane = auto()

    # Interiors
    vivo = auto()
    vivo_apt_1 = auto()
    residential_stairs_interior = auto()
    residential_stairs_interior_apt = auto()
    sewer = auto()
    boutique_interior = auto()
    hospital_room_start = auto()
    hospital_interior = auto()
    hospital_room = auto()
    office_4_floor_interior = auto()

class StreetNames:
    street_type_to_name = {
        StreetType._back: "Oopsy...",

        StreetType.ocean_drive: "Ocean Drive",
        StreetType.main_street: "Main Street",
        StreetType.park_lane: "Park Lane",
        StreetType.vivo: "Vivo Apartments",
        StreetType.vivo_apt_1: "Vivo, Apt 1",
        StreetType.residential_stairs_interior: "Base12 Apartments",
        StreetType.residential_stairs_interior_apt: "Base12, Apt B",
        StreetType.sewer: "Sewer",
        StreetType.boutique_interior: "Fashionable Pixels",
        StreetType.hospital_room_start: "Hospital Room",
        StreetType.office_4_floor_interior: "Office",
        StreetType.hospital_interior: "Hospital",
        StreetType.hospital_room: "Hospital Room",
    }
    

class Street:
    def __init__(self):
        self.name = ""

        self.street_type = None

        self.buildings = []
        self.alleys = []
        # Streets should not back eachother or itself!!
        self.bg_street = None

        self.entry_x, self.entry_y = None, None

        self.min_x = 0
        self.max_x = 0
        self.left_message = None
        self.right_message = None

        self.inside = False
        self.is_backstreet = False
        self.background_color = (0, 148, 255)

    def empty_street():
        return Street()

    def get_street_by_type(street_type):
        street = Street()
        street.street_type = street_type
        street.name = StreetNames.street_type_to_name[street_type]
        if street_type == StreetType.ocean_drive:
            street.min_x = -180
            street.max_x = 180
            street.left_message = LogEntryType.street3_left_blocker
            street.right_message = LogEntryType.street3_right_blocker
            street.buildings.extend([
                # Building.get_building_by_type(BuildingType.brick).move(0, -89),
                # Building.get_building_by_type(BuildingType.awning).move(60, -30),
                Building.get_building_by_type(BuildingType.waterfront).move(-270, 0), #inaccessible
                Building.get_building_by_type(BuildingType.residential_stairs_alt).move(-242, -80),
                Building.get_building_by_type(BuildingType.waterfront).move(-180, 0), # beginning
                # -160 to -100
                Building.get_building_by_type(BuildingType.residential_stairs).move(-160, -80),
                # -95 to -25
                Building.get_building_by_type(BuildingType.office_3_floor).move_0(-95),
                # Alley -105 to -85
                # -85 to -15
                # Building.get_building_by_type(BuildingType.office_2_floor).move(-85, -80),
                Building.get_building_by_type(BuildingType.waterfront).move(-90, 0),
                Building.get_building_by_type(BuildingType.waterfront).move(0, 0),
                # Alley -15 to 15
                Building.get_building_by_type(BuildingType.waterfront).move(90, 0),
                Building.get_building_by_type(BuildingType.awning).move_0(20),
                # 65 to 135
                Building.get_building_by_type(BuildingType.office_2_floor).move_0(65),
                # 135 to 195
                Building.get_building_by_type(BuildingType.office_4_floor).move_0(135),
                Building.get_building_by_type(BuildingType.office_4_floor).move_0(200),
                Building.get_building_by_type(BuildingType.waterfront).move(180, 0), # end, inaccessible

                # Front
                Building.get_building_by_type(BuildingType.tree).move(28, -64),
                Building.get_building_by_type(BuildingType.mentor).move(75, -90),
                Building.get_building_by_type(BuildingType.watertower).move(105, -102),
                Building.get_building_by_type(BuildingType.blocker).move(-186, -6),
                Building.get_building_by_type(BuildingType.blocker).move(180, -6),
                Building.get_building_by_type(BuildingType.streetsign).move_0(9),
                Building.get_building_by_type(BuildingType.bench).move_0(-46),
                Building.get_building_by_type(BuildingType.dumpster).move_0(-180)
            ])
            street.alleys.extend([
                Alley(pygame.Rect(-15, -20, 30, 21), StreetType.park_lane, None)
            ])
            street.bg_street = Street.get_street_by_type(StreetType.park_lane)
            return street
        elif street_type == StreetType.park_lane:
            street.min_x = -180
            street.max_x = 180
            street.left_message = LogEntryType.street2_left_blocker
            street.right_message = LogEntryType.street2_right_blocker
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.park).move(-270, -5),
                Building.get_building_by_type(BuildingType.tree).move_0(-230),
                Building.get_building_by_type(BuildingType.park).move(-180, -5),
                Building.get_building_by_type(BuildingType.boutique).move(-160, -24),
                Building.get_building_by_type(BuildingType.tree).move_0(-180),
                Building.get_building_by_type(BuildingType.bench).move_0(-176),
                Building.get_building_by_type(BuildingType.park).move(-90, -5),
                Building.get_building_by_type(BuildingType.tree).move_0(-72),
                Building.get_building_by_type(BuildingType.tree).move_0(-51),
                Building.get_building_by_type(BuildingType.statue_platform).move_0(-20),
                Building.get_building_by_type(BuildingType.bench).move_0(-7),
                Building.get_building_by_type(BuildingType.statue).move(-9, -50),
                Building.get_building_by_type(BuildingType.park).move(0, -5),
                Building.get_building_by_type(BuildingType.tree).move_0(45),
                Building.get_building_by_type(BuildingType.park).move(90, -5),
                Building.get_building_by_type(BuildingType.tree).move_0(110),
                Building.get_building_by_type(BuildingType.bench).move_0(140),
                Building.get_building_by_type(BuildingType.client).move(148, -14),
                Building.get_building_by_type(BuildingType.tree).move_0(160),
                Building.get_building_by_type(BuildingType.tree).move_0(210),
                Building.get_building_by_type(BuildingType.park).move(180, -5),
                Building.get_building_by_type(BuildingType.streetsign).move_0(-109),
                Building.get_building_by_type(BuildingType.streetsign).move_0(101),
            ])
            street.alleys.extend([
                Alley(pygame.Rect(-15, -20, 30, 21), None, StreetType.ocean_drive),
                Alley(pygame.Rect(-105, -20, 30, 21), StreetType.main_street, None),
                Alley(pygame.Rect(75, -20, 30, 21), StreetType.main_street, None)
            ])
            street.bg_street = Street.get_street_by_type(StreetType.main_street)
            return street
        elif street_type == StreetType.main_street:
            street.min_x = -180
            street.max_x = 180
            street.left_message = LogEntryType.street1_left_blocker
            street.right_message = LogEntryType.street1_right_blocker
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.brick).move_0(-237),
                Building.get_building_by_type(BuildingType.road).move(-270, 0),
                Building.get_building_by_type(BuildingType.road).move(-180, 0),
                # -180 to -105
                Building.get_building_by_type(BuildingType.hospital).move_0(-180),
                # -103 to -43
                Building.get_building_by_type(BuildingType.residential_stairs_alt).move_0(-103),
                # -42 to 18
                Building.get_building_by_type(BuildingType.office_4_floor).move_0(-42),
                Building.get_building_by_type(BuildingType.window_washer).move(-23, -120),
                # 35 to 75
                Building.get_building_by_type(BuildingType.residential_2_floor).move_0(35),
                # 75 to 105
                Building.get_building_by_type(BuildingType.blocker).move_0(75),
                Building.get_building_by_type(BuildingType.blocker).move_0(81),
                Building.get_building_by_type(BuildingType.blocker).move_0(87),
                Building.get_building_by_type(BuildingType.blocker).move_0(93),
                Building.get_building_by_type(BuildingType.blocker).move_0(99),
                # 105 to 165
                Building.get_building_by_type(BuildingType.residential_stairs_alt).move_0(105),
                Building.get_building_by_type(BuildingType.office_3_floor).move_0(167),
                Building.get_building_by_type(BuildingType.road).move(-90, 0),
                Building.get_building_by_type(BuildingType.road).move(0, 0),
                Building.get_building_by_type(BuildingType.road).move(90, 0),
                Building.get_building_by_type(BuildingType.road).move(180, 0),

                Building.get_building_by_type(BuildingType.streetsign).move_0(-109),
                Building.get_building_by_type(BuildingType.streetsign).move_0(101),
                Building.get_building_by_type(BuildingType.sewer_cap).move(125, 0),
                Building.get_building_by_type(BuildingType.bench).move_0(164),
                Building.get_building_by_type(BuildingType.dumpster).move_0(18)
            ])
            street.alleys.extend([
                Alley(pygame.Rect(-105, -20, 30, 21), None, StreetType.park_lane),
                Alley(pygame.Rect(75, -20, 30, 21), None, StreetType.park_lane)
            ])
            street.bg_street = Street.empty_street()
            return street
        elif street_type == StreetType.vivo:
            street.min_x = 1
            street.max_x = 39
            street.entry_x = 18
            street.entry_y = 57
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.vivo_interior),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            return street
        elif street_type == StreetType.vivo_apt_1:
            street.min_x = 1
            street.max_x = 39
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.vivo_floor_1),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            return street
        elif street_type == StreetType.residential_stairs_interior:
            street.min_x = 1
            street.max_x = 59
            street.entry_x = 46
            street.entry_y = 70
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.residential_stairs_interior),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            return street
        elif street_type == StreetType.residential_stairs_interior_apt:
            street.min_x = 1
            street.max_x = 17
            street.entry_x = 3
            street.entry_y = 7
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.residential_stairs_interior_apt),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            street.background_color = (178, 0, 255)
            return street
        elif street_type == StreetType.sewer:
            street.min_x = 5
            street.max_x = 49
            street.entry_x = 41
            street.entry_y = 2
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.sewer),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            street.background_color = (0, 0, 0)
            return street
        elif street_type == StreetType.boutique_interior:
            street.min_x = 1
            street.max_x = 49
            street.entry_x = 5
            street.entry_y = 14
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.boutique_interior),
                Building.get_building_by_type(BuildingType.shopkeep).move(28, 14),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            street.background_color = (128, 128, 128)
            return street
        elif street_type == StreetType.hospital_room_start:
            street.background_color = (255, 0, 220)
            street.bg_street = Street.empty_street()
            street.inside = True
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.hospital_room_start),
            ])
            return street
        elif street_type == StreetType.office_4_floor_interior:
            street.min_x = 1
            street.max_x = 59
            street.entry_x = 27
            street.entry_y = 22
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.office_4_floor_interior),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            return street
        elif street_type == StreetType._back:
            street.is_backstreet = True
            return street
        elif street_type == StreetType.hospital_interior:
            street.min_x = 1
            street.max_x = 74
            street.entry_x = 60
            street.entry_y = 50
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.hospital_interior),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            street.background_color = (128, 106, 0)
            return street
        elif street_type == StreetType.hospital_room:
            street.min_x = 1
            street.max_x = 29
            street.entry_x = 21
            street.entry_y = 5
            street.buildings.extend([
                Building.get_building_by_type(BuildingType.hospital_room),
            ])
            street.bg_street = Street.empty_street()
            street.inside = True
            street.background_color = (255, 0, 220)
            return street

    def platforms(self):
        for b in self.buildings:
            for p in b.platforms:
                yield p

    def ceilings(self):
        for b in self.buildings:
            for p in b.ceilings:
                yield p

    def interactions(self):
        for b in self.buildings:
            for p in b.interactions.values():
                yield p

    def get_alleys(self):
        for a in self.alleys:
            yield a

        for b in self.buildings:
            for p in b.doors:
                yield p

    def replace_building_type(self, old_type, new_type):
        for b in self.buildings:
            if b.building_type == old_type:
                b.building_type = new_type

class CharacterState(Enum):
    wait = auto()
    run_left_1 = auto()
    run_left_2 = auto()
    run_right_1 = auto()
    run_right_2 = auto()
    run_up_down_1 = auto()
    run_up_down_2 = auto()
    sitting = auto()

    def transition(state, x_move, y_move, idle=False):
        if x_move == 0 and y_move == 0:
            return CharacterState.wait if not idle else CharacterState.sitting

        if x_move < 0:
            if state == CharacterState.run_left_1:
                return CharacterState.run_left_2
            return CharacterState.run_left_1

        if x_move > 0:
            if state == CharacterState.run_right_1:
                return CharacterState.run_right_2
            return CharacterState.run_right_1

        if state == CharacterState.run_up_down_1:
            return CharacterState.run_up_down_2
        return CharacterState.run_up_down_1

class CharacterTextures:
    __state_to_texture_path = {
        CharacterState.wait : "frontleft.png",
        CharacterState.run_left_1 : "leftwalk1.png",
        CharacterState.run_left_2 : "leftwalk2.png",
        CharacterState.run_right_1 : "frontrightwalk1.png",
        CharacterState.run_right_2 : "frontrightwalk2.png",
        CharacterState.run_up_down_1 : "frontwalk1.png",
        CharacterState.run_up_down_2 : "frontwalk2.png",
        CharacterState.sitting : "sitting.png",
    }

    __textures = {
    }

    def load(size):
        for k, v in CharacterTextures.__state_to_texture_path.items():
            CharacterTextures.__textures[k] = pygame.transform.scale(pygame.image.load("assets/" + v).convert_alpha(), size)

    def get(state):
        return CharacterTextures.__textures[state]

class Character:
    def __init__(self):
        self.state = CharacterState.sitting
        self.state_frames_the_same = 50
        self.x = -16.0
        self.y = -150.0
        self.x_move = 0.0
        self.y_move = 0.0
        self.has_jump = True

        self.foot_box = pygame.Rect(self.x + 1, self.y + 10, 4, 1)
        self.head_box = pygame.Rect(self.x, self.y - 1, 6, 1)
        self.body_box = pygame.Rect(self.x, self.y, 6, 10)

    def transition(self, idle=False):
        new_state = CharacterState.transition(self.state, self.x_move, self.y_move, idle=self.state_frames_the_same > 30)
        if new_state == CharacterState.sitting or new_state == self.state:
            self.state_frames_the_same += 1
        else:
            self.state_frames_the_same = 0
        self.state = new_state

    def move(self):
        self.x += self.x_move
        self.y += self.y_move

        self.foot_box = pygame.Rect(self.x + 1, self.y + 10, 4, 1)
        self.head_box = pygame.Rect(self.x, self.y - 1, 6, 1)
        self.body_box = pygame.Rect(self.x, self.y, 6, 10)

class MissionPhase(Enum):
    opening_cut_scene = 0

    get_mission_1 = 1

    # 1: Need to talk to client
    # 2: Need to deliver the news.
    bad_news_1 = 2
    bad_news_2 = 3

    get_mission_2 = 4

    # 1: Need to get the wings.
    # 2: Need to deliver the wings.
    wings_1 = 5
    wings_2 = 6

    get_mission_3 = 7

    # 1: Need to deliver baby.
    baby_1 = 8

    end = 9

class LogEntryType(Enum):

    # Incidentals
    street1_left_blocker = auto()
    street1_right_blocker = auto()
    street2_left_blocker = auto()
    street2_right_blocker = auto()
    street3_left_blocker = auto()
    street3_right_blocker = auto()
    guard_1 = auto()
    guard_2 = auto()
    hospital = auto()
    window_washer = auto()
    smalldosegames_door = auto()

    # Opening
    opening_screen_1 = auto()
    opening_screen_2 = auto()
    opening_screen_3 = auto()
    opening_screen_4 = auto()

    # Mission
    _continue = auto()
    _end = auto()
    opening_cut_scene_1 = auto()
    opening_cut_scene_2 = auto()
    opening_cut_scene_3 = auto()
    opening_cut_scene_4 = auto()
    opening_cut_scene_5 = auto()
    opening_cut_scene_6 = auto()

    client_1 = auto()

    mentor_cut_scene_1 = auto()
    mentor_cut_scene_2 = auto()
    mentor_cut_scene_3 = auto()
    mentor_cut_scene_4 = auto()
    mentor_cut_scene_5 = auto()
    mentor_cut_scene_6 = auto()
    mentor_cut_scene_A = auto()
    mentor_cut_scene_7 = auto()

    mentor_1 = auto()

    bad_news_cut_scene_1 = auto()
    bad_news_cut_scene_2 = auto()
    bad_news_cut_scene_3 = auto()
    bad_news_cut_scene_4 = auto()
    bad_news_cut_scene_5 = auto()
    bad_news_cut_scene_A = auto()
    bad_news_cut_scene_6 = auto()

    friend_1 = auto()
    mentor_2 = auto()
    client_2 = auto()

    bad_news_cut_scene_7 = auto()
    bad_news_cut_scene_8 = auto()
    bad_news_cut_scene_9 = auto()
    bad_news_cut_scene_10 = auto()
    bad_news_cut_scene_11 = auto()
    bad_news_cut_scene_12 = auto()
    bad_news_cut_scene_13 = auto()
    bad_news_cut_scene_14 = auto()

    client_3 = auto()
    friend_2 = auto()
    hamster_1 = auto()

    mentor_cut_scene_8 = auto()
    mentor_cut_scene_9 = auto()
    mentor_cut_scene_10 = auto()
    mentor_cut_scene_11 = auto()
    mentor_cut_scene_12 = auto()
    mentor_cut_scene_13 = auto()

    mentor_3 = auto()
    shopkeep_1 = auto()
    hamster_2 = auto()

    wings_cut_scene_1 = auto()
    wings_cut_scene_2 = auto()

    mentor_4 = auto()
    shopkeep_2 = auto()

    wings_cut_scene_3 = auto()
    wings_cut_scene_4 = auto()
    wings_cut_scene_5 = auto()

    friend_3 = auto()
    hamster_3 = auto()
    nurse_1 = auto()

    mentor_cut_scene_14 = auto()
    mentor_cut_scene_15 = auto()
    mentor_cut_scene_16 = auto()
    mentor_cut_scene_17 = auto()
    mentor_cut_scene_18 = auto()

    mentor_5 = auto()

    patient_1 = auto()
    nurse_2 = auto()

    end_cut_scene_1 = auto()
    end_cut_scene_A = auto()
    end_cut_scene_2 = auto()
    end_cut_scene_3 = auto()

class LogEntryText:
    entry_to_text = {
        LogEntryType.street1_left_blocker : "This barrier is mightier than it looks.",
        LogEntryType.street1_right_blocker : "No... my city needs me...",
        LogEntryType.street2_left_blocker : "It's just more park.",
        LogEntryType.street2_right_blocker : "It's just more park.",
        LogEntryType.street3_left_blocker : "They're setting up a parade.",
        LogEntryType.street3_right_blocker : "Is everything in this town closed?",
        LogEntryType.smalldosegames_door : "This is Red_dino Games' office, they're probably busy.",
        LogEntryType.guard_1 : "I only do shoulders at the gym.",
        LogEntryType.guard_2 : "I might not be wearing pants, you don't know.",
        LogEntryType.hospital : "Doesn't this doctor have something better to do?",
        LogEntryType.window_washer : "Woah, watch out!",

        LogEntryType._continue : "(Continue)",
        LogEntryType._end : "(The End)",

        LogEntryType.opening_screen_1: "Ludum Dare 53: Delivery",
        LogEntryType.opening_screen_2: "Game by Red_dino",
        LogEntryType.opening_screen_3: "Music by Sirental from itch.io",
        LogEntryType.opening_screen_4: "Font by Indian Type Foundary",

        LogEntryType.opening_cut_scene_1 : "Well, I guess my job here is done.",
        LogEntryType.opening_cut_scene_2 : "Now that there's a new child in town,",
        LogEntryType.opening_cut_scene_3 : "guess I'll finally get to retire from delivering.",
        LogEntryType.opening_cut_scene_4 : "Come see me when you're ready to start work kid.",
        LogEntryType.opening_cut_scene_5 : "I'll be by the water tower on Ocean.",
        LogEntryType.opening_cut_scene_6 : "There's a nice sittin' spot I've been eyeing...",

        LogEntryType.client_1 : "*Mutters* Hmm, I wonder how I should do it...",

        LogEntryType.mentor_cut_scene_1 : "You made it!",
        LogEntryType.mentor_cut_scene_2 : "I'll let you take care of my back log,",
        LogEntryType.mentor_cut_scene_3 : "then you're on your own.",
        LogEntryType.mentor_cut_scene_4 : "*Mutters* I've been avoiding this one for ages...",
        LogEntryType.mentor_cut_scene_5 : "Someone wants to break up with their friend.",
        LogEntryType.mentor_cut_scene_6 : "They're waiting in the park where they'll tell you more.",
        LogEntryType.mentor_cut_scene_A : "I'll be here to give you your next job when you're done.",
        LogEntryType.mentor_cut_scene_7 : "Good luck!",

        LogEntryType.mentor_1 : "Already forgot? You need to find the client in the park.",

        LogEntryType.bad_news_cut_scene_1 : "Oh, you're from the delivery service!",
        LogEntryType.bad_news_cut_scene_2 : "Can you let down my friend lightly please?",
        LogEntryType.bad_news_cut_scene_3 : "We've just grown apart... and well",
        LogEntryType.bad_news_cut_scene_4 : "I'd do it myself, but these things make me so nervous.",
        LogEntryType.bad_news_cut_scene_5 : "My friend lives at Base12 Apartments, Apt B.",
        LogEntryType.bad_news_cut_scene_A : "Well, former friend I guess...",
        LogEntryType.bad_news_cut_scene_6 : "Thank you so much.",

        LogEntryType.friend_1 : "Ahh, my bestie is so amazing.",
        LogEntryType.mentor_2 : "Now for the hard part.",
        LogEntryType.client_2 : "If you must know... they're just a little clingy.",

        LogEntryType.bad_news_cut_scene_7 : "Ahh, my bestie is so amazing.",
        LogEntryType.bad_news_cut_scene_8 : "Oh, sorry, just daydreaming.",
        LogEntryType.bad_news_cut_scene_9 : "Wait, what?? WHATTTT???",
        LogEntryType.bad_news_cut_scene_10 : "It can't be... one second you're parkouring together..",
        LogEntryType.bad_news_cut_scene_11 : "and the next...",
        LogEntryType.bad_news_cut_scene_12 : "To be frank, I'm heartbroken.",
        LogEntryType.bad_news_cut_scene_13 : "Thanks for your compassion though.",
        LogEntryType.bad_news_cut_scene_14 : "I guess that's why you're a pro.",

        LogEntryType.client_3 : "I can really rest easy now, thank you!",
        LogEntryType.friend_2 : "I'm feeling blue, please give me space.",
        LogEntryType.hamster_1 : "Go away, I'm online shopping.",

        LogEntryType.mentor_cut_scene_8 : "Well, how'd it go?",
        LogEntryType.mentor_cut_scene_9 : "Great! Sounds like you're a natural.",
        LogEntryType.mentor_cut_scene_10 : "Next up, a Triangle needs to get its wings.",
        LogEntryType.mentor_cut_scene_11 : "Head over to Fashionable Pixels and pick up their order.",
        LogEntryType.mentor_cut_scene_12 : "Then deliver it to them in the sewer.",
        LogEntryType.mentor_cut_scene_13 : "You got this.",

        LogEntryType.mentor_3 : "Fashionable Pixels, then the sewer.",
        LogEntryType.shopkeep_1 : "Orange is so in right now.",
        LogEntryType.hamster_2 : "It says order ready for pickup, where are they!",

        LogEntryType.wings_cut_scene_1 : "Hi, welcome in! Yes, online order for pickup?",
        LogEntryType.wings_cut_scene_2 : "Here you go!",

        LogEntryType.mentor_4 : "Woah, that's a fashion statement all right...",
        LogEntryType.shopkeep_2 : "Great choice, those wings are going to look great on you.",

        LogEntryType.wings_cut_scene_3 : "You have my package, I can smell it!",
        LogEntryType.wings_cut_scene_4 : "Yes!! Let me turn on some lights...",
        LogEntryType.wings_cut_scene_5 : "I look amazing!!",

        LogEntryType.friend_3 : "I'm feeling better, thanks. Want to be my friend?",
        LogEntryType.hamster_3 : "I feel like taking over the city in these!",
        LogEntryType.nurse_1 : "Welcome, please use a quiet voice.",

        LogEntryType.mentor_cut_scene_14 : "Good work kid.",
        LogEntryType.mentor_cut_scene_15 : "Looks like we're at the end of the line.",
        LogEntryType.mentor_cut_scene_16 : "My final task for you is at the Hospital.",
        LogEntryType.mentor_cut_scene_17 : "Seems like there's a baby on the way.",
        LogEntryType.mentor_cut_scene_18 : "Hey, before you go. I'm proud of you.",

        LogEntryType.mentor_5 : "I'm going to sit here for the rest of my days.",

        LogEntryType.patient_1 : "Hmm, I wonder what I should name my baby.",
        LogEntryType.nurse_2 : "The patient is upstairs and all the way to the left.",

        LogEntryType.end_cut_scene_1 : "You're just in time! Hurry!",
        LogEntryType.end_cut_scene_A : "AAAAHHHH",
        LogEntryType.end_cut_scene_2 : "*Yes, I've been here before.*",
        LogEntryType.end_cut_scene_3 : "*I've seen this, but through different eyes.*",
    
    }

    scene_triggers = {
        LogEntryType.mentor_cut_scene_1,
        LogEntryType.bad_news_cut_scene_1,
        LogEntryType.bad_news_cut_scene_7,
        LogEntryType.mentor_cut_scene_8,
        LogEntryType.wings_cut_scene_1,
        LogEntryType.wings_cut_scene_3,
        LogEntryType.mentor_cut_scene_14,
        LogEntryType.end_cut_scene_1,
    }

    opening_screen = [
        LogEntryType.opening_screen_1,
        LogEntryType.opening_screen_2,
        LogEntryType.opening_screen_3,
        LogEntryType.opening_screen_4,
    ]

    mission_phase_to_conversation = {
        MissionPhase.opening_cut_scene: [
            LogEntryType.opening_cut_scene_1,
            LogEntryType.opening_cut_scene_2,
            LogEntryType.opening_cut_scene_3,
            LogEntryType.opening_cut_scene_4,
            LogEntryType.opening_cut_scene_5,
            LogEntryType.opening_cut_scene_6,
            LogEntryType._continue,
        ],
        MissionPhase.get_mission_1: [
            LogEntryType.mentor_cut_scene_1,
            LogEntryType.mentor_cut_scene_2,
            LogEntryType.mentor_cut_scene_3,
            LogEntryType.mentor_cut_scene_4,
            LogEntryType.mentor_cut_scene_5,
            LogEntryType.mentor_cut_scene_6,
            LogEntryType.mentor_cut_scene_A,
            LogEntryType.mentor_cut_scene_7,
            LogEntryType._continue,
        ],
        MissionPhase.bad_news_1: [
            LogEntryType.bad_news_cut_scene_1,
            LogEntryType.bad_news_cut_scene_2,
            LogEntryType.bad_news_cut_scene_3,
            LogEntryType.bad_news_cut_scene_4,
            LogEntryType.bad_news_cut_scene_5,
            LogEntryType.bad_news_cut_scene_A,
            LogEntryType.bad_news_cut_scene_6,
            LogEntryType._continue,
        ],
        MissionPhase.bad_news_2: [
            LogEntryType.bad_news_cut_scene_7,
            LogEntryType.bad_news_cut_scene_8,
            LogEntryType.bad_news_cut_scene_9,
            LogEntryType.bad_news_cut_scene_10,
            LogEntryType.bad_news_cut_scene_11,
            LogEntryType.bad_news_cut_scene_12,
            LogEntryType.bad_news_cut_scene_13,
            LogEntryType.bad_news_cut_scene_14,
            LogEntryType._continue,
        ],
        MissionPhase.get_mission_2: [
            LogEntryType.mentor_cut_scene_8,
            LogEntryType.mentor_cut_scene_9,
            LogEntryType.mentor_cut_scene_10,
            LogEntryType.mentor_cut_scene_11,
            LogEntryType.mentor_cut_scene_12,
            LogEntryType.mentor_cut_scene_13,
            LogEntryType._continue,
        ],
        MissionPhase.wings_1: [
            LogEntryType.wings_cut_scene_1,
            LogEntryType.wings_cut_scene_2,
            LogEntryType._continue,
        ],
        MissionPhase.wings_2: [
            LogEntryType.wings_cut_scene_3,
            LogEntryType.wings_cut_scene_4,
            LogEntryType.wings_cut_scene_5,
            LogEntryType._continue,
        ],
        MissionPhase.get_mission_3: [
            LogEntryType.mentor_cut_scene_14,
            LogEntryType.mentor_cut_scene_15,
            LogEntryType.mentor_cut_scene_16,
            LogEntryType.mentor_cut_scene_17,
            LogEntryType.mentor_cut_scene_18,
            LogEntryType._continue,
        ],
        MissionPhase.baby_1: [
            LogEntryType.end_cut_scene_1,
            LogEntryType.end_cut_scene_A,
            LogEntryType.end_cut_scene_2,
            LogEntryType.end_cut_scene_3,
            LogEntryType.opening_cut_scene_1,
            LogEntryType._end,
        ],
    }

    def mentor_lines(mission_phase):
        if mission_phase.value == MissionPhase.get_mission_1.value:
            return LogEntryType.mentor_cut_scene_1
        elif mission_phase.value == MissionPhase.bad_news_1.value:
            return LogEntryType.mentor_1
        elif mission_phase.value == MissionPhase.bad_news_2.value:
            return LogEntryType.mentor_2
        elif mission_phase.value == MissionPhase.get_mission_2.value:
            return LogEntryType.mentor_cut_scene_8
        elif mission_phase.value == MissionPhase.wings_1.value:
            return LogEntryType.mentor_3
        elif mission_phase.value == MissionPhase.wings_2.value:
            return LogEntryType.mentor_4
        elif mission_phase.value == MissionPhase.get_mission_3.value:
            return LogEntryType.mentor_cut_scene_14
        elif mission_phase.value == MissionPhase.baby_1.value:
            return LogEntryType.mentor_5

    def client_lines(mission_phase):
        if mission_phase.value < MissionPhase.bad_news_1.value:
            return LogEntryType.client_1
        elif mission_phase.value == MissionPhase.bad_news_1.value:
            return LogEntryType.bad_news_cut_scene_1
        elif mission_phase.value == MissionPhase.bad_news_2.value:
            return LogEntryType.client_2
        else:
            return LogEntryType.client_3

    def friend_lines(mission_phase):
        if mission_phase.value < MissionPhase.bad_news_2.value:
            return LogEntryType.friend_1
        elif mission_phase.value == MissionPhase.bad_news_2.value:
            return LogEntryType.bad_news_cut_scene_7
        elif mission_phase.value > MissionPhase.wings_2.value:
            return LogEntryType.friend_3
        else:
            return LogEntryType.friend_2

    def shopkeep_lines(mission_phase):
        if mission_phase.value < MissionPhase.wings_1.value:
            return LogEntryType.shopkeep_1
        elif mission_phase.value == MissionPhase.wings_1.value:
            return LogEntryType.wings_cut_scene_1
        else:
            return LogEntryType.shopkeep_2

    def hamster_lines(mission_phase):
        if mission_phase.value < MissionPhase.wings_1.value:
            return LogEntryType.hamster_1
        elif mission_phase.value == MissionPhase.wings_1.value:
            return LogEntryType.hamster_2
        elif mission_phase.value == MissionPhase.wings_2.value:
            return LogEntryType.wings_cut_scene_3
        else:
            return LogEntryType.hamster_3

    def nurse_lines(mission_phase):
        if mission_phase.value < MissionPhase.baby_1.value:
            return LogEntryType.nurse_1
        else:
            return LogEntryType.nurse_2

    def patient_lines(mission_phase):
        if mission_phase.value < MissionPhase.baby_1.value:
            return LogEntryType.patient_1
        else:
            return LogEntryType.end_cut_scene_1

class Log:

    def __init__(self):
        self.items = []
        self.active = set()

        self.fixed_mode = True

    def log(self, entry):
        if entry not in self.active:
            self.items.insert(0, (entry, pygame.time.get_ticks()))
            self.active.add(entry)

    def get_active_text(self):
        self.active = set()
        temp_items = []
        curr_time = pygame.time.get_ticks()
        for i in range(len(self.items)):
            item = self.items[i]
            if self.fixed_mode or curr_time - item[1] < 3000:
                temp_items.append(item)
                self.active.add(item[0])
                yield LogEntryText.entry_to_text[item[0]]
            else:
                break
        self.items = temp_items

    def clear_and_toggle_fixed_mode(self):
        self.clear()
        self.fixed_mode = not self.fixed_mode

    def clear(self):
        self.items = []
        self.active = set()

class Game:

    async def run():
        pygame.init()
        pygame.display.set_caption("A City Minute")
        screen_size = (1200, 900)
        screen = pygame.display.set_mode(screen_size) #, pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        factor = 1200 // 120
        x_move_factor = 1200 / 1200
        y_move_factor = 900 / 900

        clock = pygame.time.Clock()
        frame = 0

        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.music.load("assets/music.ogg")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)

        character_size = (6 * factor, 10 * factor)
        CharacterTextures.load(character_size)
        mc = Character()
        mc_loc = (1200 / 2 - 30, 900 - 300) # / 2 - 50)

        text_size = 40
        text_y = 896 - text_size
        # font = pygame.freetype.Font("assets/font.ttf", text_size)

        alley_up = False
        alley_down = False
        alley_down_name = None
        alley_up_name = None

        street = Street.get_street_by_type(StreetType.main_street)
        street_stack = []

        log = Log()
        interaction_log_lambda = None
        for entry in LogEntryText.opening_screen:
            log.log(entry)

        opening_screen = True
        opening_graphic = pygame.transform.scale(pygame.image.load("assets/logo.png").convert_alpha(), (1200, 500))

        curr_phase = MissionPhase.opening_cut_scene
        cut_scene = True
        cut_scene_continue = False
        cut_scene_index = 0
        
        running = True

        def scale_x(t, factor, mc_loc, mc_v_loc):
            return (
                10 * ((t.x - mc_loc[0]) * factor + mc_loc[0]) - 10 * mc_loc[0] + mc_v_loc[0],
                # 10 * t.x + mc_v_loc[0] - 10 * mc_loc[0],
                10 * t.y + mc_v_loc[1] - 10 * mc_loc[1],
                t.w * 10 * factor,
                t.h * 10
            )

        while running:
            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    screen_size = event.size
                    screen_size = (max(screen_size[0], 1200), max(screen_size[1], 900))
                    factor = screen_size[0] // 120
                    x_move_factor = screen_size[0] / 1200
                    y_move_factor = screen_size[1] / 900
                    character_size = (6 * factor, 10 * factor)
                    CharacterTextures.load(character_size)
                    screen = pygame.display.set_mode(event.size)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_p:
                        pygame.image.save(screen, str(pygame.time.get_ticks()) + ".png")

                    if cut_scene or opening_screen:
                        cut_scene_continue = True
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        mc.x_move = -1.0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        mc.x_move = 1.0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        alley_up = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        alley_down = True
                    elif event.key == pygame.K_e:
                        if interaction_log_lambda:
                            val = interaction_log_lambda(curr_phase)
                            if val in LogEntryText.scene_triggers:
                                cut_scene = True
                                cut_scene_continue = True
                                log.clear_and_toggle_fixed_mode()
                            else:
                                log.log(val)
                    elif event.key == pygame.K_SPACE:
                        if mc.has_jump:
                            mc.y_move = -2.4
                            mc.has_jump = False

                        # initial_jump_speed = 24 / 10
                        # max_jh = initial_jump_speed + (initial_jump_speed - 1) + ... + 2 + 1
                        # max_jh = (initial_jump_speed * (initial_jump_speed + 1) / 2) / 10
                        # max_jh = 12 * 25 / 10 = 6 * 5 = 30

                    frame = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if mc.x_move < 0:
                            mc.x_move = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if mc.x_move > 0:
                            mc.x_move = 0
                    frame = 10
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass

            # Logic
            if opening_screen:
                if cut_scene_continue:
                    opening_screen = False
                    mc.x = 17
                    mc.y = 5
                    mc.state = CharacterState.wait
                    street = Street.get_street_by_type(StreetType.hospital_room_start)
                    cut_scene = True
                    cut_scene_continue = True
                    log.clear()
            elif cut_scene:
                if cut_scene_continue and cut_scene_index >= len(LogEntryText.mission_phase_to_conversation[curr_phase]):
                    cut_scene_index = 0
                    cut_scene = False
                    log.clear_and_toggle_fixed_mode()
                    if curr_phase == MissionPhase.opening_cut_scene:
                        street_stack = [
                            (Street.get_street_by_type(StreetType.main_street), (52, -10)),
                            (Street.get_street_by_type(StreetType.vivo), (30, 35)),
                        ]
                        street = Street.get_street_by_type(StreetType.vivo_apt_1)
                        mc.x, mc.y = (3, 9)
                        mc.state = CharacterState.sitting
                        mc.state_frames_the_same = 50

                    curr_phase = MissionPhase(curr_phase.value + 1)
                    if curr_phase == MissionPhase.end:
                        opening_screen = True
                        mc.x, mc.y = (-16, -150)
                        mc.state = CharacterState.sitting
                        street = Street.get_street_by_type(StreetType.main_street)
                        curr_phase = MissionPhase.opening_cut_scene
                        log.clear()
                        log.fixed_mode = True
                        for entry in LogEntryText.opening_screen:
                            log.log(entry)
                elif cut_scene_continue:
                    entry = LogEntryText.mission_phase_to_conversation[curr_phase][cut_scene_index]
                    log.log(entry)

                    # Scene change logic
                    if entry == LogEntryType.bad_news_cut_scene_11:
                        street.replace_building_type(BuildingType.residential_stairs_interior_apt, BuildingType.residential_stairs_interior_apt_2)
                    elif entry == LogEntryType.wings_cut_scene_2:
                        street.replace_building_type(BuildingType.boutique_interior, BuildingType.boutique_interior_alt)
                    elif entry == LogEntryType.wings_cut_scene_4:
                        street.replace_building_type(BuildingType.sewer, BuildingType.sewer_winged)
                    elif entry == LogEntryType.wings_cut_scene_5:
                        street.replace_building_type(BuildingType.sewer_winged, BuildingType.sewer_light_winged)
                    elif entry == LogEntryType.end_cut_scene_A:
                        street.replace_building_type(BuildingType.hospital_room, BuildingType.hospital_room_start)
                        mc.x = 17
                        mc.y = 5

                    cut_scene_index += 1
                cut_scene_continue = False
            else:
                alley_down_name = ""
                alley_up_name = ""
                new_street = None
                for alley in street.get_alleys():
                    if alley.box.colliderect(mc.body_box):
                        alley_down_name = alley.down_name if alley.down_street_type != StreetType._back else street_stack[-1][0].name
                        alley_up_name = alley.up_name
                        if alley_down and alley.down_street_type:
                            new_street = alley.get_down_street()
                            break
                        elif alley_up and alley.up_street_type:
                            new_street = alley.get_up_street()
                            break
                alley_up = False
                alley_down = False
                if new_street:
                    if new_street.is_backstreet:
                        street, (mc.x, mc.y) = street_stack.pop()
                    elif new_street.inside:
                        street_stack.append((street, (mc.x, mc.y)))
                        street = new_street
                        if new_street.entry_x:
                            mc.x = new_street.entry_x
                        if new_street.entry_y:
                            mc.y = new_street.entry_y
                    else:
                        street = new_street

                    # Mission stuff
                    if curr_phase.value <= MissionPhase.wings_2.value:
                        if street.street_type == StreetType.residential_stairs_interior_apt and curr_phase.value > MissionPhase.bad_news_2.value:
                            street.replace_building_type(BuildingType.residential_stairs_interior_apt, BuildingType.residential_stairs_interior_apt_2)
                        if street.street_type == StreetType.ocean_drive and curr_phase.value > MissionPhase.bad_news_2.value:
                            street.replace_building_type(BuildingType.residential_stairs, BuildingType.residential_stairs_2)
                    if street.street_type == StreetType.sewer and curr_phase.value > MissionPhase.wings_2.value:
                        street.replace_building_type(BuildingType.sewer, BuildingType.sewer_light_winged)
                    if street.street_type == StreetType.park_lane and curr_phase.value > MissionPhase.wings_1.value:
                        street.replace_building_type(BuildingType.boutique, BuildingType.boutique_alt)
                    if street.street_type == StreetType.boutique_interior and curr_phase.value > MissionPhase.wings_1.value:
                        street.replace_building_type(BuildingType.boutique_interior, BuildingType.boutique_interior_alt)

                interaction_log_lambda = None
                for i in street.interactions():
                    if i[0].colliderect(mc.body_box):
                        interaction_log_lambda = i[1]

                mc.move()

                if mc.x < street.min_x:
                    mc.x = street.min_x
                    mc.x_move = 0
                    if street.left_message:
                        log.log(street.left_message)
                if mc.x > street.max_x - 6:
                    mc.x = street.max_x - 6
                    mc.x_move = 0
                    if street.right_message:
                        log.log(street.right_message)

                collided = False
                mc.has_jump = False
                for platform in street.platforms():
                    if platform.colliderect(mc.foot_box) and mc.y_move >= 0:
                        mc.y_move = 0
                        mc.y = platform.y - 10
                        collided = True
                        mc.has_jump = True
                        break
                for ceiling in street.ceilings():
                    if ceiling.colliderect(mc.head_box) and mc.y_move < 0:
                        mc.y_move = 0
                        mc.y = ceiling.y + ceiling.height
                        break
                if not collided:
                    mc.y_move += 0.1
                    mc.y_move = min(mc.y_move, 2.4)

                if frame % 20 == 0:
                    mc.transition()
                    # print(mc.x, mc.y)
                    # print(clock.get_fps())

            # Draw
            screen.fill(street.background_color)

            # platform_x - player_x + mc_visual_x
            mc_rel = (mc_loc[0] - 10 * mc.x, mc_loc[1] - 10 * mc.y)

            if street.bg_street.bg_street:
                for building in street.bg_street.bg_street.buildings:
                    if building.silhouette:
                        pygame.draw.rect(screen, (30, 30, 30), scale_x(building.visual_box, 1.0, (mc.x, mc.y), mc_loc))
            for building in street.bg_street.buildings:
                if building.silhouette:
                    pygame.draw.rect(screen, (50, 50, 50), scale_x(building.visual_box, 1.0, (mc.x, mc.y), mc_loc))

            for building in street.buildings:
                screen.blit(BuildingTextures.get(building.building_type), building.visual_loc(mc_rel))

            # for platform in street.platforms():
                # p = platform.copy()
                # p.x *= 10
                # p.y *= 10
                # p.width *= 10
                # p.height *= 10
                # p.move_ip(mc_rel)
                # pygame.draw.rect(screen, (100, 100, 100), p)

            # for alley in street.get_alleys():
                # p = alley.box.copy()
                # p.x *= 10
                # p.y *= 10
                # p.width *= 10
                # p.height *= 10
                # p.move_ip(mc_rel)
                # pygame.draw.rect(screen, (0, 74, 127), p)

            screen.blit(CharacterTextures.get(mc.state), mc_loc)

            # y = text_y
            # for text in log.get_active_text():
                # # pygame.draw.rect(screen, (0, 0, 0), (4, y, t.get_width(), t.get_height()))
                # font.render_to(screen, (4, y), text, (255, 255, 255), bgcolor=(0, 148, 255))
                # y -= text_size

            # y = text_y
            # if opening_screen:
                # t = font.render("(Any key to continue)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
                # t = font.render("Move (A/Left, D/Right)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
                # t = font.render("Jump (Space)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
                # t = font.render("Interact (E)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
                # t = font.render("Change streets (W/Up, S/Down)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
            # elif cut_scene:
                # t = font.render("(Any key)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
            # if interaction_log_lambda:
                # t = font.render("Interact (E)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
            # if alley_down_name:
                # t = font.render(alley_down_name + " (S/Down)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size
            # if alley_up_name:
                # t = font.render(alley_up_name + " (W/Up)", (255, 255, 255), bgcolor=(0, 148, 255))[0]
                # screen.blit(t, (1200 - t.get_width() - 4, y))
                # y -= text_size

            if opening_screen:
                screen.blit(opening_graphic, (0, 50))
            # else:
                # font.render_to(screen, (4, 4), street.name, (255, 255, 255), bgcolor=(0, 148, 255))
            
            pygame.display.flip()

            clock.tick(120)
            frame = (frame + 1) % 120
            await asyncio.sleep(0)

asyncio.run(Game.run())
    # draw_street(Street.get_street_by_type(StreetType.main_street), "ms.png")
    # draw_street(Street.get_street_by_type(StreetType.park_lane), "pl.png")
    # draw_street(Street.get_street_by_type(StreetType.ocean_drive), "od.png")








