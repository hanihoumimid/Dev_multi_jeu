import pygame
import random
import os

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu de l'aligot")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Chargement des images
img_path = "img"
aligot_img = pygame.image.load(os.path.join(img_path, "aligot.png"))
fraise_img = pygame.image.load(os.path.join(img_path, "fraise.png"))
pomme_img = pygame.image.load(os.path.join(img_path, "pomme.png"))
mangue_img = pygame.image.load(os.path.join(img_path, "mangue.png"))
citron_img = pygame.image.load(os.path.join(img_path, "citron.png"))

# Redimensionnement des images
aligot_img = pygame.transform.scale(aligot_img, (50, 50))
fraise_img = pygame.transform.scale(fraise_img, (40, 40))
pomme_img = pygame.transform.scale(pomme_img, (40, 40))
mangue_img = pygame.transform.scale(mangue_img, (40, 40))
citron_img = pygame.transform.scale(citron_img, (40, 40))

# Police et variables
font = pygame.font.Font(None, 36)
score = 0
time_limit = 60  # Durée en secondes
clock = pygame.time.Clock()
start_ticks = None 


text_color = BLACK  


fruits = [
    {"image": fraise_img, "score": 2, "color": (255, 0, 0)},
    {"image": pomme_img, "score": 4, "color": (0, 255, 0)},
    {"image": mangue_img, "score": 6, "color": (255, 165, 0)},
    {"image": citron_img, "score": 10, "color": (255, 255, 0)},
]

# Générer des positions aléatoires pour les fruits
def generate_fruit():
    fruit = random.choice(fruits)
    x = random.randint(50, WINDOW_WIDTH - 50)
    y = random.randint(50, WINDOW_HEIGHT - 50)
    return {"fruit": fruit, "pos": (x, y)}

# Initialisation des fruits
fruit_objects = [generate_fruit() for _ in range(5)]

# Position initiale de l'aligot
aligot_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
aligot_speed = 5

# Fonction pour afficher le score
def draw_score():
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (WINDOW_WIDTH - 150, 10))

# Fonction pour afficher le timer
def draw_timer():
    if start_ticks is not None:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, time_limit - elapsed_time)
        timer_text = font.render(f"Time: {remaining_time}s", True, text_color)
        screen.blit(timer_text, (10, 10))
        return remaining_time
    else:
        timer_text = font.render(f"Time: {time_limit}s", True, text_color)
        screen.blit(timer_text, (10, 10))
        return time_limit

# Boucle principale
running = True
background_color = WHITE

while running:
    screen.fill(background_color)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_UP]:
        aligot_pos[1] -= aligot_speed
        moved = True
    if keys[pygame.K_DOWN]:
        aligot_pos[1] += aligot_speed
        moved = True
    if keys[pygame.K_LEFT]:
        aligot_pos[0] -= aligot_speed
        moved = True
    if keys[pygame.K_RIGHT]:
        aligot_pos[0] += aligot_speed
        moved = True


    if moved and start_ticks is None:
        start_ticks = pygame.time.get_ticks()
        text_color = BLACK  

    aligot_pos[0] = max(0, min(WINDOW_WIDTH - 50, aligot_pos[0]))
    aligot_pos[1] = max(0, min(WINDOW_HEIGHT - 50, aligot_pos[1]))

    screen.blit(aligot_img, aligot_pos)

    for obj in fruit_objects:
        screen.blit(obj["fruit"]["image"], obj["pos"])

    # Collision avec les fruits
    aligot_rect = pygame.Rect(aligot_pos[0], aligot_pos[1], 50, 50)
    for obj in fruit_objects:
        fruit_rect = pygame.Rect(obj["pos"][0], obj["pos"][1], 40, 40)
        if aligot_rect.colliderect(fruit_rect):
            score += obj["fruit"]["score"]
            background_color = obj["fruit"]["color"]
            fruit_objects.remove(obj)
            fruit_objects.append(generate_fruit())

    draw_score()
    remaining_time = draw_timer()

    # Fin du jeu après le temps imparti
    if remaining_time <= 0:
        running = False

    pygame.display.flip()
    clock.tick(30)

# Affichage du score final
screen.fill(BLACK)
final_score_text = font.render(f"Score final : {score}", True, WHITE)
screen.blit(final_score_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
