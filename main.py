import pygame
import time
import random
import pickle
import easygui
import os

# 强制把工作目录锁定为脚本所在目录，防止存档和地图迷路
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

clock = pygame.time.Clock()
running = True
now_version = 0.2  # 版本号更新
now_screen = 0     # 0: 主菜单 1: 游戏 2: 设置 3: 关于
level = 1
map = [0, [], [0, 0, 0], [0, 0], [], []] 

# 玩家物理属性
player_rect = pygame.Rect(0, 0, 20, 20) 
player_speed_y = 0
is_on_ground = False
coyote_timer = 0  # 土狼时间（允许走出版面边缘后的一瞬间还能起跳）

# 字体加载
font_path = "C:/Windows/Fonts/msyh.ttc" # 如果你换了电脑报错，请改成你电脑中文字体的路径
font_title = pygame.font.Font(font_path, 80) 
font_menu = pygame.font.Font(font_path, 40)
font_small = pygame.font.Font(font_path, 20)

menu_rects = {} 

def log(message):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def load_map(l):
    global map
    mapname = f"map{l}.pkl"
    try:
        with open(mapname, "rb") as f:
            map = pickle.load(f)
        log(f"Map {l} loaded successfully.")
    except FileNotFoundError:
        log(f"{mapname} not found.")
        easygui.msgbox(f"地图文件 {mapname} 不存在，游戏将返回主菜单。", title="错误")
        return 1
    return 0

def getin_data():
    global level
    log("Now I'm in getin_data()")
    try:
        with open("data.txt", "r") as f:
            data = f.read().splitlines()
            if data: 
                level = float(data[0])
                # 防呆设计：如果数据小于 1，强行重置为第 1 关
                if level < 1:
                    level = 1
        log(f"Data retrieved successfully: level = {level}")
    except FileNotFoundError:
        log("data.txt not found. Creating a new one with default level.")
        with open("data.txt", "w") as f:
            f.write(str(level))

def save_data():
    global level
    log("Now I'm in save_data()")
    with open("data.txt", "w") as f:
        f.write(str(level))
    log(f"Data saved successfully: level = {level}")

