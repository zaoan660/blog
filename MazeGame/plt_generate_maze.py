import sys
import matplotlib.pyplot as plt
from random import randint

class Maze(object):
    def __init__(self, height, width):
        sys.setrecursionlimit(height*2 * width*2)
        self.HEIGHT = height
        self.WIDTH = width
        self.visited = []
        self.edges = set()

    def initVisitedList(self):
        for y in range(self.HEIGHT):
            line = []
            for x in range(self.WIDTH):
                line.append(False)
            self.visited.append(line)

    def get_edges(self,x, y):
        result = []
        result.append((x, y, x, y + 1))
        result.append((x + 1, y, x + 1, y + 1))
        result.append((x, y, x + 1, y))
        result.append((x, y + 1, x + 1, y + 1))
        return result

    def initEdgeList(self):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                cellEdges = self.get_edges(x, y)
                for edge in cellEdges:
                    self.edges.add(edge)

    def shuffle(self, dX, dY):
        for t in range(4):
            i = randint(0, 3)
            j = randint(0, 3)
            dX[i], dX[j] = dX[j], dX[i]
            dY[i], dY[j] = dY[j], dY[i]

    def isValidPosition(self,x, y):
        if x < 0 or x >= self.WIDTH:
            return False
        elif y < 0 or y >= self.HEIGHT:
            return False
        else:
            return True

    def getCommonEdge(self, cell1_x, cell1_y, cell2_x, cell2_y):
        edges1 = self.get_edges(cell1_x, cell1_y)
        edges2 = set(self.get_edges(cell2_x, cell2_y))
        for edge in edges1:
            if edge in edges2:
                return edge
        return None

    def DFS(self, X, Y, edgeList, visited):
        dX = [0, 0, -1, 1]
        dY = [-1, 1, 0, 0]
        self.shuffle(dX, dY)
        for i in range(len(dX)):
            nextX = X + dX[i]
            nextY = Y + dY[i]
            if self.isValidPosition(nextX, nextY):
                if not visited[nextY][nextX]:
                    visited[nextY][nextX] = True
                    commonEdge = self.getCommonEdge(X, Y, nextX, nextY)
                    if commonEdge in edgeList:
                        edgeList.remove(commonEdge)
                    self.DFS(nextX, nextY, edgeList, visited)

    def drawLine(self,x1, y1, x2, y2):
        plt.plot([x1, x2], [y1, y2], color="black")

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


