import pygame
import numpy as np
import env
import argparse

class Maze_ai():
    def __init__(self,maze_size,view_episode,visualize,episodes):
        self.maze = np.array(env.make_maze(maze_size))
        self.wall_img=pygame.image.load("images/wall.png")
        self.player_img=pygame.image.load("images/player.png")
        self.exit_img=pygame.image.load("images/exit.png")
        self.wall_img=pygame.transform.scale(self.wall_img,(50,50))
        self.player_img=pygame.transform.scale(self.player_img,(50,50))
        self.exit_img=pygame.transform.scale(self.exit_img,(50,50))
        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])
        self.maze[self.maze_height - 2][self.maze_width - 1] = 2
        # 가능한 행동
        self.actions = ['up', 'down', 'left', 'right']
        # Q 테이블 초기화
        self.q_table = np.zeros((self.maze_height, self.maze_width, len(self.actions)))
        # 하이퍼파라미터 설정
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.exploration_rate = 0.1
        self.ep_num = episodes
        #reward관련변수
        self.move=0
        self.prev_move=0
        self.serched=[]# 미로 설정
        self.visualize=visualize
        self.view_episode=view_episode
        self.maze_size=maze_size
        self.start()
    def start(self):   
        # pygame 초기화
        pygame.init()
        clock = pygame.time.Clock()
        # 색상 설정
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        # 창 크기 설정
        if self.visualize:
            screen_width = self.maze_width * 50
            screen_height = self.maze_height * 50
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Maze Solver")
        # 에이전트 초기 위치
        agent_position = (0, 1)
        # 게임 루프
        running = True
        current_episode = 1
        while running:
            if self.visualize: 
                if self.view_episode<=current_episode:            
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    
                    # 미로 그리기
                    screen.fill(BLACK)
                    for row in range(self.maze_height):
                        for col in range(self.maze_width):
                            if self.maze[row][col] == 1:
                                #img사용하기
                                screen.blit(self.wall_img,(col * 50, row * 50))
                                
                                
                            if self.maze[row][col] == 2:
                                screen.blit(self.exit_img,(col * 50, row * 50))
                    
                    # 에이전트 그리기
                    screen.blit(self.player_img,(agent_position[1] * 50, agent_position[0] * 50))
                
            # 탐험 및 활용 결정
            self.exploration_rate_threshold = np.random.uniform(0, 1)
            if self.exploration_rate_threshold > self.exploration_rate:
                action_index = np.argmax(self.q_table[agent_position])#최적의 행동
            else:
                action_index = np.random.randint(len(self.actions))#완전랜덤
                
            self.move+=1
            action = self.actions[action_index]
            
            # 에이전트 이동
            if action == 'up':
                next_position = (agent_position[0] - 1, agent_position[1])
            elif action == 'down':
                next_position = (agent_position[0] + 1, agent_position[1])
            elif action == 'left':
                next_position = (agent_position[0], agent_position[1] - 1)
            else:
                next_position = (agent_position[0], agent_position[1] + 1)
            #이전과 같은 위치에 있을 경우
            prev_move=agent_position
            self.serched.append(prev_move)

            # 벽에 부딪혔을 경우
            if self.maze[next_position[0]][next_position[1]] == 1:
                next_position = agent_position
                reward = -100
            if self.maze[next_position[0]][next_position[1]] == 2:
                agent_position = next_position
            if self.move>100:
                reward=-100

            
            # 보상 계산
            if next_position == (self.maze_height - 2, self.maze_width - 1):
                reward = 100
            elif next_position in self.serched:
                reward= -100
            else:
                reward = -1
            
            # Q 테이블 업데이트
            self.q_table[agent_position][action_index] += self.learning_rate * (
                reward + self.discount_factor * np.max(self.q_table[next_position]) - self.q_table[agent_position][action_index]
            )
            
            # 에이전트 위치 업데이트
            agent_position = next_position
            
            # 화면 업데이트
            if self.visualize:
                if self.view_episode<=current_episode:
                    #reward표시
                    font = pygame.font.SysFont('malgungothic', 30)
                    text = font.render("current_episode"+str(current_episode), True, GREEN)
                    screen.blit(text, (10, 70))
                    pygame.display.flip()
                    clock.tick(10)#
            
            # 에피소드 종료 체크
            if agent_position == (self.maze_height - 2, self.maze_width - 1):
                print("Episode", current_episode, "completed")
                current_episode += 1
                agent_position = (0, 1)
                self.move=0
                prev_move=0
                serched=[]
                self.exploration_rate=self.exploration_rate*0.99
                if self.visualize:
                    if self.view_episode<=current_episode:
                        print(self.exploration_rate)
                        pygame.time.wait(10)
            
            # 모든 에피소드가 완료되면 종료
            if current_episode > self.ep_num:
                running = False

    # 게임 종료

    pygame.quit()
if __name__ == '__main__':
    paser=argparse.ArgumentParser()
    paser.add_argument('--maze_size',type=int,default=3)
    paser.add_argument('--view_episode',type=int,default=900)
    paser.add_argument('--visualize',type=bool,default=False)
    paser.add_argument('--episode',type=int,default=1000)
    args=paser.parse_args()

    Maze_ai(args.maze_size,args.view_episode,args.visualize,args.episode)