import pygame
import random
from track import Driver, get_interpolated_position, generate_boot_track

pygame.font.init()

# Initialize drivers with initials, colors, and base speeds
drivers = [
    Driver("HAM", (0, 255, 255), speed=0.0162),  # Lewis Hamilton (Cyan)
    Driver("VER", (75, 0, 130), speed=0.013),  # Max Verstappen (Indigo)
    Driver("LEC", (255, 0, 0), speed=0.015),  # Charles Leclerc (Red)
    Driver("PER", (75, 0, 130), speed=0.01),  # Sergio Perez (Indigo)
    Driver("NOR", (255, 255, 0), speed=0.012),  # Lando Norris (Yellow)
    Driver("ALO", (0, 128, 0), speed=0.011),  # Fernando Alonso (Dark Green)
    Driver("RUS", (0, 255, 255), speed=0.0123),  # George Russell (Cyan)
    Driver("SAI", (255, 0, 0), speed=0.016),  # Carlos Sainz (Red)
    Driver("BOT", (0, 128, 0), speed=0.014),  # Valtteri Bottas (Green)
    Driver("OCO", (255, 105, 180), speed=0.01),  # Esteban Ocon (Pink)
    Driver("MAG", (255, 255, 255), speed=0.0123),  # Kevin Magnussen (White)
    Driver("HUL", (255, 255, 255), speed=0.0118),  # Nico Hülkenberg (White)
    Driver("TSU", (0, 0, 255), speed=0.01),  # Yuki Tsunoda (Blue)
    Driver("LAW", (0, 0, 255), speed=0.01),  # Logan Sargeant (Blue)
    Driver("ALB", (173, 216, 230), speed=0.01),  # Alexander Albon (Light Blue)
    Driver("COL", (173, 216, 230), speed=0.011),  # Franco Colapinto (Light Blue)
    Driver("STO", (0, 128, 0), speed=0.0123),  # Lance Stroll (Dark Green)
    Driver("GAS", (255, 105, 180), speed=0.013),  # Pierre Gasly (Pink)
    Driver("ZHO", (0, 128, 0), speed=0.01),  # Zhou Guanyu (Green)
]

def render_driver(screen, driver, position):
    pygame.draw.circle(screen, driver.color, position, 8)
    font = pygame.font.SysFont(None, 24)
    text = font.render(driver.name, True, (255, 255, 255))
    screen.blit(text, (position[0] - 10, position[1] - 20))

def render_start_finish_line(screen, track):
    """
    Render the start/finish line on the track.
    :param screen: Pygame screen object.
    :param track: The track (list of waypoints).
    """
    start_point = track[0]  # Start/finish line at the first point of the track
    pygame.draw.line(screen, (255, 255, 0), (start_point[0] - 20, start_point[1]), (start_point[0] + 20, start_point[1]), 5)

def render_lap_info(screen, current_lap, total_laps):
    """
    Render current lap and total laps on the right side of the screen.
    :param screen: Pygame screen object.
    :param current_lap: The current lap number.
    :param total_laps: The total number of laps in the race.
    """
    font = pygame.font.SysFont(None, 36)
    lap_info = f"{current_lap}/{total_laps} Laps"
    text = font.render(lap_info, True, (255, 255, 255))
    screen.blit(text, (650, 20))  # Display on the right side

def render_podium(screen, podium):
    """
    Render the final podium celebration.
    :param screen: Pygame screen object.
    :param podium: Top 3 drivers in order of finish.
    """
    font = pygame.font.SysFont(None, 48)
    podium_colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]  # Gold, Silver, Bronze
    title = font.render("Final Podium!", True, (255, 255, 255))
    screen.blit(title, (300, 50))
    for i, driver in enumerate(podium):
        text = font.render(f"{i + 1}. {driver.name}", True, podium_colors[i])
        screen.blit(text, (300, 150 + i * 60))

def render_leaderboard(screen, driver_positions, driver_laps):
    """
    Render the leaderboard showing driver positions and laps.
    :param screen: Pygame screen object.
    :param driver_positions: Dictionary of driver positions.
    :param driver_laps: Dictionary of driver laps.
    """
    font = pygame.font.SysFont(None, 20)
    sorted_drivers = sorted(drivers, key=lambda d: (-driver_laps[d], -driver_positions[d]))
    for i, driver in enumerate(sorted_drivers):
        text = font.render(f"{i + 1}. {driver.name} - Lap {driver_laps[driver]}", True, (255, 255, 255))
        screen.blit(text, (20, 20 + i * 14))  # Display on the left side


def simulation():
    pygame.init()
    screen = pygame.display.set_mode((900, 800))
    pygame.display.set_caption("F1 Race Simulation")
    clock = pygame.time.Clock()

    track = generate_boot_track(screen.get_width(), screen.get_height())
    driver_positions = {driver: 0 for driver in drivers}
    driver_laps = {driver: 0 for driver in drivers}
    current_lap = 1
    final_lap = 5
    race_finished = False
    podium = []

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not race_finished:
            # Simulate driver movements
            for driver in drivers:
                speed_multiplier = random.uniform(0.8, 1.2)
                if random.random() < 0.03:
                    speed_multiplier *= 0.7

                current_pos = driver_positions[driver]
                next_pos = (current_pos + driver.speed * speed_multiplier) % len(track)
                driver_positions[driver] = next_pos

                if next_pos < current_pos:
                    driver_laps[driver] += 1

            # Update current lap
            leading_driver = max(driver_laps, key=driver_laps.get)
            current_lap = driver_laps[leading_driver] + 1

            # End the race if a driver finishes the final lap
            if driver_laps[leading_driver] >= final_lap:
                race_finished = True
                podium = sorted(drivers, key=lambda d: (-driver_laps[d], -driver_positions[d]))[:3]

        # Render track
        for i in range(len(track) - 1):
            pygame.draw.line(screen, (255, 255, 255), track[i], track[i + 1], 3)
        pygame.draw.line(screen, (255, 255, 255), track[-1], track[0], 3)

        # Render start/finish line
        render_start_finish_line(screen, track)

        # Render lap info
        render_lap_info(screen, current_lap, final_lap)

        # Render drivers
        for driver in drivers:
            current_pos = driver_positions[driver]
            position = get_interpolated_position(track, current_pos / len(track))
            render_driver(screen, driver, position)

        # Render leaderboard
        render_leaderboard(screen, driver_positions, driver_laps)

        # Render podium if race is finished
        if race_finished:
            render_podium(screen, podium)

        pygame.display.flip()
        clock.tick(60)

simulation()