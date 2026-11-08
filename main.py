import pygame
import time
import random
import pickle
import easygui
import os

# 将当前工作目录强制切换为该文件所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

clock = pygame.time.Clock()
running = True
now_version = 0.1
now_screen = 0 # 0: 主菜单 1: 游戏 2: 设置 3: 关于
level = 1
map = [0,[],[0,0,0],[0,0],[],[]] 
# map[关卡编号（0），
# [出生点x,出生点y]（1），
# [背景颜色RGB]（2），
# [终点x,终点y]（3），
# [
# [障碍物1起始x,障碍物1起始y,障碍物1终点x,障碍物1终点y]，其他障碍物
# ]（4）
# [
# [陷阱1起始x,陷阱1起始y,陷阱1终点x,陷阱1终点y]，其他陷阱]
# ]（5）
#
# ]
# """
playerx = 0
playery = 0




# 修复了缩进问题，放在全局
font_path = "C:/Windows/Fonts/msyh.ttc" # 确保这个路径在你的电脑上存在
font_title = pygame.font.Font(font_path, 80) 
font_menu = pygame.font.Font(font_path, 40)
font_small = pygame.font.Font(font_path, 20)

# 声明为全局变量，以便主循环能获取按钮的坐标进行点击判定
menu_rects = {} 
# 玩家的真实坐标和物理属性（使用 pygame.Rect 方便做碰撞检测）
player_rect = pygame.Rect(0, 0, 20, 20) 
player_speed_y = 0

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
        log("Map loaded successfully.")
    except FileNotFoundError:
        log(f"{mapname} not found.")
        return 1
    

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
# 全局变量区加一个记录跳跃状态的变量（放在 menu_rects = {} 下面）
player_speed_y = 0
is_on_ground = False

def player_jump():
    global player_speed_y, is_on_ground
    # 只有在踩在地面上时才能跳
    if is_on_ground:
        player_speed_y = -16  # 跳跃高度
        is_on_ground = False

def game_screen():
    global level, screen, now_screen, running, map, player_rect, player_speed_y, is_on_ground
    
    # 1. 关卡加载与初始化
    if level != map[0]:
        lm_rt = load_map(int(level))
        if lm_rt == 1:
            now_screen = 0
            return
        # 初始化出生点
        player_rect.x = map[1][0]
        player_rect.y = map[1][1]
        player_speed_y = 0 

    # 2. 绘制背景
    backcolor = map[2]
    screen.fill((backcolor[0], backcolor[1], backcolor[2])) 
    
    # 3. 物理运动逻辑（左右移动 + 边界限制）
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
        player_rect.x -= 5
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
        player_rect.x += 5
        
    # 【核心修复】强行限制 X 坐标，绝对不允许跑出屏幕左右边界
    if player_rect.left < 0: player_rect.left = 0
    if player_rect.right > 1000: player_rect.right = 1000

    # 重力计算
    player_speed_y += 1
    if player_speed_y > 15: player_speed_y = 15
    if keys[pygame.K_s]: player_speed_y += 2  # 按S加速下落
    player_rect.y += player_speed_y

    # 4. 绘制地图元素并进行碰撞检测
    is_on_ground = False  # 每帧先重置落地状态

    # 画终点 (绿色)
    goal_rect = pygame.Rect(map[3][0], map[3][1], 20, 40)
    pygame.draw.rect(screen, (0, 255, 0), goal_rect)
    
    # 画障碍物 (黑色)
    for obs in map[4]:
        obs_rect = pygame.Rect(obs[0], obs[1], obs[2]-obs[0], obs[3]-obs[1])
        pygame.draw.rect(screen, (0, 0, 0), obs_rect)
        
        if player_rect.colliderect(obs_rect):
            # 如果正在下落（速度为正值）且碰到了方块顶部
            if player_speed_y > 0 and player_rect.bottom - player_speed_y <= obs_rect.top + 5:
                player_rect.bottom = obs_rect.top
                player_speed_y = 0
                is_on_ground = True
                
    # 画陷阱 (红色)
    for trap in map[5]:
        trap_rect = pygame.Rect(trap[0], trap[1], trap[2]-trap[0], trap[3]-trap[1])
        pygame.draw.rect(screen, (255, 0, 0), trap_rect)
        
        if player_rect.colliderect(trap_rect):
            # 碰到陷阱回出生点
            player_rect.x = map[1][0] 
            player_rect.y = map[1][1]
            player_speed_y = 0

    # 5. 绘制玩家 (蓝色)
    pygame.draw.rect(screen, (0, 0, 255), player_rect)

    # 6. 掉出世界底部的死亡检测
    if player_rect.top > 600:
        player_rect.x = map[1][0]
        player_rect.y = map[1][1]
        player_speed_y = 0

    # 7. 胜利检测
    if player_rect.colliderect(goal_rect):
        level += 1
        save_data()
        map[0] = -1 # 下一帧自动加载新地图
    
    # 8. 绘制 UI 文字
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
        
                # 键盘事件处理
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and now_screen != 0:
                now_screen = 0
            # 【新增】如果在游戏界面，按 W/空格/↑ 触发跳跃
            elif now_screen == 1:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    player_jump()

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
    clock.tick(60) 

pygame.quit()