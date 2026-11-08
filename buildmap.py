import pickle
import os

class MapBuilder:
    """关卡构建器，用于快速、安全地生成地图数据"""
    def __init__(self, level_num, bg_color, spawn_x=50, spawn_y=500):
        self.level_num = level_num
        self.bg_color = bg_color
        self.spawn_point = [spawn_x, spawn_y]
        self.goal_point = [900, 500]
        self.grounds = []
        self.traps = []

    def add_ground(self, x1, y1, x2, y2):
        """添加地面/平台 [起点x, 起点y, 终点x, 终点y]"""
        self.grounds.append([x1, y1, x2, y2])

    def add_trap(self, x1, y1, x2, y2):
        """添加陷阱/岩浆"""
        self.traps.append([x1, y1, x2, y2])

    def set_goal(self, x, ground_y):
        """设置终点，自动将其贴在地面正上方(防止卡进方块里)"""
        # 玩家高度是 20，终点高度 40。让它站在地面上
        self.goal_point = [x, ground_y - 40]

    def save(self):
        """打包并保存为 pkl 文件"""
        # 严格按照 main.py 要求的数据结构组装
        map_data = [
            self.level_num,
            self.spawn_point,
            self.bg_color,
            self.goal_point,
            self.grounds,
            self.traps
        ]
        filename = f"map{self.level_num}.pkl"
        with open(filename, "wb") as f:
            pickle.dump(map_data, f)
        print(f"[成功] 生成关卡 {self.level_num}: {filename} (平台:{len(self.grounds)} 陷阱:{len(self.traps)})")


def generate_all_maps():
    print("开始生成地图...")

    # ==========================================
    # 关卡 1：新手起步（平地，熟悉移动）
    # ==========================================
    m1 = MapBuilder(1, [100, 180, 255], spawn_x=50, spawn_y=500)
    m1.add_ground(0, 550, 1000, 600)  # 一整块大平地
    m1.set_goal(900, 550)
    m1.save()

    # ==========================================
    # 关卡 2：小试牛刀（跨越鸿沟，避开岩浆）
    # ==========================================
    m2 = MapBuilder(2, [50, 150, 100], spawn_x=50, spawn_y=450)
    # 平台
    m2.add_ground(0, 500, 300, 600)     # 起步台 (高度 500)
    m2.add_ground(420, 480, 650, 600)   # 中间台 (高度 480)
    m2.add_ground(750, 550, 1000, 600)  # 终点台 (高度 550)
    # 陷阱（全铺在坑底）
    m2.add_trap(300, 550, 420, 600)     # 坑1岩浆
    m2.add_trap(650, 550, 750, 600)     # 坑2岩浆
    m2.add_trap(500, 450, 550, 480)     # 中间台上的尖刺
    m2.set_goal(900, 550)               # 终点在最后的平台上
    m2.save()

    # ==========================================
    # 关卡 3：步步高升（跳跃阶梯，考验连跳）
    # ==========================================
    m3 = MapBuilder(3, [200, 150, 100], spawn_x=50, spawn_y=500)
    # 阶梯状平台，每层抬高 60 像素，完全在跳跃能力内
    m3.add_ground(0, 550, 200, 600)     # 起步
    m3.add_ground(250, 500, 350, 600)
    m3.add_ground(400, 440, 500, 600)
    m3.add_ground(550, 380, 650, 600)
    m3.add_ground(700, 320, 1000, 600)  # 终点大平台
    # 底下铺满岩浆
    m3.add_trap(200, 550, 250, 600)
    m3.add_trap(350, 550, 400, 600)
    m3.add_trap(500, 550, 550, 600)
    m3.add_trap(650, 550, 700, 600)
    m3.set_goal(850, 320)               # 放在最高处的平台上
    m3.save()

    # ==========================================
    # 关卡 4：终极挑战（垂直攀爬 + 密集陷阱）
    # ==========================================
    m4 = MapBuilder(4, [100, 100, 150], spawn_x=50, spawn_y=500)
    # 底部地面
    m4.add_ground(0, 550, 1000, 600)
    # 垂直攀爬悬浮台（高度差 80 左右）
    m4.add_ground(200, 470, 300, 500)
    m4.add_ground(380, 390, 480, 420)
    m4.add_ground(560, 310, 660, 340)
    m4.add_ground(750, 230, 1000, 260)  # 最顶部的终点平台
    # 底部岩浆池
    m4.add_trap(100, 550, 300, 600)
    m4.add_trap(350, 550, 500, 600)
    m4.add_trap(550, 550, 700, 600)
    m4.add_trap(750, 550, 1000, 600)
    # 悬浮台边角上的干扰陷阱
    m4.add_trap(430, 370, 480, 390)
    m4.add_trap(610, 290, 660, 310)
    m4.set_goal(850, 230)               # 放在最高处平台上
    m4.save()

    print("所有地图生成完毕！可以直接运行 main.py 测试了。")


if __name__ == "__main__":
    generate_all_maps()