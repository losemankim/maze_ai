import pygame
import numpy as np
import env
#인자값받기
import argparse


# 미로 설정
def start(maze_size,visualize,ep_num,episodes):   
    print(visualize)
    maze = env.make_maze(maze_size)
    maze = np.array(maze)
    wall_img=pygame.image.load("images/wall.png")
    player_img=pygame.image.load("images/player.png")
    exit_img=pygame.image.load("images/exit.png")
    #이미지크기조정
    wall_img=pygame.transform.scale(wall_img,(50,50))
    player_img=pygame.transform.scale(player_img,(50,50))
    exit_img=pygame.transform.scale(exit_img,(50,50))


    # 미로의 크기
    maze_height = len(maze)
    maze_width = len(maze[0])
    maze[maze_height - 2][maze_width - 1] = 2

    # 가능한 행동
    actions = ['up', 'down', 'left', 'right']

    # Q 테이블 초기화
    q_table = np.zeros((maze_height, maze_width, len(actions)))

    # 하이퍼파라미터 설정
    learning_rate = 0.1
    discount_factor = 0.99
    exploration_rate = 0.3
    max_exploration_rate = 1.0
    min_exploration_rate = 0.01
    exploration_decay_rate = 0.01
    num_episodes = episodes
    move=0
    prev_move=0
    # 초기화
    pygame.init()
    clock = pygame.time.Clock()

    # 색상 설정
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # 창 크기 설정
    if visualize:
        screen_width = maze_width * 50
        screen_height = maze_height * 50
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Maze Solver")

    # 에이전트 초기 위치
    agent_position = (0, 1)

    # 게임 루프
    running = True
    current_episode = 1

    while running:
        if visualize:
            if ep_num<=current_episode:            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                # 미로 그리기
                screen.fill(BLACK)
                for row in range(maze_height):
                    for col in range(maze_width):
                        if maze[row][col] == 1:
                            #img사용하기
                            screen.blit(wall_img,(col * 50, row * 50))
                            
                            
                        if maze[row][col] == 2:
                            screen.blit(exit_img,(col * 50, row * 50))
                
                # 에이전트 그리기
                screen.blit(player_img,(agent_position[1] * 50, agent_position[0] * 50))
            
        # 탐험 및 활용 결정
        exploration_rate_threshold = np.random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action_index = np.argmax(q_table[agent_position])#최적의 행동
        else:
            action_index = np.random.randint(len(actions))#완전랜덤
            
        move+=1
        action = actions[action_index]
        
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
        # 벽에 부딪혔을 경우
        if maze[next_position[0]][next_position[1]] == 1:
            next_position = agent_position
            reward = -100
        if maze[next_position[0]][next_position[1]] == 2:
            agent_position = next_position
        if move>100:
            reward=-100

        
        # 보상 계산
        if next_position == (maze_height - 2, maze_width - 1):
            reward = 100
        elif prev_move==next_position:
            reward=-100
            print("같은 위치에 있음")
        else:
            reward = -1
        
        # Q 테이블 업데이트
        q_table[agent_position][action_index] += learning_rate * (
            reward + discount_factor * np.max(q_table[next_position]) - q_table[agent_position][action_index]
        )
        
        # 에이전트 위치 업데이트
        agent_position = next_position
        
        # 화면 업데이트
        if visualize:
            if ep_num<=current_episode:
                #reward표시
                font = pygame.font.SysFont('malgungothic', 30)
                text = font.render("reward"+str(reward), True, GREEN)
                screen.blit(text, (10, 70))
                #prev_move표시
                font = pygame.font.SysFont('malgungothic', 30)
                text = font.render("prev"+str(prev_move), True, GREEN)
                screen.blit(text, (10, 10))
                #agent_position표시
                font = pygame.font.SysFont('malgungothic', 30)
                text = font.render("agent"+str(agent_position), True, GREEN)
                screen.blit(text, (10, 40))



                pygame.display.flip()
                clock.tick(10)#
        
        # 에피소드 종료 체크
        if agent_position == (maze_height - 2, maze_width - 1):
            print("Episode", current_episode, "completed")
            current_episode += 1
            agent_position = (0, 1)
            if visualize:
                if ep_num<=current_episode:
                    pygame.time.wait(10)
        
        # 모든 에피소드가 완료되면 종료
        if current_episode > num_episodes:
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

    start(args.maze_size,args.visualize,args.view_episode,args.episode)