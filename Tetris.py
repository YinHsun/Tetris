import pygame,sys,time,random
from pygame.locals import*

pygame.init()
screen=pygame.display.set_mode((650,600))
pygame.display.set_caption('Tetris')
font=pygame.font.SysFont(None,48)
mainClock = pygame.time.Clock()
musicPlaying=True
pygame.mixer.music.load('background.mp3')
scoreSound=pygame.mixer.Sound('scoreMusic.wav')
gameOverSound=pygame.mixer.Sound('gameOverMusic.wav')

Type=[
      [(0,1),(1,0),(1,1)], #方
      [(-1,0),(1,0),(2,0)], #直
      [(0,1),(1,0),(2,0)], #L
      [(-2,0),(-1,0),(0,1)], #反L
      [(-1,0),(0,1),(1,0)], #T
      [(-1,0),(0,1),(1,1)], #Z
      [(-1,1),(0,1),(1,0)], #反Z
      ]
Color=[(255,255,0),(0,245,255),(255,140,0),(0,0,255),(148,0,211),(255,0,0),(0,255,0)]
white=(255,255,255)
black=(0,0,0)
gray=(112,128,144)

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text,font,surface,position):
    ptext=font.render(text,True,white)
    surface.blit(ptext,position)

def instruction():
    screen.fill(black)
    drawText('Tetris',font,screen,(250,102))
    drawText('Z or Up Key:Counterclockwise Rotate',font,screen,(0,150))
    drawText('X:Clockwise Rotate',font,screen,(0,200))
    drawText('Left Key:Left',font,screen,(0,250))
    drawText('Right Key:Right',font,screen,(0,300))
    drawText('Down Key:Slowly Down',font,screen,(0,350))
    drawText('Space:Quickly Down',font,screen,(0,400))
    drawText('M:Music On/Off',font,screen,(0,450))
    drawText('Press a key to start',font,screen,(140,500))

def PressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return
            
def showdifficulty():
    screen.fill(black)
    drawText('0',font,screen,(30,102))
    drawText('1',font,screen,(130,102))
    drawText('2',font,screen,(230,102))
    drawText('3',font,screen,(330,102))
    drawText('4',font,screen,(430,102))
    drawText('5',font,screen,(530,102))
    drawText('Easy--------------------------------Difficult',font,screen,(30,200))
    drawText('Press key 0 to 5 to select difficulty',font,screen,(30,350))
    
def selectdifficulty():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_0 or event.key == K_KP0:
                    return 0,0
                if event.key == K_1 or event.key == K_KP1:
                    return 2,1
                if event.key == K_2 or event.key == K_KP2:
                    return 2.5,2
                if event.key == K_3 or event.key == K_KP3:
                    return 10/3,3
                if event.key == K_4 or event.key == K_KP4:
                    return 5,4
                if event.key == K_5 or event.key == K_KP5:
                    return 10,5
           
def randBlock(p):
    kind=random.randint(0,6)
    return {'type':[Type[kind][0],Type[kind][1],Type[kind][2]],'color':Color[kind],'position':p}

def nextNrotate(b):
    newblock={'color':b['color'],'position':b['position'],'type':[]}
    for i in range(3):
        newblock['type']+=[[b['type'][i][1],-b['type'][i][0]]]
    return newblock

def nextProtate(b):
    newblock={'color':b['color'],'position':b['position'],'type':[]}
    for i in range(3):
        newblock['type']+=[[-b['type'][i][1],b['type'][i][0]]]
    return newblock

def rotatable(b,t):
    centerx,centery=b['position'][0],b['position'][1]
    for i in range(3):
        dx=b['type'][i][0]+centerx
        dy=b['type'][i][1]+centery
        if dx < 0 or dx > 9:
            return False
        if dy < 0 or dy > 19:
            return False
    for i in range(3):
        dx=centerx+b['type'][i][0]
        dy=centery+b['type'][i][1]
        if t[dy][dx] != black:
            return False
    return True
    
def Nrotate(b):
    for i in range(3):
        b['type'][i]=[b['type'][i][1],-b['type'][i][0]]

def Protate(b):
    for i in range(3):
        b['type'][i]=[-b['type'][i][1],b['type'][i][0]]
        
def drawTable(t):
    for i in range(20):
        for j in range(10):
            pygame.draw.rect(screen,t[i][j],(j*30+150+2.5,i*30+2.5,25,25),0)

def drawnowBlock(b):
    centerx,centery=150+b['position'][0]*30+2.5,b['position'][1]*30+2.5
    pygame.draw.rect(screen,b['color'],(centerx,centery,25,25),0)
    for i in range(3):
        dx=b['type'][i][0]*30+centerx
        dy=b['type'][i][1]*30+centery
        pygame.draw.rect(screen,b['color'],(dx,dy,25,25),0)
        
