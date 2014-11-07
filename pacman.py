bif="./Pictures/bg.jpg"
pif="./Pictures/ball.png"
pdif="./Pictures/pacdes.png"
gif="./Pictures/ghost.png"

import pygame,sys,time
from pygame.locals import *
pygame.mixer.init()
cosound=pygame.mixer.Sound('./Audio/coin.wav')
diesound=pygame.mixer.Sound('./Audio/mariodie.wav')
winsound=pygame.mixer.Sound('./Audio/world_clear.wav')
thanksound=pygame.mixer.Sound('./Audio/thank.wav')
track=pygame.mixer.Sound('./Audio/track.ogg')

pygame.init()
screen=pygame.display.set_mode((1280,720),0,32)

background=pygame.image.load(bif).convert()
pac=pygame.image.load(pif).convert_alpha()
pacdes=pygame.image.load(pdif).convert_alpha()
gho=pygame.image.load(gif).convert_alpha()
	
pac=pygame.transform.scale(pac,(1280/35,720/15))
pacdes=pygame.transform.scale(pacdes,(1280/35,720/15))
gho=pygame.transform.scale(gho,(1280/35,720/15))


class Person():
	def __init__(self,i,j):
		self.i=i
		self.j=j
	def checkWall(self,x,y):
		f=1
		for i in walls:
			if i[0]==x*1280/35 and i[1]==y*720/15:
				f=0
				break
		return f
	def move(self,movex,movey):
		x=self.i
		y=self.j
		if x+movex<35 and x+movex>=0:	
			x+=movex
		if y+movey<15 and y+movey>=0:
			y+=movey
		if self.checkWall(x,y):
			self.i=x
			self.j=y
	def mov_this():
		raise NotImplementedError("Subclass must implement abstract method")

		
		
class Pacman(Person):
	def __init__(self,i,j):
		Person.__init__(self,i,j)
		self.src=pac
		self.score=0

	def changesrc(self):
		self.src=pacdes
	
	def __coinPop(self,i):
		coins.pop(i)
		cosound.play()
	def collectCoin(self):
		r=720/30
		for i in range(0,len(coins)):
			if (self.i*1280/35+r)==coins[i][0] and (self.j*720/15+r)==coins[i][1]:
				self.score+=1
				self.__coinPop(i)
				break	
	def checkGhost(self):
		global gamov
		ghos1=ghoobj1.ghostPosition()
		ghos2=ghoobj2.ghostPosition()
		if self.i==ghos1[0] and self.j==ghos1[1]:
			gamov=1
		if self.i==ghos2[0] and self.j==ghos2[1]:
			gamov=1

		
	
	def mov_this(self,event):
		global movex
		global movey
		if event.type==KEYDOWN:
			if event.key==K_LEFT or event.key==K_a:
				movex=-1
			elif event.key==K_RIGHT or event.key==K_d:
				movex=+1
			elif event.key==K_UP or event.key==K_w:
				movey=-1
			elif event.key==K_DOWN or event.key==K_s:
				movey=+1
		if event.type==KEYUP:
			if event.key==K_LEFT or event.key==K_a:
				movex=0
			elif event.key==K_RIGHT or event.key==K_d:
				movex=0
			elif event.key==K_UP or event.key==K_w:
				movey=0
			elif event.key==K_DOWN or event.key==K_s:
				movey=0
		self.move(movex,movey)
		self.collectCoin()
		self.checkGhost()

	
class Ghost(Person):
	def __init__(self,i,j):
		Person.__init__(self,i,j)
		self.src=gho
	def ghostPosition(self):
		return (self.i,self.j)
	def mov_this(self):
		movex,movey=0,0
		x=int(random.random()*100)%4
		if x==0:
			movex=1
		elif x==1:
			movex=-1
		elif x==2:
			movey=1
		elif x==3:
			movey=-1
		self.move(movex,movey)

	

track.play()
	

gamov=0
import random
movex,movey=0,0

coins=[]

