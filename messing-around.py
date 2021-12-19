# Python program for solution of M Coloring
# problem using backtracking
import numpy as np


class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

        # ALE ADDED:
        self.domain_tracker = {}
        for ii in range(vertices):
            self.domain_tracker[ii] = [1, 2, 3]
        self.colors = {1: 'R', 2: 'G', 3: 'B'}

    # A utility function to check if the current color assignment is valid for current vertex
    def isSafe(self, curr_vertex, color, c):
        for i in range(self.V):
            if self.graph[curr_vertex][i] == 1 and color[i] == c:
                return False
        return True

    # # ALE ADDED:
    # def forward_checking(self, curr_vertex, c):
    #     for i in range(self.V):
    #         if self.graph[curr_vertex][i] == 1:
    #             print(self.domain_tracker)
    #             neighbor = self.domain_tracker[i]
    #             neighbor.remove(c)

    # A recursive utility function to solve m-coloring problem
    def graphColorUtil(self, domain_size, color, curr_vertex):
        # import pdb; pdb.set_trace()
        # have we checked each vertex [==state in australia]?
        if curr_vertex == self.V:
            return True

        for c in range(1, domain_size + 1):
            if self.isSafe(curr_vertex, color, c):
                # assign color to current vertex:
                color[curr_vertex] = c
                # # ALE ADDED: action required! remove assigned color from the domain of the current vertex's neighbors!
                # self.forward_checking(curr_vertex, c)
                # # --------------------------------------------------
                if self.graphColorUtil(domain_size, color, curr_vertex + 1):
                    return True
                color[curr_vertex] = 0

    def graphColoring(self, domain_size):
        color = [0] * self.V
        if not self.graphColorUtil(domain_size, color, 0):
            return False

        # Print the solution
        print("Solution exist and Following are the assigned colours:")
        for c in color:
            final_color = self.colors[c]
            print(final_color)

        return True


# Driver Code
g = Graph(6)
g.graph = [[0, 0, 1, 1, 0, 1], [0, 0, 1, 1, 1, 0], [1, 1, 0, 1, 0, 0], [1, 1, 1, 0, 1, 1], [0, 1, 0, 1, 0, 0],
           [1, 0, 0, 1, 0, 0]]
domain_size = 3
g.graphColoring(domain_size)