def drawdownBlock(b):
    centerx,centery=150+b['position'][0]*30+2.5,b['position'][1]*30+2.5
    pygame.draw.rect(screen,gray,(centerx,centery,25,25),5)
    for i in range(3):
        dx=b['type'][i][0]*30+centerx
        dy=b['type'][i][1]*30+centery
        pygame.draw.rect(screen,gray,(dx,dy,25,25),5)
        
def drawnextBlock(b):
    centerx,centery=b['position'][0]+2.5,b['position'][1]+2.5
    pygame.draw.rect(screen,b['color'],(centerx,centery,25,25),0)
    for i in range(3):
        dx=b['type'][i][0]*30+centerx
        dy=b['type'][i][1]*30+centery
        pygame.draw.rect(screen,b['color'],(dx,dy,25,25),0)
        
def nextmove(b,direction):
    newblock={'type':b['type'],'color':b['color']}
    if direction == 'left':
        newblock['position']=[b['position'][0]-1,b['position'][1]]
    elif direction == 'right':
        newblock['position']=[b['position'][0]+1,b['position'][1]]
    elif direction == 'down':
        newblock['position']=[b['position'][0],b['position'][1]+1]
    elif direction == 'leftdown':
        newblock['position']=[b['position'][0]-1,b['position'][1]+1]
    elif direction == 'rightdown':
        newblock['position']=[b['position'][0]+1,b['position'][1]+1]
    return newblock
    
def moveable(b,t):
    centerx,centery=b['position'][0],b['position'][1]
    if centerx < 0 or centerx > 9:
        return False
    if centery > 19:
        return False
    for i in range(3):
        dx=b['type'][i][0]+centerx
        dy=b['type'][i][1]+centery
        if dx < 0 or dx > 9:
            return False
        if dy > 19:
            return False
    if t[centery][centerx] != black:
        return False
    for i in range(3):
        dx=centerx+b['type'][i][0]
        dy=centery+b['type'][i][1]
        if t[dy][dx] != black:
            return False
    return True

def move_ip(b,direction):
    if direction == 'leftdown':
        b['position'][0]-=1
        b['position'][1]+=1
    elif direction == 'rightdown':
        b['position'][0]+=1
        b['position'][1]+=1
    elif direction == 'left':
        b['position'][0]-=1
    elif direction == 'right':
        b['position'][0]+=1
    elif direction == 'down':
        b['position'][1]+=1
        
def stopblock(b,t):
    centerx,centery=b['position'][0],b['position'][1]
    if centery == 19 or t[centery+1][centerx] != black:
        return True
    for i in range(3):
        dx=b['type'][i][0]+centerx
        dy=b['type'][i][1]+centery
        if dy == 19 or t[dy+1][dx] != black:
            return True
    return False

def appendTable(t,b):
    centerx,centery=b['position'][0],b['position'][1]
    t[centery][centerx]=b['color']
    for i in range(3):
        dx=b['type'][i][0]+centerx
        dy=b['type'][i][1]+centery
        t[dy][dx]=b['color']
        
def DownBlock(b,t):
    hitbottom=False
    centerx,centery=b['position'][0],b['position'][1]
    for i in range(centery,20):
        if t[i][centerx] != black:
            if t[i][centerx] != black:
                return [centerx,i-1]
        for j in range(3):
            dx=centerx+b['type'][j][0]
            dy=i+b['type'][j][1]
            if t[dy][dx] != black or dy==19:
                if t[dy][dx] != black:
                    return [centerx,i-1]
                else:
                    hitbottom=True
                    continue
        if hitbottom:
            return [centerx,i]
    return [centerx,19]
        
def scoring(t,score,m):
    s=score
    for i in range(20):
        if black not in t[i]:
            s+=1
            for j in range(i,0,-1):
                for k in range(10):
                    t[j][k]=(t[j-1][k][0],t[j-1][k][1],t[j-1][k][2])
    if s != score and m:
        scoreSound.play()
    return s

def isGameover(t):
    if t[0] != [black]*10:
        return True
    return False

def displayGameover():
    pygame.draw.rect(screen,black,(450,0,200,600),0)
    drawText('GAME',font,screen,(470,0))
    drawText('OVER',font,screen,(475,50))
    drawText('Play',font,screen,(480,130))
    drawText('Again',font,screen,(470,180))
    drawText('Press:Y',font,screen,(460,230))
    drawText('Leave',font,screen,(470,300))
    drawText('Press:N',font,screen,(460,350))
    drawText('See',font,screen,(490,450))
    drawText('Instruction',font,screen,(450,500))
    drawText('Press:K',font,screen,(460,550))

