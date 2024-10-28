import tkinter as tk
import random

class Game2048:
    print("hello world")
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.master.bind("<Key>", self.key_down)

        self.size = 4  # 4x4 grid
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.colors = {
            0: "#CDC1B4", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
            32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61", 512: "#EDC850",
            1024: "#EDC53F", 2048: "#EDC22E"
        }

        self.init_grid()
        self.spawn_tile()
        self.spawn_tile()
        self.update_grid()

    def init_grid(self):
        """创建 4x4 的游戏网格"""
        self.tiles = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                tile = tk.Label(self.master, text="", width=4, height=2,
                                font=("Helvetica", 32, "bold"), bg=self.colors[0], fg="#776E65")
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def spawn_tile(self):
        """在随机空位置生成一个新的 2 或 4"""
        empty_tiles = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = random.choice([2, 4])

    def update_grid(self):
        """更新网格显示"""
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                self.tiles[i][j].config(text=str(value) if value != 0 else "", bg=self.colors[value])

    def key_down(self, event):
        """处理键盘输入"""
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            if self.move(key):
                self.spawn_tile()
                self.update_grid()
                if self.check_game_over():
                    self.game_over()

    def move(self, direction):
        """处理滑动逻辑"""
        def slide_row_left(row):
            """将行向左滑动并合并相同数字"""
            new_row = [i for i in row if i != 0]
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    new_row[i + 1] = 0
            new_row = [i for i in new_row if i != 0]
            return new_row + [0] * (self.size - len(new_row))

        moved = False
        if direction == "Left":
            for i in range(self.size):
                new_row = slide_row_left(self.grid[i])
                if new_row != self.grid[i]:
                    moved = True
                self.grid[i] = new_row
        elif direction == "Right":
            for i in range(self.size):
                new_row = slide_row_left(self.grid[i][::-1])[::-1]
                if new_row != self.grid[i]:
                    moved = True
                self.grid[i] = new_row
        elif direction == "Up":
            for j in range(self.size):
                column = [self.grid[i][j] for i in range(self.size)]
                new_column = slide_row_left(column)
                if new_column != column:
                    moved = True
                for i in range(self.size):
                    self.grid[i][j] = new_column[i]
        elif direction == "Down":
            for j in range(self.size):
                column = [self.grid[i][j] for i in range(self.size)]
                new_column = slide_row_left(column[::-1])[::-1]
                if new_column != column:
                    moved = True
                for i in range(self.size):
                    self.grid[i][j] = new_column[i]
        return moved

    def check_game_over(self):
        """检查游戏是否结束"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return False
                if i < self.size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < self.size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def game_over(self):
        """显示游戏结束提示"""
        game_over_label = tk.Label(self.master, text="Game Over!", font=("Helvetica", 32, "bold"), bg="#CDC1B4")
        game_over_label.grid(row=1, columnspan=self.size)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()