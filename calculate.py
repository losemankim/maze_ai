from collections import deque

class Calculate():
    def __init__(self, maze):
        self.maze = maze
        self.shortest_path = self.calculate_shortest_path()
        print("Shortest Path:", self.shortest_path)
        
    def return_shortest_path(self):
        return self.shortest_path
    # 최단거리 계산 함수
    def calculate_shortest_path(self):
        maze = self.maze
        start_position = (0, 1)
        end_position = (len(maze) - 2, len(maze[0]) - 2)

        # 방문 여부를 저장하는 배열
        visited = [[False] * len(maze[0]) for _ in range(len(maze))]

        # 이동 방향 (상, 하, 좌, 우)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # 시작 위치를 큐에 추가
        queue = deque([(start_position, 0)])
        visited[start_position[0]][start_position[1]] = True

        while queue:
            position, distance = queue.popleft()

            if position == end_position:
                return distance

            for direction in directions:
                next_position = (position[0] + direction[0], position[1] + direction[1])

                if (
                    0 <= next_position[0] < len(maze)
                    and 0 <= next_position[1] < len(maze[0])
                    and maze[next_position[0]][next_position[1]] == 0
                    and not visited[next_position[0]][next_position[1]]
                ):
                    queue.append((next_position, distance + 1))
                    visited[next_position[0]][next_position[1]] = True

        return -1  # 최단거리가 없을 경우 -1 반환
