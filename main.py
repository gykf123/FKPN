import pygame
import time
import random

pygame.init()

running = True
now_version = 0.1
now_screen = 0 # 0: 主菜单 1: 游戏 2: 设置 3: 关于
level = 1

# 修复了缩进问题，放在全局
font_path = "C:/Windows/Fonts/msyh.ttc" # 确保这个路径在你的电脑上存在
font_title = pygame.font.Font(font_path, 80) 
font_menu = pygame.font.Font(font_path, 40)
font_small = pygame.font.Font(font_path, 20)

# 声明为全局变量，以便主循环能获取按钮的坐标进行点击判定
menu_rects = {} 

def log(message):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def getin_data():
    global level
    log("Now I'm in getin_data()")
    try:
        with open("data.txt", "r") as f:
            data = f.read().splitlines()
            if data: # 防止文件为空
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
    global now_screen, level, running, screen, now_version, menu_rects
    
    pygame.display.set_caption(f"方块跑酷 v{now_version} - 主菜单")
    screen.fill((68, 200, 249)) 
    
    W, H = screen.get_size()
    WHITE = (255, 255, 255)
    HOVER_COLOR = (255, 215, 0)  # 悬停黄色
    TEXT_COLOR = (60, 60, 60)    # 深灰色文字

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # 1. 渲染并居中绘制标题 (稍微往上移一点)
    title_surf = font_title.render("方块跑酷", True, WHITE)
    title_rect = title_surf.get_rect(center=(W // 2, H // 4 - 20)) 
    screen.blit(title_surf, title_rect)

    # 2. 渲染并居中绘制菜单项
    menu_items = ["开始游戏", "设置", "关于"]
    
    # 【关键优化】统一按钮宽度和高度
    # 找出所有菜单项中最长文字的宽度，以此作为基准
    max_text_width = max(font_menu.size(text)[0] for text in menu_items)
    btn_width = max_text_width + 100  # 两侧各留 50 像素的边距
    btn_height = 70                   # 固定高度，扁平一点更好看
    
    # 布局参数
    start_y = H // 2 + 20  # 按钮整体起始位置
    gap = 100              # 按钮之间的中心间距
    
    for i, text in enumerate(menu_items):
        # 渲染文字
        text_surf = font_menu.render(text, True, TEXT_COLOR)
        
        # 所有按钮统一大小
        hit_rect = pygame.Rect(0, 0, btn_width, btn_height)
        hit_rect.center = (W // 2, start_y + i * gap)
        
        # 实际绘制的矩形
        draw_rect = hit_rect.copy()
        btn_color = WHITE
        
        # 悬停与点击检测
        if hit_rect.collidepoint(mouse_pos):
            btn_color = HOVER_COLOR
            if mouse_pressed:
                draw_rect = draw_rect.inflate(-10, -10) # 点击缩小

        # 绘制圆角矩形按钮 
        # border_radius 设为高度的一半 (35)，就会变成完美的胶囊/椭圆角
        pygame.draw.rect(screen, btn_color, draw_rect, border_radius=btn_height // 2)
        
        # 文字居中
        text_rect = text_surf.get_rect(center=draw_rect.center)
        screen.blit(text_surf, text_rect)
        
        # 记录点击区域
        menu_rects[text] = hit_rect 

    # 3. 渲染左上角的关卡信息
    info_surf = font_small.render(f"当前关卡: {int(level)}", True, WHITE)
    screen.blit(info_surf, (20, 20))
# ---------------- 其他界面的占位函数 (防止点击后黑屏无反应) ----------------
def game_screen():
    screen.fill((0, 0, 0)) # 游戏背景
    text = font_menu.render("游戏进行中... (按ESC返回)", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(screen.get_width()//2, screen.get_height()//2)))

# ---------------- 游戏入口 ----------------
log("Trying to get data from data.txt")
getin_data()
log("Data retrieved successfully.")
print(f"Welcome to the game! Current level: {level}")

log("Trying to open pygame window...")
screen = pygame.display.set_mode((1000, 600))
log("Pygame window opened successfully.")

while running:
    # 将获取事件的代码放在前面
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data() # 退出前保存数据
            running = False
            
        # 鼠标点击事件处理
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if now_screen == 0: # 如果当前在主菜单
                if menu_rects["开始游戏"].collidepoint(event.pos):
                    now_screen = 1
                    log("Game started.")
                elif menu_rects["设置"].collidepoint(event.pos):
                    now_screen = 2
                    log("Settings opened.")
                elif menu_rects["关于"].collidepoint(event.pos):
                    now_screen = 3
                    log("About opened.")
        
        # 键盘事件处理 (按ESC返回菜单)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and now_screen != 0:
                now_screen = 0

    # 根据状态渲染不同的界面
    if now_screen == 0:
        main_menu()
    elif now_screen == 1:
        game_screen() # 占位符：这里可以换成你写的游戏逻辑函数
    elif now_screen == 2:
        screen.fill((100, 100, 100))
    elif now_screen == 3:
        screen.fill((150, 100, 100))
    
    # 主循环中统一刷新屏幕
    pygame.display.flip()

pygame.quit()