import pygame
import time
import random
pygame.init()

running = True
now_version = 0.1
now_screen = 0 #0: main menu 1: game 2: settings 3: about\
level = 1
font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 100) 
def log(message):
    with open("log.txt", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")
def getin_data():
    global level
    log("Now I'm in getin_data()")
    try:
        with open("data.txt", "r") as f:
            data = f.read().splitlines()
            level = float(data[0])
        log(f"Data retrieved successfully: level = {level}")
    except FileNotFoundError:
        log("data.txt not found. Creating a new one with default level.")
        with open("data.txt", "w") as f:
            f.write(str(level))
        log("data.txt created with default level.")

def save_data():
    global level
    log("Now I'm in save_data()")
    with open("data.txt", "w") as f:
        f.write(str(level))
    log(f"Data saved successfully: level = {level}")
def main_menu():
    #main menu code here
    global now_screen, level , running,screen,now_version,font
    pygame.display.set_caption(f"方块跑酷 v{now_version} -主菜单")
    screen.fill([68, 200, 249]) 
    screen.blit(font.render("方块跑酷", True, (255, 255, 255)), (300, 50))
    screen.blit(font.render("开始游戏", True, (255, 255, 255)), (400, 200))
    screen.blit(font.render("设置", True, (255, 255, 255)), (400, 300))
    screen.blit(font.render("关于", True, (255, 255, 255)), (400, 400))
    screen.blit(font.render(f"当前关卡: {level}", True, (255, 255, 255)), (10, 10))


    


    
log("Trying to get data from data.txt")
getin_data()
log("Data retrieved successfully.")
log("Starting the game...")
print("Welcome to the game!")
print(level)

log("Trying to open pygame window...")
screen = pygame.display.set_mode((1000, 600))
log("Pygame window opened successfully.")

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if now_screen == 0:
        main_menu()
    
    pygame.display.flip()
pygame.quit()