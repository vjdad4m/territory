#!/usr/bin/env python

import pygame
import random

pygame.init()
pygame.mixer.init()

with open("kerdesek.txt", "r", encoding="utf-8") as f:
    kerdesek = f.read().split('\n')

if kerdesek[len(kerdesek)-1] == '':
    kerdesek.pop(len(kerdesek)-1)

random.shuffle(kerdesek)

clock = pygame.time.Clock()

font_sz = 64

display_width, display_height = 1920, 1080

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Territory")

bp_map = pygame.image.load('assets/bp.png')

bp_map = pygame.transform.scale(bp_map, tuple(map(int, (bp_map.get_width() // 1.4, bp_map.get_height() // 1.4))))

font_sz = 36
font = pygame.font.Font('assets/robotocondensed.ttf', font_sz)
    
bp_map_rect = bp_map.get_rect(center=(display_width/2+60, display_height/2))

current_pixel_color = 255

kerulet = [True]*25

isQuestionShowing = False
currentQuestion = 0
currentTeam = 0

teamColors = [(255, 128, 128), (128, 255, 128), (128, 128, 255)]

cAnswer = 0

sound_correct = pygame.mixer.Sound("assets/correct.wav")
sound_incorrect = pygame.mixer.Sound("assets/incorrect.wav")

sound_correct.set_volume(1)
sound_incorrect.set_volume(1)

score = [0, 0, 0]

running = True
while running:
    display.fill((255, 255, 255))
    
    if not isQuestionShowing:
        display.blit(bp_map, bp_map_rect)
        pygame.draw.circle(display, (0, 0, 0), (display_width - display_width // 6, display_height // 8), 48)
        pygame.draw.circle(display, teamColors[currentTeam], (display_width - display_width // 6, display_height // 8), 44)
    
    current_pixel_color = display.get_at(pygame.mouse.get_pos())[0]

    pygame.draw.circle(display, teamColors[0], (60, display_height // 2 - font_sz * 3), font_sz) 
    pygame.draw.circle(display, teamColors[1], (60, display_height // 2), font_sz) 
    pygame.draw.circle(display, teamColors[2], (60, display_height // 2 + font_sz * 3), font_sz) 

    sc_t_1 = font.render(str(score[0]), True, (0, 0, 0))
    sc_t_2 = font.render(str(score[1]), True, (0, 0, 0))
    sc_t_3 = font.render(str(score[2]), True, (0, 0, 0))

    display.blit(sc_t_1, (60 + font_sz * 1.5, display_height // 2 - font_sz * 3 - font_sz // 2))
    display.blit(sc_t_2, (60 + font_sz * 1.5, display_height // 2 - font_sz // 2))
    display.blit(sc_t_3, (60 + font_sz * 1.5, display_height // 2 + font_sz * 3 - font_sz // 2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not isQuestionShowing and 0 < current_pixel_color < 25 and kerulet[current_pixel_color]:
                    isQuestionShowing = True
                    chosenDistrict = current_pixel_color
                elif isQuestionShowing:
                    if mousePixel == cAnswer:
                        sound_correct.play()
                        isQuestionShowing = False
                        kerulet[chosenDistrict] = False
                        pxarray = pygame.PixelArray(bp_map)
                        pxarray.replace((chosenDistrict, chosenDistrict, chosenDistrict), teamColors[currentTeam][::-1])
                        del pxarray
                        currentQuestion += 1
                        currentTeam += 1
                        score[currentTeam - 1] += 100
                    elif mousePixel in [1, 2, 3, 4]:
                        sound_incorrect.play()
                        isQuestionShowing = False
                        currentQuestion += 1
                        currentTeam += 1
    
    currentTeam = currentTeam % 3
    
    if isQuestionShowing:
        pygame.draw.rect(display, teamColors[currentTeam], pygame.Rect(60, 60, display_width-120, display_height-120),  0, 40)
        
        pygame.draw.rect(display, (1, 1, 1), pygame.Rect(display_width // 12,                                                           display_height - display_height // 1.5, display_width // 2 - display_width // 8, display_height // 4),  0, 40)
        pygame.draw.rect(display, (2, 2, 2), pygame.Rect(display_width - display_width // 2 + display_width // 8 - display_width // 12, display_height - display_height // 1.5, display_width // 2 - display_width // 8, display_height // 4),  0, 40)
        pygame.draw.rect(display, (3, 3, 3), pygame.Rect(display_width // 12,                                                           display_height - display_height // 2.8, display_width // 2 - display_width // 8, display_height // 4),  0, 40)
        pygame.draw.rect(display, (4, 4, 4), pygame.Rect(display_width - display_width // 2 + display_width // 8 - display_width // 12, display_height - display_height // 2.8, display_width // 2 - display_width // 8, display_height // 4),  0, 40)
        
        c_question = kerdesek[currentQuestion].split('|')
        cAnswer = int(c_question[5])
        
        
        if len(c_question[0]) > 50:
            c_qsplit = c_question[0].split()
            if len(c_qsplit) > 6:
                t_p1 = ' '.join(c_qsplit[:6])
                t_p2 = ' '.join(c_qsplit[6:])

                t_question = font.render(t_p1, True, (0, 0, 0))
                t_question_rect = t_question.get_rect()
                t_question_rect.center = (display_width // 2, 120)

                t_question2 = font.render(t_p2, True, (0, 0, 0))
                t_question2_rect = t_question2.get_rect()
                t_question2_rect.center = (display_width // 2, 120 + font_sz * 1.5)

                display.blit(t_question, t_question_rect)
                display.blit(t_question2, t_question2_rect)

            else:
                t_question = font.render(c_question[0], True, (0, 0, 0))
                t_question_rect = t_question.get_rect()
                t_question_rect.center = (display_width // 2, 120)
                display.blit(t_question, t_question_rect)
        
        else:
            t_question = font.render(c_question[0], True, (0, 0, 0))
            t_question_rect = t_question.get_rect()
            t_question_rect.center = (display_width // 2, 120)
            display.blit(t_question, t_question_rect)

            
        t_ans1 = font.render(c_question[1], True, (255, 255, 255))
        t_ans2 = font.render(c_question[2], True, (255, 255, 255))
        t_ans3 = font.render(c_question[3], True, (255, 255, 255))
        t_ans4 = font.render(c_question[4], True, (255, 255, 255))
        
        t_ans1_rect = t_ans1.get_rect()
        t_ans2_rect = t_ans2.get_rect()
        t_ans3_rect = t_ans3.get_rect()
        t_ans4_rect = t_ans4.get_rect()
        
        offsetx = (display_width // 2 - display_width // 8) / 2
        offsety = display_height // 8
        
        t_ans1_rect.center = (display_width // 12 + offsetx,   display_height - display_height // 1.5 + offsety)
        t_ans2_rect.center = (display_width - display_width // 2 + display_width // 8 - display_width // 12 + offsetx, display_height - display_height // 1.5 + offsety)
        t_ans3_rect.center = (display_width // 12 + offsetx, display_height - display_height // 2.8 + offsety)
        t_ans4_rect.center = (display_width - display_width // 2 + display_width // 8 - display_width // 12 + offsetx, display_height - display_height // 2.8 + offsety)
        
        mousePixel = display.get_at(pygame.mouse.get_pos())[0]       
        
        display.blit(t_ans1, t_ans1_rect)
        display.blit(t_ans2, t_ans2_rect)
        display.blit(t_ans3, t_ans3_rect)
        display.blit(t_ans4, t_ans4_rect)
                
    currentQuestion = currentQuestion % len(kerdesek)
        
    pygame.display.update()
    clock.tick(30)
