import pygame
import random

# pygame setup
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width(), screen.get_height()) / 2

# Cargar el dragón UNA sola vez (no dentro del while loop, es carísimo hacerlo cada frame)
dragon = pygame.image.load("dragon.png").convert_alpha()
scaled_dragon = pygame.transform.scale(
    dragon, (int(dragon.get_width() * 0.2), int(dragon.get_height() * 0.2))
)
dragon_half_w = scaled_dragon.get_width() // 2
dragon_half_h = scaled_dragon.get_height() // 2

# Sky (fondo)
sky_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
sky_img.fill((135, 206, 235))  # Sky Blue

# --- Nubes: lista de nubes individuales que caen de arriba hacia abajo ---
class Cloud:
    def __init__(self):
        self.reset(initial=True)

    def reset(self, initial=False):
        self.x = random.randint(0, SCREEN_WIDTH)
        # Si es la primera vez, repartirlas en toda la pantalla;
        # si no, que aparezcan arriba (fuera de pantalla) para "caer"
        self.y = random.randint(0, SCREEN_HEIGHT) if initial else random.randint(-200, -60)
        self.speed = random.uniform(40, 100)  # px/seg
        self.scale = random.uniform(0.6, 1.2)

    def update(self, dt):
        self.y += self.speed * dt
        if self.y > SCREEN_HEIGHT + 60:
            self.reset()

    def draw(self, surface):
        s = self.scale
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), int(60 * s))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x + 50 * s), int(self.y + 20 * s)), int(50 * s))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x - 50 * s), int(self.y + 20 * s)), int(50 * s))


clouds = [Cloud() for _ in range(6)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Fondo ---
    screen.blit(sky_img, (0, 0))

    # --- Nubes cayendo ---
    for cloud in clouds:
        cloud.update(dt)
        cloud.draw(screen)

    # --- Movimiento del dragón ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 600 * dt
    if keys[pygame.K_s]:
        player_pos.y += 600 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 600 * dt
    if keys[pygame.K_d]:
        player_pos.x += 600 * dt

    # --- Limitar al dragón para que no se salga de la pantalla (ni "bajo la superficie") ---
    player_pos.x = max(dragon_half_w, min(SCREEN_WIDTH - dragon_half_w, player_pos.x))
    player_pos.y = max(dragon_half_h, min(SCREEN_HEIGHT - dragon_half_h, player_pos.y))

    # --- Dibujar dragón ---
    screen.blit(scaled_dragon, (player_pos.x - dragon_half_w, player_pos.y - dragon_half_h))

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()