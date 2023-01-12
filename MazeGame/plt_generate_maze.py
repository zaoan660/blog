import sys
import matplotlib.pyplot as plt
from random import randint

# 生成地图主要使用深度优先搜索遍历所有的点
class Maze(object):
    def __init__(self, height, width):
        #设置栈的最大深度，防止递归写错占太多内存
        sys.setrecursionlimit(height*2 * width*2)
        self.HEIGHT = height
        self.WIDTH = width
        #这个列表用来设置还有哪个点没有使用过
        self.visited = []
        #这个是边的列表，把（0，0）带入get_edges()很容易就能理解是哪四条边
        self.edges = set()

    # 这个方法用来初始化点的列表
    def initVisitedList(self):
        for y in range(self.HEIGHT):
            line = []
            for x in range(self.WIDTH):
                line.append(False)
            self.visited.append(line)

    # 这个用来获得每个点周围的边
    def get_edges(self,x, y):
        result = []
        result.append((x, y, x, y + 1))
        result.append((x + 1, y, x + 1, y + 1))
        result.append((x, y, x + 1, y))
        result.append((x, y + 1, x + 1, y + 1))
        return result

    # 这个用来初始化所有的边，形成集合
    def initEdgeList(self):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                cellEdges = self.get_edges(x, y)
                for edge in cellEdges:
                    self.edges.add(edge)

    # 这个是随机指定某个点旁边的点
    def shuffle(self, dX, dY):
        for t in range(4):
            i = randint(0, 3)
            j = randint(0, 3)
            dX[i], dX[j] = dX[j], dX[i]
            dY[i], dY[j] = dY[j], dY[i]

    # 这个用来判断点是否有效的，即是否包含在初始化点的那个列表里（那个列表里每一个False的索引都是一个点）
    def isValidPosition(self,x, y):
        if x < 0 or x >= self.WIDTH:
            return False
        elif y < 0 or y >= self.HEIGHT:
            return False
        else:
            return True

    # 这个用来返回应该删掉哪一条线
    def getCommonEdge(self, cell1_x, cell1_y, cell2_x, cell2_y):
        edges1 = self.get_edges(cell1_x, cell1_y)
        edges2 = set(self.get_edges(cell2_x, cell2_y))
        for edge in edges1:
            if edge in edges2:
                return edge
        return None

    # 这个是最主要的逻辑，他用来得到迷宫地图的线（在初始化所有边的基础上删掉一些边）
    def DFS(self, X, Y, edgeList, visited):
        # dX,dY 共同代表了原点上下左右的四个点
        dX = [0, 0, -1, 1]
        dY = [-1, 1, 0, 0]
        # 打乱顺序
        self.shuffle(dX, dY)
        for i in range(len(dX)):
            nextX = X + dX[i]
            nextY = Y + dY[i]
            if self.isValidPosition(nextX, nextY):
                # 判断点有没有被遍历过
                if not visited[nextY][nextX]:
                    visited[nextY][nextX] = True
                    # 删除某一条线
                    commonEdge = self.getCommonEdge(X, Y, nextX, nextY)
                    if commonEdge in edgeList:
                        edgeList.remove(commonEdge)
                    # 使用深度优先搜索遍历每一个点
                    self.DFS(nextX, nextY, edgeList, visited)

    # 用来在plt上画线
    def drawLine(self,x1, y1, x2, y2):
        plt.plot([x1, x2], [y1, y2], color="black")

    # 整合前面所有的方法
    def generate_maze(self):
        self.initVisitedList()
        self.initEdgeList()
        self.DFS(0, 0, self.edges, self.visited)
        self.edges.remove((0, 0, 0, 1))
        self.edges.remove((self.WIDTH, self.HEIGHT - 1, self.WIDTH, self.HEIGHT))

    def show_maze(self):
        plt.axis('equal')
        plt.title('Maze')
        for edge in self.edges:
            self.drawLine(edge[0], edge[1], edge[2], edge[3])
        plt.show()

if __name__ == '__main__':
    maze = Maze(height=4,width=4)
    maze.generate_maze()
    maze.show_maze()