def playagain():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_y:
                    return
                if event.key == K_n:
                    terminate()
                if event.key == K_k:
                    return True

instruction()
pygame.display.update()
PressKey()

while True:
    showdifficulty()
    pygame.display.update()
    difficulty,level=selectdifficulty()
    time=0
    table=[[black]*10 for i in range(20)]
    score=0
    isScoring=False
    nowBlock=randBlock([4,0])
    nextBlock=randBlock((520,178))
    downBlock={'type':nowBlock['type'],'position':DownBlock(nowBlock,table)}
    Kleftdown=Krightdown=Kleft=Kright=Kdown=False
    if musicPlaying:
        pygame.mixer.music.play(-1)
    while True:
        screen.fill(black)
        score=scoring(table,score,musicPlaying)
        for i in range(20):
            for j in range(10):
                pygame.draw.rect(screen,white,(j*30+150,i*30,30,30),1)
        drawText('Lines',font,screen,(30,250))
        drawText('Next',font,screen,(490,100))
        drawText('%s'%(score),font,screen,(60,300))
        drawText('Level',font,screen,(30,50))
        drawText('%s'%(level),font,screen,(60,100))
        
        if isGameover(table):
            drawTable(table)
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT:
                    Kleft=True
                if event.key == K_RIGHT:
                    Kright=True
                if event.key == K_DOWN:
                    Kdown=True                
                if (event.key == K_UP or event.key == K_z)and rotatable(nextNrotate(nowBlock),table) and nowBlock['type'] != Type[0]:
                    Nrotate(nowBlock)
                if event.key == K_x and rotatable(nextProtate(nowBlock),table) and nowBlock['type'] != Type[0]:
                    Protate(nowBlock)
                if event.key == K_m:
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1)
                    musicPlaying=not musicPlaying
                if event.key == K_SPACE:
                    nowBlock['position']=downBlock['position']
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    Kleft=False
                if event.key == K_RIGHT:
                    Kright=False
                if event.key == K_DOWN:
                    Kdown=False
        if Kleft and Kdown:
            Kleftdown=True
            Kleft=Kdown=False
        if Kright and Kdown:
            Krightdown=True
            Kright=Kdown=False
        if Kleft and not moveable(nextmove(nowBlock,'left'),table):
            Kleft=False
        if Kright and not moveable(nextmove(nowBlock,'right'),table):
            Kright=False
        if Kdown and not moveable(nextmove(nowBlock,'down'),table):
            Kdown=False
        
        if Kleftdown and not moveable(nextmove(nowBlock,'leftdown'),table):
            Kleftdown=False
            Kdown=True
        if Krightdown and not moveable(nextmove(nowBlock,'rightdown'),table):
            Krightdown=False
            Kdown=True
        if not moveable(nextmove(nowBlock,'left'),table):
            Kleft=False
        if not moveable(nextmove(nowBlock,'right'),table):
            Kright=False
        if not moveable(nextmove(nowBlock,'down'),table):
            Kdown=False
        
        if Kleft:
            move_ip(nowBlock,'left')
        if Kright:
            move_ip(nowBlock,'right')
        if Kdown:
            move_ip(nowBlock,'down')
            time=0
        if Kleftdown:
            move_ip(nowBlock,'leftdown')
            Kleftdown=False
            Kleft=Kdown=True
            time=0
        if Krightdown:
            move_ip(nowBlock,'rightdown')
            Krightdown=False
            Kright=Kdown=True
            time=0
        downBlock['position']=DownBlock(nowBlock,table)
        drawTable(table)
        drawdownBlock(downBlock)
        drawnowBlock(nowBlock)
        drawnextBlock(nextBlock)
        if stopblock(nowBlock,table):
            appendTable(table,nowBlock)
            nowBlock={'type':nextBlock['type'],'color':nextBlock['color'],'position':[4,0]}
            downBlock={'type':nowBlock['type'],'position':DownBlock(nowBlock,table)}
            nextBlock=randBlock((520,178))
        if not Kdown and not Kleftdown and not Krightdown:
            time+=difficulty
        if time>=10 and moveable(nextmove(nowBlock,'down'),table):
            move_ip(nowBlock,'down')
            time=0
        pygame.display.update()
        mainClock.tick(10)
    pygame.mixer.music.stop()
    if musicPlaying:
        gameOverSound.play(-1)
    displayGameover()
    pygame.display.update()
    seeInstruction=False
    seeInstruction=playagain()
    gameOverSound.stop()
    if seeInstruction:
        instruction()
        pygame.display.update()
        PressKey()