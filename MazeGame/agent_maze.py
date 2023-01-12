import tkinter as tk
import numpy as np
from plt_generate_maze import Maze


def left_move(x_coordinate, y_coordinate):
    x = (x_coordinate, y_coordinate,
         x_coordinate, y_coordinate + ratio)
    if x not in can_line:
        return True
    return False


def right_move(x_coordinate, y_coordinate):
    x = (x_coordinate + ratio, y_coordinate,
         x_coordinate + ratio, y_coordinate + ratio)
    if x not in can_line:
        return True
    return False


def up_move(x_coordinate, y_coordinate):
    x = (x_coordinate, y_coordinate,
         x_coordinate + ratio, y_coordinate)
    if x not in can_line:
        return True
    return False


def down_move(x_coordinate, y_coordinate):
    x = (x_coordinate, y_coordinate + ratio,
         x_coordinate + ratio, y_coordinate + ratio)
    if x not in can_line:
        return True
    return False


def left_arrow(event):
    if left_move(maze_can.x_coordinate, maze_can.y_coordinate):
        maze_can.x_coordinate -= ratio
        maze_can.delete(maze_can.player)
        maze_can.player = maze_can.create_oval(maze_can.x_coordinate, maze_can.y_coordinate,
                                               maze_can.x_coordinate + ratio, maze_can.y_coordinate + ratio,
                                               width=1, fill='red')


def right_arrow(event):
    if right_move(maze_can.x_coordinate, maze_can.y_coordinate):
        maze_can.delete(maze_can.player)
        maze_can.x_coordinate += ratio
        maze_can.player = maze_can.create_oval(maze_can.x_coordinate, maze_can.y_coordinate,
                                               maze_can.x_coordinate + ratio, maze_can.y_coordinate + ratio,
                                               width=1, fill='red')


def up_arrow(event):
    if up_move(maze_can.x_coordinate, maze_can.y_coordinate):
        maze_can.delete(maze_can.player)
        maze_can.y_coordinate -= ratio
        maze_can.player = maze_can.create_oval(maze_can.x_coordinate, maze_can.y_coordinate,
                                               maze_can.x_coordinate + ratio, maze_can.y_coordinate + ratio,
                                               width=1, fill='red')


def down_arrow(event):
    if down_move(maze_can.x_coordinate, maze_can.y_coordinate):
        maze_can.delete(maze_can.player)
        maze_can.y_coordinate += ratio
        maze_can.player = maze_can.create_oval(maze_can.x_coordinate, maze_can.y_coordinate,
                                               maze_can.x_coordinate + ratio, maze_can.y_coordinate + ratio,
                                               width=1, fill='red')


height = 50
width = 50
maze = Maze(height=height, width=width)
maze.generate_maze()
window = tk.Tk()
window.title("简单绘画")
height_can = 0;
width_can = 0;
ratio = 0
while height_can < 500 or width_can < 600:
    ratio += 1
    height_can = maze.HEIGHT * ratio
    width_can = maze.WIDTH * ratio
maze_can = tk.Canvas(window, width=width_can + ratio, height=height_can + ratio)
maze_can.pack()
can_line = [(ratio, ratio, ratio, 1 * ratio + ratio),
            (maze.WIDTH * ratio + ratio, (maze.HEIGHT - 1) * ratio + ratio, maze.WIDTH * ratio + ratio,
             maze.HEIGHT * ratio + ratio)]
for edge in maze.edges:
    q = (edge[0] * ratio + ratio, edge[1] * ratio + ratio, edge[2] * ratio + ratio, edge[3] * ratio + ratio)
    can_line.append(q)
    maze_can.create_line((q[0], q[1]), (q[2], q[3]), width=2)
maze_can.x_coordinate = ratio
maze_can.y_coordinate = ratio
maze_can.player = maze_can.create_oval(maze_can.x_coordinate, maze_can.y_coordinate,
                                       maze_can.x_coordinate + ratio, maze_can.y_coordinate + ratio,
                                       width=1, fill='red')
window.bind('<Left>', left_arrow)
window.bind('<Right>', right_arrow)
window.bind('<Up>', up_arrow)
window.bind('<Down>', down_arrow)

maze_can.agent = maze_can.create_oval(maze_can.x_coordinate, maze_can.y_coordinate,
                                      maze_can.x_coordinate + ratio, maze_can.y_coordinate + ratio,
                                      width=1, fill='blue')
agent_list = np.zeros((height, width))
agent_list -= 100000
agent_list[height - 1][width - 1] = 0
valid_queue = []
valid_queue.append((height - 1, width - 1))


def get_queue(height_index, width_index):
    if left_move((width_index + 1) * ratio, (height_index + 1) * ratio) and agent_list[height_index][
        width_index - 1] == -100000:
        valid_queue.append((height_index, width_index - 1))
    if right_move((width_index + 1) * ratio, (height_index + 1) * ratio) and agent_list[height_index][
        width_index + 1] == -100000:
        valid_queue.append((height_index, width_index + 1))
    if up_move((width_index + 1) * ratio, (height_index + 1) * ratio) and agent_list[height_index - 1][
        width_index] == -100000:
        valid_queue.append((height_index - 1, width_index))
    if down_move((width_index + 1) * ratio, (height_index + 1) * ratio) and agent_list[height_index + 1][
        width_index] == -100000:
        valid_queue.append((height_index + 1, width_index))


def reward_value(height_index, width_index):
    i = {}
    if left_move((width_index + 1) * ratio, (height_index + 1) * ratio):
        i[agent_list[height_index][width_index - 1]] = 'left'
    if right_move((width_index + 1) * ratio, (height_index + 1) * ratio):
        i[agent_list[height_index][width_index + 1]] = 'right'
    if up_move((width_index + 1) * ratio, (height_index + 1) * ratio):
        i[agent_list[height_index - 1][width_index]] = 'up'
    if down_move((width_index + 1) * ratio, (height_index + 1) * ratio):
        i[agent_list[height_index + 1][width_index]] = 'down'
    return i


for index in valid_queue:
    get_queue(index[0], index[1])
    if agent_list[index[0]][index[1]] == -100000:
        nearby_dic = reward_value(index[0], index[1])
        agent_list[index[0]][index[1]] = max(nearby_dic.keys()) - 1

def get_path(height_index, width_index):
    nearby_dic = reward_value(height_index, width_index)
    direction = nearby_dic[max(nearby_dic.keys())]
    if direction == 'left':
        path_queue.append((height_index, width_index - 1))
    if direction == 'right':
        path_queue.append((height_index, width_index + 1))
    if direction == 'up':
        path_queue.append((height_index - 1, width_index))
    if direction == 'down':
        path_queue.append((height_index + 1, width_index))


path_queue = [(0, 0)]
for index in path_queue:
    x = index[1] * ratio + 1.3 * ratio
    y = index[0] * ratio + 1.3 * ratio
    maze_can.create_rectangle(x, y, x + 0.4 * ratio, y + 0.4 * ratio, fill='green', outline='green')
    if index == (height - 1, width - 1):
        break
    get_path(index[0], index[1])

window.mainloop()
