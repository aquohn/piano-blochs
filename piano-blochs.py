# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 23:37:39 2019

@author: aquohn
"""

import pygame
from pygame.locals import *
from qiskit import *
from qiskit.tools.visualization import plot_bloch_multivector
from qiskit.quantum_info.states import Statevector
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from numpy import pi

TURN_FRAMES = 4        
B_FIELD = 0.001
SCREEN_WIDTH=640
SCREEN_HEIGHT=650
X_COLOR = "green"
Y_COLOR = "orange"
Z_COLOR = "blue"

class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

pygame.init()

sv_arr = np.array([1,0])
z1 = [0,1]
circuit = QuantumCircuit(1,1) #1 qubit and 1 classical bit
simulator = Aer.get_backend('statevector_simulator')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

clock = pygame.time.Clock()

time_delay = 3000 #milliseconds
time_delay_out = 1000

time0 = int(pygame.time.get_ticks())

#Song stuff:
timing = [5000, 7000]
list = np.array([[1,0], [1, 0]])

checklist=np.zeros(len(list))

combo=0
combotext=str()
score = 0

# Getting the wav
song = pygame.mixer.Sound("testes.wav") #use wav is best apparently

pygame.mixer.music.load('testes.wav')
pygame.mixer.music.play(0) #i think 0 = play 1 time, 1 is for 2 times, -1 is for infinite

maxscore = 1000000
score_per_note = maxscore/len(list)

# Rotation stuff
xcnt = 0
ycnt = 0
zcnt = 0
x_ax_x = y_ax_y = z_ax_z = 1.8
x_ax_y = x_ax_z = y_ax_x = y_ax_z = z_ax_x = z_ax_y = 0

while running:
    screen.fill((0, 0, 0))
    
    time = int(pygame.time.get_ticks())-time0
    
    # Initialization
    circuit = QuantumCircuit(1,1) #1 qubit and 1 classical bit
    sv_arr = np.array([sv_arr[0]+B_FIELD, sv_arr[1]])
    sv_arr = sv_arr/((abs(sv_arr[0]))**2+(abs(sv_arr[1]))**2)**0.5
    circuit.initialize(sv_arr, 0)

    circuit.u3(0,0,0.3,0)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_a:
                xcnt += TURN_FRAMES
            elif event.key == K_s:
                ycnt += TURN_FRAMES
            elif event.key == K_d:
                zcnt += TURN_FRAMES
            elif event.key == K_RETURN:
                circuit.measure([0],[0])
                backend = Aer.get_backend('qasm_simulator')
                result = execute(circuit,backend=backend,shots = 1).result()
                counts = result.get_counts()
                for key in counts:
                    sv_arr[int(key)] = 1
                    sv_arr[1-int(key)] = 0
                # Check if statevector coincides with point here


                # OSU!!!
                hit = 0 #check if there is a valid hit (no double counting)
                for i in range(len(timing)): #find the closest beat timing[i] that is after current time, and the associated time diff
                    if timing[i] > time: #check that the note is later than current time
                        if timing[i]- time > time - timing[i-1]:
                            time_diff = time - timing[i-1] #late for the i-1 the note
                            if checklist[i-1] == 1: #check if note is already played
                                break
                            else:
                                checklist[i-1] = 1
                                hit = 1
                        else:
                            time_diff = timing[i] - time #early for the ith note
                            if checklist[i] == 1: #check if note is already played
                                break
                            else:
                                checklist[i] = 1
                                hit = 1
                    elif timing[i] == timing[-1]: #accounting for last note
                        time_diff = time - timing[i] #late for the last note
                        if checklist[i] == 1: #check if note is already played
                            break
                        else:
                            checklist[i] = 1
                            hit = 1
                if hit == 1:
                    #measure state, return probability of getting point? +z? as probability

                    if time_diff < time+500: #if timing is early
                        combo = 0
                        combotext = "MISS!"
                    elif time_diff > time-500: #if timing is late
                        combo = 0
                        combotext = "MISS!"
                    else: 
                        if int(key) == 0: # (1/(1+time_diff) * probability)<0.5:
                            combo = 0
                            combotext = "MISS!"
                        else:
                            combo += 1
                            score += 1/(1+time_diff)*score_per_note
                            combotext = str(combo)
                else:
                    combo = 0
                    combotext = "MISS!"

        elif event.type == QUIT:
            running = False



#        elif event.type == QUIT:
#            running = False
    
    if xcnt > 0:
        circuit.rx(pi / TURN_FRAMES, 0)
        xcnt -= 1 
    if ycnt > 0:
        circuit.ry(pi / TURN_FRAMES, 0)
        ycnt -= 1
    if zcnt > 0:
        circuit.rz(pi / TURN_FRAMES, 0)
        zcnt -= 1
    
    fig = plt.figure(figsize=(10,10))
    #ax = plt.gca(projection='3d')
    ax = Axes3D(fig)
    ax._axis3don = False
    ax.set_xlim3d(-1.3, 1.3)
    ax.set_ylim3d(-1.3, 1.3)
    ax.set_zlim3d(-1.3, 1.3)
    
    # z-axis
    ax.plot([-z_ax_x, z_ax_x], [-z_ax_y, z_ax_y], [-z_ax_z, z_ax_z], color=Z_COLOR)
    ax.text(z_ax_x, z_ax_y, z_ax_z, " + z", color=Z_COLOR)
    ax.text(-z_ax_x, -z_ax_y, -z_ax_z, " - z", color=Z_COLOR)
    
    # y-axis
    ax.plot([-y_ax_x, y_ax_x], [-y_ax_y, y_ax_y], [-y_ax_z, y_ax_z], color=Y_COLOR)
    ax.text(y_ax_x, y_ax_y, y_ax_z, " + y", color=Y_COLOR)
    ax.text(-y_ax_x, -y_ax_y, -y_ax_z, " - y", color=Y_COLOR)
    
    # x-axis
    ax.plot([-x_ax_x, x_ax_x], [-x_ax_y, x_ax_y], [-x_ax_z, x_ax_z], color=X_COLOR)
    ax.text(x_ax_x, x_ax_y, x_ax_z, " + x", color=X_COLOR)
    ax.text(-x_ax_x, -x_ax_y, -x_ax_z, " - x", color=X_COLOR)
    
    # TODO: use 3d rotation matrices to rotate the axes
    
    #ax.set_aspect("equal")

    # draw sphere
    u, v = np.mgrid[0:2*pi:50j, 0:pi:25j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, color=(0,0,0,0.2))

    result = execute(circuit, backend = simulator).result()
    sv_arr = result.get_statevector()
    z1 = [0,-np.real(1-2*np.conj(sv_arr[0])*sv_arr[0])]
    x1 = [0,2*(np.real(sv_arr[0])*np.real(sv_arr[1])+np.imag(sv_arr[0])*np.imag(sv_arr[1]))]
    y1 = [0,2*(np.imag(sv_arr[0])*np.real(sv_arr[1])+np.real(sv_arr[0])*np.imag(sv_arr[1]))]
    n = (x1[1]**2+y1[1]**2+z1[1]**2)**0.5
    a = Arrow3D(x1/n, y1/n, z1/n, mutation_scale=20,
            lw=1, arrowstyle="-|>", color='r')
    ax.add_artist(a)

    #add points for the rhythm
    for i in range(len(timing)):
        if timing[i] - time < time_delay and time < timing[i]: #fade in
#             plot point list[i] on bloch sphere with opacity = 1- (timing[i]-time)/time delay
            
            z1 = [0,-np.real(1-2*np.conj(list[i][0])*list[i][0])]
            x1 = [0,2*(np.real(list[i][0])*np.real(list[i][1])+np.imag(list[i][0])*np.imag(list[i][1]))]
            y1 = [0,2*(np.imag(list[i][0])*np.real(list[i][1])+np.real(list[i][0])*np.imag(list[i][1]))]
            n = (x1[1]**2+y1[1]**2+z1[1]**2)**0.5
            ax.scatter(x1,y1,z1, s=500, c='b', alpha = 1- (timing[i]-time)/time_delay)
            #,alpha = 1- (timing[i]-time)/time_delay
#             ax.add_artist(a)
#             print(str(time)+"Yes")
        elif time - timing[i] < time_delay_out and time > timing[i]: #fade out
#             plot point list[i] on bloch sphere with opacity = 1- (time - timing[i])/time delay out

            z1 = [0,-np.real(1-2*np.conj(list[i][0])*list[i][0])]
            x1 = [0,2*(np.real(list[i][0])*np.real(list[i][1])+np.imag(list[i][0])*np.imag(list[i][1]))]
            y1 = [0,2*(np.imag(list[i][0])*np.real(list[i][1])+np.real(list[i][0])*np.imag(list[i][1]))]
            n = (x1[1]**2+y1[1]**2+z1[1]**2)**0.5
            ax.scatter(x1,y1,z1, s=500, c='b',alpha = 1- (time - timing[i])/time_delay_out)
#             print(str(time)+"No")
        else:
            continue

    plt.savefig('bloch.tiff')
    #     A = plot_bloch_multivector(statevector)
    #     A.savefig('bloch.png')
    surf = pygame.image.load("bloch.tiff")
    screen.blit(surf,(0,0))

    font = pygame.font.SysFont('comicsans', 30, True)
    timetext = font.render("Time: " + str(time), 1, (0,0,0)) 
    combotext2 = font.render("Combo: " + str(combotext), 1, (0,0,0))
    #scoretext = font.render()
    screen.blit(timetext, (0, 0))
    screen.blit(combotext2, (200, 0))

    pygame.display.flip()
    
    clock.tick(30)
    plt.close(fig)

pygame.quit()