walls=[]
r=720/30
for s in range(0,15):
	if s not in (6,7):
		x=11*1280/35
		y=s*720/15
		walls.append((x,y,1280/35,720/15))

for s in range(0,35):
	if s not in (9,10,20):
		x=s*1280/35
		y=8*720/15
		walls.append((x,y,1280/35,720/15))
	
yellow=(255,255,0)
brown=(51,0,0)	
green=(0,255,0)
blue=(0,0,255)
import random

no=1
while True:
	x,y=int(random.random()*100)%35,int(random.random()*100)%15
	f=0
	if x==0 and y==0:
		f=1
	if x==34 and y==14:
		f=1
	for i in walls:
		if x*1280/35==i[0] and y*720/15==i[1]:
			f=1
			break
	if f==0:
		coins.append((x*1280/35+r,y*720/15+r))
		no+=1
	if no==25:
		break
r=720/60
rat=0
pacobj=Pacman(0,0)
ghoobj1=Ghost(34,14)
ghoobj2=Ghost(34,0)
movex,movey=0,0
movex,movey=0,0
msg=''

def init():
	no=1
	track.stop()
	track.play()
	global coins
	coins=[]
	global r
	r=720/30
	while True:
		x,y=int(random.random()*100)%35,int(random.random()*100)%15
		f=0
		if x==0 and y==0:
			f=1
		if x==34 and y==14:
			f=1
		for i in walls:
			if x*1280/35==i[0] and y*720/15==i[1]:
				f=1
				break
		if f==0:
			coins.append((x*1280/35+r,y*720/15+r))
			no+=1
		if no==25:
			break
	global rat
	global pacobj
	global ghoobj1
	global ghoobj2
	global movex,movey
	global msg 
	global sou
	r=720/60
	rat=0
	pacobj=Pacman(0,0)
	ghoobj1=Ghost(34,14)
	ghoobj2=Ghost(34,0)
	movex,movey=0,0
	msg=''
	sou=0

msg=''
sou=0
while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			thanksound.play()
			time.sleep(2)
			pygame.quit()
			sys.exit()
		e=event
		pacobj.mov_this(e)
		if event.type==KEYDOWN:
			if event.key==K_q:
				thanksound.play()
				time.sleep(2)
				pygame.quit()
				sys.exit()
			if event.key==K_y and gamov==1:
				init()
				gamov=0
		
	
	rat+=1
	rat=rat%30
		
	screen.blit(background,(0,0))
	screen.lock()
	for i in walls:
		pygame.draw.rect(screen,brown,i)
	
	for i in coins:
		pygame.draw.circle(screen,yellow,i,r)
	if rat==0:
		ghoobj1.mov_this()
		ghoobj2.mov_this()
		pacobj.move(movex,movey)
		pacobj.collectCoin()
	screen.unlock()
	
	font = pygame.font.Font(None, 60)
	if gamov!=1:
		sc="Score:"+str(pacobj.score)
	text = font.render(sc, 1, blue)	
	textpos = text.get_rect(centerx=1200)
	screen.blit(text, textpos)
	pacobj.checkGhost();

	if coins==[]:
		gamov=1
	if gamov==1:
		po=sc
		font = pygame.font.Font(None, 150)
		track.stop()
		if coins!=[]:
			msg="GAME OVER(press Y)"
			pacobj.changesrc()
			if sou==0:
				diesound.play()
				sou=1
		elif msg!="GAME OVER(press Y)":
			msg="YOU WIN(press Y)"
			if sou==0:
				winsound.play()
				sou=1
		text = font.render(msg, 1, green)	
		textpos = text.get_rect(centerx=1280/2)
		screen.blit(text, textpos)


	screen.blit(pacobj.src,((pacobj.i*1280)/35,(pacobj.j*720)/15))
	screen.blit(ghoobj1.src,((1280*ghoobj1.i)/35,(720*ghoobj1.j)/15))
	screen.blit(ghoobj2.src,((1280*ghoobj2.i)/35,(720*ghoobj2.j)/15))

	
	 
	 
	 
	 
	 
	 
	 
		
	  	
	

	pygame.display.update()

