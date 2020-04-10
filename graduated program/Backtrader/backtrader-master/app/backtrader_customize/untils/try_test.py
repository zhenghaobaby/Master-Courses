class Solution(object):
    def getMaximumGold(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        self.ans = 0  
        m = len(grid)
        n = len(grid[0])

        sum_val = 0


        def DFS(i, j, visit, start):

            direction = []

            if i > 0:  # up
                if grid[i - 1][j] != 0 and (i - 1, j) not in visit:
                    direction.append((i - 1, j))
            if i < m - 1:  # down
                if grid[i + 1][j] != 0 and (i + 1, j) not in visit:
                    direction.append((i + 1, j))
            if j > 0:  # left
                if grid[i][j - 1] != 0 and (i, j - 1) not in visit:
                    direction.append((i, j - 1))
            if j < n - 1:  # right
                if grid[i][j + 1] != 0 and (i, j + 1) not in visit:
                    direction.append((i, j + 1))

            if len(direction) == 0:
                self.ans = max(self.ans,start)

            else:
                for temp in direction:
                    start += grid[temp[0]][temp[1]]
                    visit.append(temp)
                    DFS(temp[0], temp[1], visit, start)
                    del visit[-1]
                    start-=grid[temp[0]][temp[1]]
            return self.ans


        for i in range(m):
            for j in range(n):
                visit = []
                if grid[i][j] > 0:
                    visit.append((i, j))
                    self.ans = 0
                    sum_val = max(sum_val, DFS(i, j, visit, grid[i][j]))
                else:
                    continue

        return sum_val

a = Solution()
m = a.getMaximumGold([[0,0,34,0,5,0,7,0,0,0],[0,0,0,0,21,0,0,0,0,0],[0,18,0,0,8,0,0,0,4,0],[0,0,0,0,0,0,0,0,0,0],[15,0,0,0,0,22,0,0,0,21],[0,0,0,0,0,0,0,0,0,0],[0,7,0,0,0,0,0,0,38,0]])
s= 2