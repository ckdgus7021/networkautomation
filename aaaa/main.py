import pygame
import random
import sys
import time
from kivy.app import App


class test(App):

    def build(self):
        # 메인 코드
        pygame.init()
        
        pygame.display.set_caption('test')

        playGame()



def paintEntity(entity, x, y) :
    monitor.blit(entity, (x, y))

def writeGameOver() :
    myfont = pygame.font.Font('C:\img/NanumGothic-Regular.ttf', 40)
    txt = myfont.render(u'우주선 폭파!! 게임 끝!', True, (255-r, 255-g, 255-b))
    monitor.blit(txt, (swidth/2-180, sheight/2-50))
    pygame.display.update()
    time.sleep(5)

def writeScore(score) :
    myfont = pygame.font.Font('C:\img/NanumGothic-Regular.ttf', 20)
    txt = myfont.render(u'파괴한 우주괴물 수 : ' + str(score), True, (255-r, 255-g, 255-b))
    monitor.blit(txt, (10, sheight - 40))

def playGame() :
    global monitor, r, g, b, ship, monster, monsterImage, missile

    monitor = pygame.display.set_mode((swidth, sheight))
    ship = pygame.image.load('C:\img/ship02.png')
    shipSize = ship.get_rect().size
    missile = pygame.image.load('C:\img/missile.png')

    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)

    # 우주선 초기 위치
    shipX = swidth / 2
    shipY = sheight * 0.8
    dx, dy = 0, 0  # 키보드를 누를 때 우주선의 이동량

    monster = pygame.image.load(random.choice(monsterImage))
    monsterSize = monster.get_rect().size
    monsterX = random.randrange(0, int(swidth))
    monsterY = 0
    monsterSpeed = random.randrange(5,10)

    missileX, missileY = None, None

    fireCount = 0


# 무한 루프
    while True :
        (pygame.time.Clock()).tick(50)   # 게임 진행을 늦춤
        monitor.fill((r,g,b))   # 배경을 칠함

        for e in pygame.event.get() :
            if e.type in [pygame.QUIT] :
                pygame.quit()
                sys.exit()

            # 방향키에 따라 우주선 이동
            if e.type in [pygame.KEYDOWN] :
                if e.key == pygame.K_LEFT : dx = -5
                elif e.key == pygame.K_RIGHT : dx = +5
                elif e.key == pygame.K_UP : dy = -5
                elif e.key == pygame.K_DOWN : dy = +5

                elif e.key == pygame.K_SPACE :
                    if missileX == None :
                        missileX = shipX + shipSize[0]/2
                        missileY = shipY

            # 방향키를 떼면 우주선 멈춤
            if e.type in [pygame.KEYUP] :
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT \
                    or e.key == pygame.K_UP or e.key == pygame.K_DOWN :
                    dx, dy = 0, 0
                
        # 우주선이 화면 안에서만 움직임
        if (0 < shipX + dx and shipX + dx <= swidth - shipSize[0]) \
            and (sheight / 2 < shipY + dy and shipY + dy <= sheight - shipSize[1]) : # x축은 끝까지, y축은 화면의 중앙까지만(sheight /2)
            shipX += dx
            shipY += dy

        paintEntity(ship, shipX, shipY) # 우주선을 화면에 표시

        # 괴물 움직임
        monsterY += monsterSpeed
        if monsterY > sheight :
            monsterY = 0
            monsterX = random.randrange(0, int(swidth))
            monster = pygame.image.load(random.choice(monsterImage))
            monsterSize = monster.get_rect().size
            monsterSpeed = random.randrange(5,10)
            fireCount -= 1

        paintEntity(monster, monsterX, monsterY)


        if missileX != None :
            missileY -= 10
            if missileY < 0 :
                missileX, missileY = None, None
        if missileX != None :
            paintEntity(missile, missileX, missileY)

            # 미사일 맞추면 괴물 재생성
            if (monsterX < missileX and missileX < monsterX + monsterSize[0]) and \
                (monsterY < missileY and missileY < monsterY + monsterSize[1]) :
                fireCount += 1

                ship = pygame.image.load(random.choice(shipImage))
                monster = pygame.image.load(random.choice(monsterImage))
                monsterSize = monster.get_rect().size
                monsterY = 0
                monsterX = random.randrange(0, int(swidth))
                monsterSpeed = random.randrange(5,10)

                missileX, missileY = None, None
        
        mx1 = monsterX
        my1 = monsterY
        mx2 = monsterX + monsterSize[0]
        my2 = monsterY + monsterSize[1]
        sx1 = shipX
        sy1 = shipY
        sx2 = shipX + shipSize[0]
        sy2 = shipY + shipSize[1]

        meet = False
        # 우주 괴물이 우주선 안에 들어가는지 체크
        if (sx1 < mx1 and mx1 < sx2) and (sy1 < my1 and my1 < sy2) :
            meet = True
        elif (sx1 < mx2 and mx2 < sx2) and (sy1 < my2 and my2 < sy2) :
            meet = True
        elif (sx1 < mx1 and mx1 < sx2) and (sy1 < my2 and my2 < sy2) :
            meet = True
        elif (sx1 < mx2 and mx2 < sx2) and (sy1 < my1 and my1 < sy2) :
            meet = True
        # 우주선이 우주괴물 안에 들어가는지 체크(통과방지)
        if (mx1 < sx1 and sx1 < mx2) and (my1 < sy1 and sy1 < my2) :
            meet = True
        elif (mx1 < sx2 and sx2 < mx2) and (my1 < sy2 and sy2 < my2) :
            meet = True
        elif (mx1 < sx1 and sx1 < mx2) and (my1 < sy2 and sy2 < my2) :
            meet = True
        elif (mx1 < sx2 and sx2 < mx2) and (my1 < sy1 and sy1 < my2) :
            meet  = True

        if meet == True :
            writeGameOver()
            pygame.quit()
            sys.exit()


        writeScore(fireCount)


        pygame.display.update()
        print('~', end = '')



# 전역 변수 선언
r, g, b = [0] * 3
swidth, sheight = 500, 700
monitor = None
ship, shipSize = None, 0
monsterImage = ['C:\img/monster01.png', 'C:\img/monster02.png', 'C:\img/monster03.png', 'C:\img/monster04.png', 'C:\img/monster05.png', \
    'C:\img/monster06.png', 'C:\img/monster07.png', 'C:\img/monster08.png', 'C:\img/monster09.png', 'C:\img/monster10.png']
monster = None
missile = None
shipImage = ['C:\img/ship01.png', 'C:\img/ship02.png', 'C:\img/ship03.png', 'C:\img/ship04.png']


if __name__ == '__main__':
    test().run()

