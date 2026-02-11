# -*- coding: gbk -*-
import pygame as pg
pg.init()

def juice_extractor_animation_init(n:int):
    w=pg.Surface((11,2),pg.SRCALPHA)
    pg.draw.line(w,(255,255,255),((1+n if n<9 else 17-n) ,0),(5,0))
    pg.draw.line(w,(255,255,255),((9-n if n<9 else n-8) ,1),(5,1))
    return w

class player:
    def __init__(self,x,y,job:str,chartlet:str):
        self.x=x
        self.y=y
        self.job=job
        self.movespeed=5
        self.nowspeed=[0,0] #[x,y]
        self.orientation=1 #1:left,0:right
        self.chartlet=pg.image.load(chartlet)
        self.chartlet.set_colorkey((255,255,255))
        self.animations=[animation(5,33,6,[juice_extractor_animation_init(i) for i in range(18)]) if self.job=="juice extractor"  else animation(0,0,0,[])]
    def sprint(self,window):
        effects=pg.image.load("资源/通用动作效果/冲刺效果.bmp")
        effects.set_colorkey((255,255,255))
        if self.orientation:
            window.blit(effects,(self.x+32,self.y))
        else:
            effects=pg.transform.flip(effects,1,0)
            window.blit(effects,(self.x-64,self.y))
        if self.nowspeed==[0,0]:
            if self.orientation:
                self.nowspeed[0]=-16
            else:
                self.nowspeed[0]=16
        else:
            self.nowspeed[0]*=2
    def Active_skills(self):
        pass
    def passive_skill(self):
        pass
    def tick_refresh(self,window):
        self.passive_skill()
        self.nowspeed=[self.nowspeed[0]*0.75,self.nowspeed[1]*0.75]
        if self.nowspeed[0]>16:
            self.nowspeed[0]=16
        elif self.nowspeed[0]<-16:
            self.nowspeed[0]=-16
        if self.nowspeed[1]>16:
            self.nowspeed[1]=16
        elif self.nowspeed[1]<-16:
            self.nowspeed[1]=-16
        self.x+=self.nowspeed[0]
        self.y+=self.nowspeed[1]
        if self.orientation==1 and self.nowspeed[0]>0:
            self.chartlet=pg.transform.flip(self.chartlet,1,0)
            self.orientation=0
        elif self.orientation==0 and self.nowspeed[0]<0:
            self.chartlet=pg.transform.flip(self.chartlet,1,0)
            self.orientation=1
        self.draw(window)
    def draw(self,window):
        window.blit(self.chartlet,(self.x,self.y),None)
        for i in self.animations:
            if self.orientation==0:
                window.blit(i.get(),(self.x+16-i.x,self.y+i.y),None)
            else:
                window.blit(i.get(),(self.x+i.x,self.y+i.y),None)

class animation:
    def __init__(self,x,y,velocity:int,images:list):
        self.x=x
        self.y=y
        self.time=0
        self.velocity=velocity
        self.images=images
    def get(self):
        self.time+=1
        self.time=self.time%(self.velocity*len(self.images))
        return self.images[self.time//self.velocity]
