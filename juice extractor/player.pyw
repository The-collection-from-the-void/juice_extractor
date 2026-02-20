# -*- coding: gbk -*-
import pygame as pg
pg.init()

def juice_extractor_animation_init(n:int):
    w=pg.Surface((11,2),pg.SRCALPHA)
    pg.draw.line(w,(255,255,255),((1+n if n<9 else 17-n) ,0),(5,0))
    pg.draw.line(w,(255,255,255),((9-n if n<9 else n-8) ,1),(5,1))
    return w 

class Key:
    def __init__(self,keys,event):
        try:
            self.keys = list(keys) 
        except:
            self.keys = [keys]
        self.event = event 
    def press(self,down_keys):
        r=1
        for key in self.keys:
            r=r and down_keys[key]
        return self.event if r else None
    def change(self,keys):
        self.keys = keys

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
        self.Key_binding=[Key(119,self.move_up),#绑定为w
                          Key(115,self.move_down),#绑定为s
                          Key(97,self.move_left),#绑定为a
                          Key(100,self.move_right),#绑定为d
                          Key(107,self.sprint)]#绑定为k
    def move_up(self):
        self.nowspeed[1]-=self.movespeed
    def move_down(self):
        self.nowspeed[1]+=self.movespeed
    def move_left(self):
        self.nowspeed[0]-=self.movespeed
    def move_right(self):
        self.nowspeed[0]+=self.movespeed
    #冲刺
    def sprint(self):
        self.animations.append(animation((32 if self.orientation else 80),
                                         0,1,
                                         [pg.image.load("resource/General effect of actions/Sprint effect.bmp")],
                                         (255,255,255),1,not self.orientation))
        if self.nowspeed==[0,0]:
            if self.orientation:
                self.nowspeed[0]=-1
            else:
                self.nowspeed[0]=1
        else:
            self.nowspeed[0]*=2
    #技能
    def Active_skills(self):#主动
        pass
    def passive_skill(self):#被动
        pass
    #刷新
    def tick_refresh(self,window,down_keys):
        if down_keys:
            for i in self.Key_binding:
                 f=i.press(down_keys)
                 if f:
                     f()
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
            image=i.get()
            if image:
                if self.orientation==0:
                    window.blit(image,(self.x+16-i.x,self.y+i.y),None)
                else:
                    window.blit(image,(self.x+i.x,self.y+i.y),None)
            else:
                del i
class animation:
    def __init__(self,x,y,velocity:int,images:list,transparent_color=None,life_span=-1,Mirror_flip=0):
        self.x=x
        self.y=y
        self.time=0
        self.velocity=velocity
        self.images=images
        self.life_span=life_span
        self.Mirror_flip=Mirror_flip
        if transparent_color:
              for image in images:
                  image.set_colorkey(transparent_color)
    def get(self):
        if self.time==self.life_span:
            return None
        self.time=self.time%(self.velocity*len(self.images))
        self.time+=1
        r_image=self.images[self.time//self.velocity-1]
        if self.Mirror_flip:
            r_image=pg.transform.flip(r_image,1,0)
        return r_image
