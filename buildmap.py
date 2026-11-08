import pickle
import os

# 强制把工作目录锁定为脚本所在目录，防止地图生成到别的地方
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        self.goal_point = [x, ground_y - 40]

    def save(self):
        """打包并保存为 pkl 文件"""
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
    print("开始生成地图... 共 10 关")

    # ==========================================
    # 关卡 1：新手起步（平地，熟悉移动）
    # ==========================================
    m1 = MapBuilder(1, [100, 180, 255], spawn_x=50, spawn_y=500)
    m1.add_ground(0, 550, 1000, 600)  
    m1.set_goal(900, 550)
    m1.save()

    # ==========================================
    # 关卡 2：小试牛刀（跨越鸿沟，避开岩浆）
    # ==========================================
    m2 = MapBuilder(2, [50, 150, 100], spawn_x=50, spawn_y=450)
    m2.add_ground(0, 500, 300, 600)     
    m2.add_ground(420, 480, 650, 600)   
    m2.add_ground(750, 550, 1000, 600)  
    m2.add_trap(300, 550, 420, 600)     
    m2.add_trap(650, 550, 750, 600)     
    m2.add_trap(500, 450, 550, 480)     
    m2.set_goal(900, 550)               
    m2.save()

    # ==========================================
    # 关卡 3：步步高升（跳跃阶梯，考验连跳）
    # ==========================================
    m3 = MapBuilder(3, [200, 150, 100], spawn_x=50, spawn_y=500)
    m3.add_ground(0, 550, 200, 600)     
    m3.add_ground(250, 500, 350, 600)
    m3.add_ground(400, 440, 500, 600)
    m3.add_ground(550, 380, 650, 600)
    m3.add_ground(700, 320, 1000, 600)  
    m3.add_trap(200, 550, 250, 600)
    m3.add_trap(350, 550, 400, 600)
    m3.add_trap(500, 550, 550, 600)
    m3.add_trap(650, 550, 700, 600)
    m3.set_goal(850, 320)               
    m3.save()

    # ==========================================
    # 关卡 4：垂直攀爬（宽容版，土狼时间主场）
    # ==========================================
    m4 = MapBuilder(4, [100, 100, 150], spawn_x=50, spawn_y=500)
    m4.add_ground(0, 550, 120, 600)     
    m4.add_ground(160, 480, 280, 520)   
    m4.add_ground(320, 410, 440, 450)   
    m4.add_ground(480, 340, 600, 380)   
    m4.add_ground(640, 270, 1000, 310)  
    m4.add_trap(0, 570, 1000, 600)      
    m4.set_goal(850, 270)  
    m4.save()

    # ==========================================
    # 关卡 5：尖刺阵（连续小跳）
    # ==========================================
    m5 = MapBuilder(5, [180, 100, 120], spawn_x=50, spawn_y=500)
    m5.add_ground(0, 550, 1000, 600) # 一马平川，但充满危险
    # 地上的尖刺
    m5.add_trap(200, 530, 250, 550)
    m5.add_trap(350, 530, 450, 550)
    m5.add_trap(550, 530, 600, 550)
    m5.add_trap(700, 530, 800, 550)
    m5.set_goal(900, 550)
    m5.save()

        # ==========================================
    # 关卡 6：勇敢的跨越（修复版，需要助跑）
    # ==========================================
    m6 = MapBuilder(6, [80, 150, 80], spawn_x=50, spawn_y=500)
    m6.add_ground(0, 550, 350, 600)     # 起步台
    m6.add_ground(450, 500, 550, 600)   # 【新增】中间的浮空小岛垫脚石
    m6.add_ground(650, 550, 1000, 600)  # 终点台
    
    # 调整后的岩浆池宽度，全部在跳跃极限内
    m6.add_trap(350, 550, 450, 600)     # 第一段坑
    m6.add_trap(550, 550, 650, 600)     # 第二段坑
    m6.set_goal(900, 550)
    m6.save()

    # ==========================================
    # 关卡 7：高低错落（有起有伏）
    # ==========================================
    m7 = MapBuilder(7, [150, 150, 80], spawn_x=50, spawn_y=500)
    m7.add_ground(0, 550, 200, 600)
    m7.add_ground(280, 450, 450, 500) # 向上跳
    m7.add_ground(530, 350, 700, 400) # 继续向上
    m7.add_ground(780, 500, 1000, 600) # 向下跳
    m7.add_trap(200, 550, 280, 600)
    m7.add_trap(450, 550, 530, 600)
    m7.add_trap(700, 550, 780, 600)
    m7.set_goal(900, 500)
    m7.save()

    # ==========================================
    # 关卡 8：天花板限制（不能跳太高）
    # ==========================================
    m8 = MapBuilder(8, [100, 80, 150], spawn_x=50, spawn_y=500)
    m8.add_ground(0, 550, 250, 600)
    m8.add_ground(350, 450, 600, 500)
    m8.add_ground(700, 550, 1000, 600)
    # 悬浮的黑色天花板，限制跳跃空间
    m8.add_ground(300, 300, 650, 320) 
    m8.add_trap(250, 550, 350, 600)
    m8.add_trap(600, 550, 700, 600)
    m8.set_goal(900, 550)
    m8.save()

    # ==========================================
    # 关卡 9：极限走钢丝（极小平台）
    # ==========================================
    m9 = MapBuilder(9, [150, 80, 80], spawn_x=50, spawn_y=500)
    m9.add_ground(0, 550, 150, 600)
    # 悬浮小方块
    m9.add_ground(250, 500, 300, 520)
    m9.add_ground(400, 450, 450, 470)
    m9.add_ground(550, 400, 600, 420)
    m9.add_ground(700, 450, 750, 470)
    m9.add_ground(850, 550, 1000, 600)
    # 无尽深渊
    m9.add_trap(0, 570, 1000, 600)
    m9.set_goal(900, 550)
    m9.save()

    # ==========================================
    # 关卡 10：终极试炼（融合设计）
    # ==========================================
    m10 = MapBuilder(10, [60, 60, 100], spawn_x=50, spawn_y=500)
    m10.add_ground(0, 550, 150, 600)    # 起点
    m10.add_ground(250, 500, 400, 600)  # 带刺平台1
    m10.add_trap(300, 480, 350, 500)    
    m10.add_ground(500, 420, 650, 600)  # 带刺平台2
    m10.add_trap(550, 400, 600, 420)
    m10.add_ground(750, 340, 1000, 600) # 终点高台
    m10.add_trap(650, 550, 750, 600)    # 最后的深渊
    m10.set_goal(900, 340)
    m10.save()

    print("所有 10 关地图生成完毕！可以直接运行 main.py 测试了。")


if __name__ == "__main__":
    generate_all_maps()