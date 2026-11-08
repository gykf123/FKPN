import pygame
import pickle
import time

pygame.init()
UIwindow = pygame.display.set_mode((1000, 600)) # 用你刚才调整的 1000x600
pygame.display.set_caption("方块跑酷 v0.2")
clock = pygame.time.Clock()

# --- 全局变量和字体 ---
running = True
now_screen = 0 # 0: 菜单 1: 游戏
level = 1

font_path = "C:/Windows/Fonts/msyh.ttc"
font_title = pygame.font.Font(font_path, 80)
font_menu = pygame.font.Font(font_path, 40)
font_small = pygame.font.Font(font_path, 20)

# 修复了你旧代码的引用 Bug，起点和角色坐标完全分离
game_running_datas = [] 

# --- 主菜单（用咱们刚优化的版本） ---
menu_rects = {}
def main_menu():
    global now_screen, level, running
    UIwindow.fill((68, 200, 249))
    W, H = UIwindow.get_size()
    WHITE, HOVER = (255, 255, 255), (255, 215, 0)
    TEXT_COLOR = (60, 60, 60)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    title_surf = font_title.render("方块跑酷", True, WHITE)
    UIwindow.blit(title_surf, title_surf.get_rect(center=(W // 2, H // 4 - 20)))

    menu_items = ["开始游戏", "设置", "关于"]
    max_text_width = max(font_menu.size(text)[0] for text in menu_items)
    btn_width = max_text_width + 100
    btn_height = 70
    start_y = H // 2 + 20

    for i, text in enumerate(menu_items):
        text_surf = font_menu.render(text, True, TEXT_COLOR)
        hit_rect = pygame.Rect(0, 0, btn_width, btn_height)
        hit_rect.center = (W // 2, start_y + i * 100)
        
        draw_rect = hit_rect.copy()
        btn_color = WHITE
        
        if hit_rect.collidepoint(mouse_pos):
            btn_color = HOVER
            if mouse_pressed:
                draw_rect = draw_rect.inflate(-10, -10)

        pygame.draw.rect(UIwindow, btn_color, draw_rect, border_radius=btn_height // 2)
        UIwindow.blit(text_surf, text_surf.get_rect(center=draw_rect.center))
        menu_rects[text] = hit_rect

    info_surf = font_small.render(f"当前关卡: {int(level)}", True, WHITE)
    UIwindow.blit(info_surf, (20, 20))


# --- 游戏主界面 ---
# 不再使用像素列表，而是使用 Rect 来代表地面和障碍物
# 这样不仅性能高，而且方便做碰撞
player_rect = pygame.Rect(100, 450, 20, 20)
player_speed_y = 0
is_jumping = False

# 模拟从 map 读取的数据
ground_rects = [
    pygame.Rect(0, 500, 1000, 100), # 底部大地面
    pygame.Rect(300, 400, 150, 20), # 半空台阶
    pygame.Rect(600, 300, 150, 20)  # 半空台阶
]
hazard_rects = [
    pygame.Rect(500, 480, 50, 20)   # 红色销毁物
]
goal_rect = pygame.Rect(900, 450, 30, 50) # 绿色终点

def game_window():
    global now_screen, player_speed_y, is_jumping
    
    UIwindow.fill((51, 153, 255)) # 背景
    
    # --- 物理逻辑 ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
        
    # 重力系统
    player_speed_y += 1 # 重力加速度
    if player_speed_y > 15: 
        player_speed_y = 15 # 终端速度限制
    player_rect.y += player_speed_y
    
    # --- 碰撞检测 ---
    # 默认没有落地
    on_ground = False
    
    # 检测是否落地（只检测和地面的碰撞）
    for ground in ground_rects:
        if player_rect.colliderect(ground):
            if player_speed_y > 0: # 下落时碰到地面
                player_rect.bottom = ground.top
                player_speed_y = 0
                on_ground = True
                
    # 出界掉落
    if player_rect.top > 600:
        player_rect.x, player_rect.y = 100, 450
        player_speed_y = 0

    # --- 事件处理（跳跃） ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and on_ground:
                player_speed_y = -15 # 给一个向上的初速度
            if event.key == pygame.K_ESCAPE:
                now_screen = 0 # 回菜单

    # --- 渲染 ---
    for ground in ground_rects:
        pygame.draw.rect(UIwindow, (0, 0, 0), ground)
    for hazard in hazard_rects:
        pygame.draw.rect(UIwindow, (255, 0, 0), hazard)
    pygame.draw.rect(UIwindow, (0, 255, 0), goal_rect)
    
    pygame.draw.rect(UIwindow, (0, 0, 255), player_rect) # 绘制玩家
    
    # 关卡文字
    text_surf = font_menu.render(f"关卡 {level}", True, (200, 200, 200))
    UIwindow.blit(text_surf, (20, 20))

# --- 主循环 ---
while running:
    # 先处理退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # 菜单点击事件
        if now_screen == 0 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu_rects["开始游戏"].collidepoint(event.pos):
                now_screen = 1
                level = 1

    # 渲染对应窗口
    if now_screen == 0:
        main_menu()
    elif now_screen == 1:
        game_window()

    pygame.display.flip()
    clock.tick(60) # 锁定 60 帧

pygame.quit()