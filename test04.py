import pygame
import math
import os

# --- Constants ---
WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)
ORANGE = (255, 165, 0)

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Solar System")
font = pygame.font.Font(None, 24)

# --- Celestial Body Class ---
class CelestialBody:
    def __init__(self, name, radius, color, orbit_distance, orbital_period, info_text):
        self.name = name
        self.radius = radius          # display radius (pixels)
        self.color = color
        self.orbit_distance = orbit_distance
        self.orbital_period = orbital_period  # in days (scaled)
        self.info_text = info_text
        self.angle = 0
        self.x = 0
        self.y = 0
        self.is_highlighted = False

    def update_position(self, time_factor):
        if self.orbital_period != 0:
            self.angle += (2 * math.pi / self.orbital_period) * time_factor
        self.x = WIDTH / 2 + self.orbit_distance * math.cos(self.angle)
        self.y = HEIGHT / 2 + self.orbit_distance * math.sin(self.angle)

    def draw(self, screen, center_x, center_y):
        if self.orbit_distance > 0:
            pygame.draw.circle(screen, GRAY, (int(center_x), int(center_y)),
                               int(self.orbit_distance), 1)
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), int(self.radius))
        if self.is_highlighted:
            pygame.draw.circle(screen, LIGHT_GREEN,
                               (int(self.x), int(self.y)),
                               int(self.radius) + 3, 2)
        name_text = font.render(self.name, True, WHITE)
        screen.blit(name_text, (self.x + self.radius + 5, self.y - self.radius))

    def get_info(self):
        return self.info_text

    def is_clicked(self, mouse_pos):
        distance = math.sqrt((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)
        return distance < self.radius

# --- Search & Info UI ---
class SearchBar:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.active = False
        self.text = ""
        self.font = pygame.font.Font(None, 24)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = ORANGE if self.active else GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

class InfoDisplay:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_lines = []
        self.font = pygame.font.Font(None, 24)

    def update_text(self, new_text):
        self.text_lines = new_text.split('\n')

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 30, 30), self.rect, 0)
        pygame.draw.rect(screen, ORANGE, self.rect, 2)
        y_offset = self.rect.y + 10
        for line in self.text_lines:
            text_surface = self.font.render(line, True, WHITE)
            screen.blit(text_surface, (self.rect.x + 10, y_offset))
            y_offset += 25

# --- Simplified Dataset ---
PLANET_DATA = [
    CelestialBody("Sun", 30, YELLOW, 0, 0,
        "Name: Sun\nType: Star\nMass: 1.989e30 kg\nGravity: 274 m/s²\nRadius: 696,340 km\nTemp: 5778 K"),
    CelestialBody("Earth", 9, BLUE, 120, 365,
        "Name: Earth\nType: Planet\nMass: 5.97e24 kg\nGravity: 9.8 m/s²\nRadius: 6,371 km\nHas Life: Yes"),
    CelestialBody("Mars", 6, RED, 180, 687,
        "Name: Mars\nType: Planet\nMass: 6.39e23 kg\nGravity: 3.7 m/s²\nRadius: 3,389 km"),
    CelestialBody("Moon", 4, GRAY, 40, 27,
        "Name: Moon\nType: Moon\nMass: 7.35e22 kg\nGravity: 1.62 m/s²\nRadius: 1,737 km\nOrbits: Earth"),
    CelestialBody("Jupiter", 18, (200,150,100), 260, 4333,
        "Name: Jupiter\nType: Planet\nMass: 1.898e27 kg\nGravity: 24.8 m/s²\nRadius: 69,911 km")
]

SOLAR_SYSTEM = {body.name.lower(): body for body in PLANET_DATA}

# --- Main Loop ---
def main():
    running = True
    clock = pygame.time.Clock()
    time_factor = 0.01  # speed control

    search_bar = SearchBar(50, 50, 200, 40)
    info_display = InfoDisplay(50, 100, 220, 260)
    search_button_rect = pygame.Rect(50, 50 + 40 + 5, 200, 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            search_bar.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if search_button_rect.collidepoint(event.pos):
                    query = search_bar.text.strip().lower()
                    for planet in PLANET_DATA:
                        if planet.name.lower() == query:
                            planet.is_highlighted = True
                            info_display.update_text(planet.get_info())
                        else:
                            planet.is_highlighted = False
                    if query not in SOLAR_SYSTEM:
                        info_display.update_text("Object not found.")
                for planet in PLANET_DATA:
                    if planet.is_clicked(event.pos):
                        info_display.update_text(planet.get_info())
                        for p in PLANET_DATA:
                            p.is_highlighted = (p == planet)

        # Update & Draw
        for body in PLANET_DATA:
            body.update_position(time_factor)
        screen.fill(BLACK)
        sun = SOLAR_SYSTEM["sun"]
        sun.draw(screen, WIDTH / 2, HEIGHT / 2)
        for body in PLANET_DATA[1:]:
            body.draw(screen, WIDTH / 2, HEIGHT / 2)

        search_bar.draw(screen)
        info_display.draw(screen)
        pygame.draw.rect(screen, BLUE, search_button_rect)
        btn_text = font.render("Search", True, WHITE)
        screen.blit(btn_text, (search_button_rect.x + 65, search_button_rect.y + 7))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    os.sys.exit()

if __name__ == "__main__":
    main()