def main_menu():
    global now_screen, level, running, screen, now_version, menu_rects
    
    pygame.display.set_caption(f"方块跑酷 v{now_version} - 主菜单")
    screen.fill((68, 200, 249)) 
    
    W, H = screen.get_size()
    WHITE = (255, 255, 255)
    HOVER_COLOR = (255, 215, 0)  
    TEXT_COLOR = (60, 60, 60)    

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # 1. 标题
    title_surf = font_title.render("方块跑酷", True, WHITE)
    title_rect = title_surf.get_rect(center=(W // 2, H // 4 - 20)) 
    screen.blit(title_surf, title_rect)

    # 2. 菜单项
    menu_items = ["开始游戏", "设置", "关于"]
    max_text_width = max(font_menu.size(text)[0] for text in menu_items)
    btn_width = max_text_width + 100  
    btn_height = 70                   
    
    start_y = H // 2 + 20  
    gap = 100              
    
    for i, text in enumerate(menu_items):
        text_surf = font_menu.render(text, True, TEXT_COLOR)
        hit_rect = pygame.Rect(0, 0, btn_width, btn_height)
        hit_rect.center = (W // 2, start_y + i * gap)
        
        draw_rect = hit_rect.copy()
        btn_color = WHITE
        
        if hit_rect.collidepoint(mouse_pos):
            btn_color = HOVER_COLOR
            if mouse_pressed:
                draw_rect = draw_rect.inflate(-10, -10) # 点击缩小

        pygame.draw.rect(screen, btn_color, draw_rect, border_radius=btn_height // 2)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        screen.blit(text_surf, text_rect)
        menu_rects[text] = hit_rect 

    # 3. 关卡信息
    info_surf = font_small.render(f"当前关卡: {int(level)} (按 R 重置进度)", True, WHITE)
    screen.blit(info_surf, (20, 20))

def player_jump():
    global player_speed_y, is_on_ground, coyote_timer
    if is_on_ground or coyote_timer > 0:
        player_speed_y = -17  # 跳跃高度
        is_on_ground = False
        coyote_timer = 0      

def game_screen():
    global level, screen, now_screen, running, map, player_rect, player_speed_y, is_on_ground, coyote_timer
    
    # 动态更新窗口标题
    pygame.display.set_caption(f"方块跑酷 v{now_version} - 第 {int(level)} 关")
    
    # 1. 关卡加载
    if level != map[0]:
        lm_rt = load_map(int(level))
        if lm_rt == 1:
            now_screen = 0
            return
        player_rect.x = map[1][0]
        player_rect.y = map[1][1]
        player_speed_y = 0 

    # 2. 绘制背景
    backcolor = map[2]
    screen.fill((backcolor[0], backcolor[1], backcolor[2])) 
    
    # 3. 物理运动（左右移动 + 边界限制）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: player_rect.x -= 6
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: player_rect.x += 6
        
    if player_rect.left < 0: player_rect.left = 0
    if player_rect.right > 1000: player_rect.right = 1000

    # 重力计算
    player_speed_y += 1
    if player_speed_y > 15: player_speed_y = 15
    if keys[pygame.K_s]: player_speed_y += 2  
    player_rect.y += player_speed_y

    # 4. 碰撞检测
    is_on_ground = False  

    # 画终点
    goal_rect = pygame.Rect(map[3][0], map[3][1], 20, 40)
    pygame.draw.rect(screen, (0, 255, 0), goal_rect)
    
    # 画障碍物
    for obs in map[4]:
        obs_rect = pygame.Rect(obs[0], obs[1], obs[2]-obs[0], obs[3]-obs[1])
        pygame.draw.rect(screen, (0, 0, 0), obs_rect)
        
        if player_rect.colliderect(obs_rect):
            if player_speed_y > 0 and player_rect.bottom - player_speed_y <= obs_rect.top + 5:
                player_rect.bottom = obs_rect.top
                player_speed_y = 0
                is_on_ground = True

    # 计算土狼时间
    if is_on_ground:
        coyote_timer = 8
    elif coyote_timer > 0:
        coyote_timer -= 1
                
    # 画陷阱
    for trap in map[5]:
        trap_rect = pygame.Rect(trap[0], trap[1], trap[2]-trap[0], trap[3]-trap[1])
        pygame.draw.rect(screen, (255, 0, 0), trap_rect)
        
        # 陷阱增加 4 像素容错，擦边也算死
        if player_rect.colliderect(trap_rect.inflate(4, 4)):
            player_rect.x = map[1][0] 
            player_rect.y = map[1][1]
            player_speed_y = 0

    # 5. 绘制玩家
    pygame.draw.rect(screen, (0, 0, 255), player_rect)

    # 6. 掉出世界
    if player_rect.top > 600:
        player_rect.x = map[1][0]
        player_rect.y = map[1][1]
        player_speed_y = 0

    # 7. 胜利检测
    if player_rect.colliderect(goal_rect):
        level += 1
        save_data()
        map[0] = -1 
    
    # 8. UI 文字
    texts = [
        ((500,20), font_small.render("游戏进行中... (按ESC返回)", True, (255, 255, 255))),
        ((100,20), font_small.render(f"当前关卡: {int(level)}", True, (255, 255, 255)))
    ]
    for xy, ttext in texts:
        screen.blit(ttext, ttext.get_rect(center=xy))

# ---------------- 游戏入口 ----------------
log("Trying to get data from data.txt")
getin_data()
log("Data retrieved successfully.")
print(f"Welcome to the game! Current level: {level}")

log("Trying to open pygame window...")
screen = pygame.display.set_mode((1000, 600))
log("Pygame window opened successfully.")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data() 
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if now_screen == 0:
                if menu_rects["开始游戏"].collidepoint(event.pos):
                    now_screen = 1
                    log("Game started.")
                elif menu_rects["设置"].collidepoint(event.pos):
                    now_screen = 2
                elif menu_rects["关于"].collidepoint(event.pos):
                    now_screen = 3
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and now_screen != 0:
                now_screen = 0
            
            # 【新增】主菜单按 R 键重置进度
            elif event.key == pygame.K_r and now_screen == 0:
                level = 1
                map[0] = -1 # 让下次进游戏强制加载新地图
                save_data()
                log("Progress reset to level 1.")
                
            # 游戏中跳跃
            elif now_screen == 1:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    player_jump()

    if now_screen == 0:
        main_menu()
    elif now_screen == 1:
        game_screen() 
    elif now_screen == 2:
        screen.fill((100, 100, 100))
    elif now_screen == 3:
        screen.fill((150, 100, 100))
    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()