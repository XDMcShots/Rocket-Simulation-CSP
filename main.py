import pygame
import math
import time

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vinegar–Baking Soda Rocket Simulation")
clock = pygame.time.Clock()
FPS = 60

# ------------------- Constants -------------------
# Chemistry inputs

vinegar_conc = 0.08  # mol/L
vinegar_volume = 0.1  # L
moles_acid = vinegar_conc * vinegar_volume

mass_nahco3 = 1.68  # g
molar_mass_nahco3 = 84.01
moles_nahco3 = mass_nahco3 / molar_mass_nahco3  # ≈ 0.02 mol
nahco3_conc = moles_nahco3 / vinegar_volume     # vinegar_volume = 0.1 L → 0.2 mol/L

vinegar_to_baking_ratio = vinegar_conc / nahco3_conc


"""
0.1 L for all solution Volume
 
"""
moles_co2 = min(moles_nahco3, moles_acid)

# Gas law
R = 8.314  # J/mol·K
T = 298  # K
bottle_volume = 0.0005  # m³
pressure = (moles_co2 * R * T) / bottle_volume  # in Pascals (N/m²)

# Thrust force
nozzle_radius = 0.013  # m
nozzle_area = math.pi * nozzle_radius**2
force = pressure * nozzle_area  # in Newtons

# Rocket physics
rocket_mass = 0.16507  # kg
distance = 0.1  # m
initial_velocity = math.sqrt((2 * force * distance) / rocket_mass)

# Motion setup
angle_deg = 45
angle_rad = math.radians(angle_deg)
vx = initial_velocity * math.cos(angle_rad)
vy = initial_velocity * math.sin(angle_rad)

# Gravity
g = 9.81  # m/s²

# Visual scaling
scale = 100  # 1 meter = 100 pixels
x0, y0 = WIDTH // 2, HEIGHT - 50  # Ground position in pixels

# Rocket image
rocket_img = pygame.Surface((20, 50), pygame.SRCALPHA)
pygame.draw.polygon(rocket_img, (255, 50, 50), [(10, 0), (0, 50), (20, 50)])
rocket_rect = rocket_img.get_rect(center=(x0, y0))

# Start time
start_time = None

# ------------------- Simulation Variables -------------------
max_height = 0
max_range = 0
flight_time = 0

# ------------------- Main Loop -------------------
running = True
flight_active = False
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Restart on spacebar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not flight_active:
                start_time = pygame.time.get_ticks()
                max_height = 0
                max_range = 0
                flight_active = True

    if start_time is None:
        start_time = pygame.time.get_ticks()

    if flight_active:
        t = (pygame.time.get_ticks() - start_time) / 1000  # time in seconds
        flight_time = t

        # Physics: position in meters
        x_m = vx * t
        y_m = vy * t - 0.5 * g * t ** 2

        # Update max values
        max_height = max(max_height, y_m)
        max_range = max(max_range, x_m)

        # Convert to pixels
        x_px = x0 + x_m * scale
        y_px = y0 - y_m * scale

        # Stop if rocket hits ground
        if y_px >= HEIGHT:
            flight_active = False
            y_px = HEIGHT - 50  # Place rocket at ground visually
    else:
        # Freeze rocket position at landing spot
        x_px = x0 + max_range * scale
        y_px = HEIGHT - 50
        t = flight_time

    if y_px >= HEIGHT and flight_active:
        flight_active = False
        y_px = HEIGHT - 50  # visually land on ground
        flight_time = t  # store final time

    # Draw rocket
    rocket_rect.center = (x_px, y_px)
    screen.blit(rocket_img, rocket_rect)

    # UI Text
    font = pygame.font.SysFont('Arial', 18)

    # Chemistry Info
    screen.blit(font.render(f"Vinegar Conc: {vinegar_conc:.2f} mol/L", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Vinegar Vol: {vinegar_volume * 1000:.0f} mL", True, (0, 0, 0)), (10, 30))
    screen.blit(font.render(f"NaHCO3 Mass: {mass_nahco3:.2f} g", True, (0, 0, 0)), (10, 50))
    screen.blit(font.render(f"NaHCO3 Conc: {nahco3_conc:.2f} mol/L", True, (0, 0, 0)), (10, 70))
    screen.blit(font.render(f"Ratio (V:NaHCO3): {vinegar_to_baking_ratio:.2f}", True, (0, 0, 0)), (10, 90))
    screen.blit(font.render(f"Moles CH3COOH: {moles_acid:.4f}", True, (0, 0, 0)), (10, 110))
    screen.blit(font.render(f"Moles NaHCO3: {moles_nahco3:.4f}", True, (0, 0, 0)), (10, 130))
    screen.blit(font.render(f"Moles CO2: {moles_co2:.4f}", True, (0, 0, 0)), (10, 150))

    # Physics Info
    screen.blit(font.render(f"Initial Velocity: {initial_velocity:.2f} m/s", True, (0, 0, 0)), (10, 170))
    screen.blit(font.render(f"Force: {force:.2f} N", True, (0, 0, 0)), (10, 190))
    screen.blit(font.render(f"Flight Time: {t:.2f} s", True, (0, 0, 0)), (10, 210))

    # Flight Info
    if flight_active:
        screen.blit(font.render(f"Current Height: {max(0, y_m):.2f} m", True, (0, 0, 0)), (10, 230))
        screen.blit(font.render(f"Current Range: {x_m:.2f} m", True, (0, 0, 0)), (10, 250))
    else:
        screen.blit(font.render("Flight complete. Press [SPACE] to launch again.", True, (150, 0, 0)), (10, 260))

    # Peak Values
    screen.blit(font.render(f"Max Height: {max_height:.2f} m", True, (0, 0, 0)), (WIDTH - 220, 10))
    screen.blit(font.render(f"Max Range: {max_range:.2f} m", True, (0, 0, 0)), (WIDTH - 220, 30))
    screen.blit(font.render(f"Time Period: {t:.2f} s", True, (0, 0, 0)), (WIDTH - 220, 50))

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
