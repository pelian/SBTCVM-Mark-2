#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import libSBTCVM
import libbaltcalc
pygame.font.init()
pygame.mixer.init()
#libvmui
#this library handles many graphical tasks, as well as containing
#functions for many tools and features found in the menus and in MK2-TOOLS
#even the VM pause menu is in here.

#fonts
simplefont = pygame.font.SysFont(None, 16)
simplefontA = pygame.font.SysFont(None, 20)
simplefontB = pygame.font.SysFont(None, 22)

simplefontC = pygame.font.SysFont(None, 32)
smldispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)
lgdispfont = pygame.font.Font(os.path.join("VMSYSTEM", "SBTCVMreadout.ttf"), 16)


#these use the same squarewave generator as SBTCVM's buzzer.
#sound A
menusound1=pygame.mixer.Sound(libSBTCVM.autosquare(300, 0.1))
#menu select sound
menusound2=pygame.mixer.Sound(libSBTCVM.autosquare(250, 0.1))
#clock widget second sound
menusound3=pygame.mixer.Sound(libSBTCVM.autosquare(280, 0.1))

def initui(scsurf, kiomode):
	global screensurf
	screensurf=scsurf
	global vmlaunchbg
	global KIOSKMODE
	global GNDlamp
	global POSlamp
	global NEGlamp
	global CPULEDSTANDBY
	global LEDGREENOFF
	global GFXLOGO
	global CREDITHBAR
	global vmtoolsbg
	global vmtoolsbgfull
	global vmbg
	global sbtccat
	KIOSKMODE=kiomode
	vmtoolsbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-TOOLS.png')).convert_alpha()
	vmtoolsbgfull=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-TOOLS_FULL.png')).convert()
	vmbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VMBG.png')).convert()
	vmlaunchbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-PAUSEMASK.png')).convert_alpha()
	GNDlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampGND.png')).convert()
	POSlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampPOS.png')).convert()
	NEGlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampNEG.png')).convert()
	GFXLOGO=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'GFXLOGO-CAT.png')).convert()
	CREDITHBAR=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'CREDITHBAR.png')).convert()
	#indicator lamps
	#GREEN
	#LEDGREENON=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN.png')).convert()
	LEDGREENOFF=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-GREEN-OFF.png')).convert()
	#CPU
	#CPULEDACT=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-BLUE.png')).convert()
	CPULEDSTANDBY=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'LAMP-ORANGE.png')).convert()
	sbtccat=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'SBTCCAT34.png')).convert()




#Balanced ternary clock function. (shows clock that is in the extras menu.
def BTCLOCKDATE():
	
	loopend=0
	hourY=227
	minY=227
	secY=227
	ttextY=204
	helplab = simplefontB.render(('''Red=-, violet=0 blue=+'''), True, (255, 255, 255))
	screensurf.blit(helplab, (3, 120))
	prevtime=None
	#quick fix to solve drawing glitches
	scbak=screensurf.copy()
	while loopend==0:
		
		#screensurf.fill((127, 127, 127))
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
				break
			elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
				loopend=1
			if event.type == QUIT:
				loopend=1
		screensurf.blit(scbak, (0, 0))
		pygame.event.clear()
		curtim=time.localtime()
		hourdec=curtim[3]
		mindec=curtim[4]
		secdec=curtim[5]
		if prevtime!=secdec:
			menusound3.play()
		prevtime=secdec
		hourbt=libSBTCVM.trunkto4(libbaltcalc.DECTOBT(hourdec))
		minbt=libSBTCVM.trunkto5(libbaltcalc.DECTOBT(mindec))
		secbt=libSBTCVM.trunkto5(libbaltcalc.DECTOBT(secdec))
		hourX=3
		hourtext = simplefont.render(("Hr. " + str(hourdec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(hourtext, (hourX, ttextY))
		for fxg in hourbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (hourX, hourY))
			if fxg=="+":
				screensurf.blit(POSlamp, (hourX, hourY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (hourX, hourY))
			hourX += 9
		minX=(hourX + 9)
		mintext = simplefont.render(("Min. " + str(mindec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(mintext, (minX, ttextY))
		for fxg in minbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (minX, minY))
			if fxg=="+":
				screensurf.blit(POSlamp, (minX, minY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (minX, minY))
			minX += 9
		secX=(minX + 9)
		sectext = simplefont.render(("Sec. " + str(secdec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(sectext, (secX, ttextY))
		for fxg in secbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (secX, secY))
			if fxg=="+":
				screensurf.blit(POSlamp, (secX, secY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (secX, secY))
			secX += 9
		pygame.display.update()