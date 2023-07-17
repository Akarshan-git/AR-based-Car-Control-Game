import cv2
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Define screen size
screen_width = 1920
screen_height = 1080

# Create Pygame screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up camera
camera = cv2.VideoCapture(0)

# Load car image
car_image = pygame.image.load('car.png')

# Define marker pattern
marker_pattern = np.array([[0, 0], [0, 50], [50, 50], [50, 0]])

# Define car position and movement speed
car_x = screen_width // 2
car_y = screen_height // 2
car_speed = 2

# Define background images
start_image = pygame.image.load('start.png')
background_image = pygame.image.load('background.png')
game_over_image = pygame.image.load('game_over.png')

# Game loop
game_over = False
game_started = False
while not game_over:
    if not game_started:
        # Show start game screen
        screen.blit(start_image, (0, 0))
        pygame.display.flip()
        # Wait for user to start game
        while not game_started:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_started = True
                if event.type == pygame.QUIT:
                    game_over = True
                    game_started = True
                    break
    else:
        # Read video stream from camera
        ret, frame = camera.read()

        # Convert video frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect marker pattern in grayscale frame
        corners = cv2.goodFeaturesToTrack(gray, 4, 0.01, 10)
        if corners is not None:
            # Extract marker pattern coordinates
            corners = np.int0(corners)
            marker = corners[0].reshape(-1, 2)

            # Draw marker pattern on video frame
            cv2.polylines(frame, [corners], True, (0, 255, 0), 2)

            # Control car movement with marker pattern
            if marker[0][0] < screen_width // 3:
                car_x -= car_speed
            elif marker[0][0] > 2 * screen_width // 3:
                car_x += car_speed
            if marker[0][1] < screen_height // 3:
                car_y -= car_speed
            elif marker[0][1] > 2 * screen_height // 3:
                car_y += car_speed

            # Blit background image onto screen
            screen.blit(background_image, (0, 0))

            # Update car position on screen
            screen.blit(car_image, (car_x, car_y))

            # Display screen
            pygame.display.flip()

        # Check for game over event
        if car_x < 0 or car_x > screen_width or car_y < 0 or car_y > screen_height:
            game_over = True
        # Check for restart event
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_over = False
                car_x = screen_width // 2
                car_y = screen_height // 2
                break
            if event.type == pygame.QUIT:
                game_over = True

# Show game over screen
screen.blit(game_over_image, (0, 0))
pygame.display.flip()
# Wait
