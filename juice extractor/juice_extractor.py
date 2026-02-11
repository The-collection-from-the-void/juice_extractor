# -*- coding: gbk -*-
version="0.1 alpha 1 "

import pygame as pg
import player # type: ignore

#main
pg.init()
font=pg.font.Font("资源/字体/默认字体（华文楷体）.TTF")
main_window=pg.display.set_mode((800,600),pg.RESIZABLE | pg.SCALED)
pg.display.set_caption("榨汁机v. "+version) 
playerlist=[player.player(0,0,"juice extractor","资源/角色贴图/榨汁机/默认皮肤.bmp")]
this_player=playerlist[0]  

clock=pg.time.Clock()
running=1
while running:
    main_window.fill((0,0,0))
    for ev in pg.event.get():
        if ev.type==pg.QUIT:
            running=0
            break
        if ev.type==pg.VIDEORESIZE:
            main_window=pg.display.set_mode((ev.w, ev.h), pg.RESIZABLE)
    
    keys=pg.key.get_pressed()
    for i in range(len(keys)):
        if keys[i]:
            print(i)
    if keys[pg.K_w]:
        this_player.nowspeed[1]-=this_player.movespeed
    if keys[pg.K_s]:
        this_player.nowspeed[1]+=this_player.movespeed
    if keys[pg.K_a]:
        this_player.nowspeed[0]-=this_player.movespeed
    if keys[pg.K_d]:
        this_player.nowspeed[0]+=this_player.movespeed
    if keys[pg.K_k]:
        this_player.sprint(main_window)
    if keys[pg.K_r]:
        this_player.x=0
        this_player.y=0
    this_player.movespeed=5
    for i in playerlist:
        i.tick_refresh(main_window)    

    
    pg.display.update()
    clock.tick(60)

pg.quit()