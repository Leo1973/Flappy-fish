import pygame
from pygame.locals import *
from gameobjects.vector2 import *   
import random
import math
SCREEN_SIZE = (600,800)
class Object(object):#实体类
    def __init__(self,name,position):
        self.name = name
        self.position = Vector2(*position)
        self.speed = 0


class Fish(Object):#小球类
    def __init__(self,name,position):
        Object.__init__(self,name,position)
    def render(self,screen):#绘制小球自己
        x,y = self.position
        pygame.draw.circle(screen, (251,162,40), (int(x),int(y)),30)
class Block(Object):#方块类
    def __init__(self,name,position,ID):
        Object.__init__(self,name,position)
        self.ran = random.randint(0,300)#随机值用于开口位置
        self.ID = ID#用于标记这是第几个方块，方便统计分数
    def render(self,screen):#绘制上下两个长方形形成障碍物
        x,y = self.position       
        pygame.draw.rect(screen,(0,255,0),Rect((int(x),int(y)),(100,100+self.ran)))
        pygame.draw.rect(screen,(0,255,0),Rect((int(x),self.ran+350),(100,500)))
class Button(object):#按钮类
    def __init__(self , position):
 
        self.position = position
 
    def render(self, screen):
        x, y = self.position
        pygame.draw.circle(screen, (251,162,40), (int(x),int(y)),50)
 
    def is_over(self, point):#判断鼠标是否在按钮上
        x  = self.position[0] - point[0]
        y  = self.position[1] - point[1]
        v = Vector2((x,y))
        length = v.get_length()
        return length < 50
        
def start():#开始界面
    buttons = {}
    buttons["start"] = Button((300,400))#开始按钮位置
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)#设置窗口

    while True:
        screen.fill((140,215,251))#填色
        button_pressed = None#初始化按钮
        buttons["start"]
        for button in buttons.values():#绘制所有按钮
            button.render(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:#如果鼠标按下
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        button_pressed = button_name
                        break
            if button_pressed is not None:
                if button_pressed == "start":#如果按得是开始按钮
                    run()#开始

    
def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)#窗口
    font = pygame.font.SysFont("arial",32)#字体
    fish = Fish("flappy fish",(300.,400.))#球类
    block1 = Block("Block1",(600.,0.),1)#方块1
    block2 = Block("Block2",(600.,0.),0)#方块2
    run1 = 0#运行标志位
    flag1 = 0#计数标志位
    run2 = 0
    flag2 = 0
    clock = pygame.time.Clock()#引入时钟
    point_text = "0"#初始化分数
    ID = 1#初始化方块ID
    while True:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:#空格就获得向上的速度
                 if event.key == K_SPACE:
                    fish.speed = -4
        time_passed = clock.tick(80)/1000#80fps
        fish.speed += time_passed * 16#小球的加速度
        fish.position += (0,fish.speed)#计算小球位置
        block1.speed = time_passed * 160#方块的速度
        block1.position[0] -= block1.speed#方块的位置
        block2.position[0] -= block2.speed
        block1.render(screen)#绘制
        block2.render(screen)
        fish.render(screen)
        screen.blit(font.render(point_text,True,(0,0,0)),(300,50))#打印分数
        pygame.display.update()#update


        if fish.position[1] - 30< 0:#到达顶方的碰撞
            fish.position[1] = 30
            fish.speed = 0
        if fish.position[1] +30 > 800:#到达最下方判定死亡
            start()
        if block1.position[0] < 170 and flag1 == 0 :#当一个方块x坐标左移到170时另一个方块准备就绪
            block2.position[0] = 600.
            block2.speed = 0
            block2.ran = random.randint(0,300)
            ID+=1
            block2.ID = ID
            flag1 = 1
            flag2 = 0
        if block2.position[0] < 170 and flag2 == 0 :
            block1.position[0] = 600.
            block1.speed = 0
            block1.ran = random.randint(0,300)
            ID+=1
            block1.ID = ID
            flag2 = 1
            flag1 = 0
        
        if block1.position[0] < 100 and run1 == 0:#当一个方块左移到100时，另一个方块获得速度
            block2.speed = time_passed * 160
            run1 = 1
            run2 = 0
        if block2.position[0] < 100 and run2 == 0:
            block1.speed = time_passed * 160
            run2 = 1
            run1 = 0
        
        if 170 <= block1.position[0] <= 330 :#判定碰撞
            if 300 < block1.position[0] <= 330 and (math.sqrt(900 - (block1.position[0]-300)**2)+100+block1.ran > fish.position[1] or (math.sqrt(900 - (block1.position[0]-300)**2)+ 450 - block1.ran)>800 - fish.position[1]):
                start()
            if 200 <= block1.position[0] <= 300 and (fish.position[1] < block1.ran + 130 or fish.position[1] > 320 + block1.ran):
                start()
            if 170 <= block1.position[0] < 200 and (math.sqrt(900 - (block1.position[0]-170)**2)+100+block1.ran > fish.position[1] or (math.sqrt(900 - (block1.position[0]-170)**2)+ 450 - block1.ran)>800 - fish.position[1]):
                start()
            
        if 170 <= block2.position[0] <= 330:
            if 300 < block2.position[0] <= 330 and (math.sqrt(900 - (block2.position[0]-300)**2)+100+block2.ran > fish.position[1]or (math.sqrt(900 - (block2.position[0]-300)**2)+ 450 - block2.ran)>800 - fish.position[1]):
                start()
            if 200 <= block2.position[0] <= 300 and (fish.position[1] < block2.ran + 130 or fish.position[1] > 320 + block2.ran):
                start()
            if 170 <= block2.position[0] < 200 and (math.sqrt(900 - (block2.position[0]-170)**2)+100+block2.ran > fish.position[1] or (math.sqrt(900 - (block2.position[0]-170)**2)+ 450 - block2.ran)>800 - fish.position[1]):
                start()
        point_text = str(min (block1.ID,block2.ID))#获得当前分数






if __name__ == "__main__":
    start()
