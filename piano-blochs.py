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
EASY = 10
BPM = 119
B_FIELD = 0.03
SCREEN_WIDTH=640
SCREEN_HEIGHT=650
X_COLOR = "green"
Y_COLOR = "orange"
Z_COLOR = "blue"
hit = 0
TAPZONE = [[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]]
xs,ys,zs = list(), list(), list()

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
list = np.array([[0.6,0.8], [-0.8, 0.6]])
note_time_arr = np.floor(((np.array(range(70)) + 1) * EASY/BPM * 60 + 2) * 1000)
checklist=np.zeros(len(note_time_arr))

# Generate note distribution for each note
rand = QuantumCircuit(6,6)
rand.h([0,1,2,3,4,5])
for i in range(len(note_time_arr)):
    rand.measure([0,1,2,3,4,5],[0,1,2,3,4,5])
    counts = execute(rand,backend=simulator,shots=1).result().get_counts()
    for key in counts:
        a = key
        b = [pos for pos, i in enumerate(key) if i == 1]
        if len(b) == 0:
            xs = TAPZONE[:][0]
            ys = TAPZONE[:][1]
            zs = TAPZONE[:][2]
        else:
            c = np.array([TAPZONE[i] for i in b])
            xs.append(np.array([TAPZONE[i][0] for i in b]))
            ys.append(np.array([TAPZONE[i][1] for i in b]))
            zs.append(np.array([TAPZONE[i][2] for i in b]))

combo=0
combotext=str()
score = 0

# Getting the wav
song = pygame.mixer.Sound("testes.wav") #use wav is best apparently

pygame.mixer.music.load('testes.wav')
pygame.mixer.music.play(0) #i think 0 = play 1 time, 1 is for 2 times, -1 is for infinite

MAXSCORE = 1000000
SCORE_PER_NOTE = MAXSCORE/len(note_time_arr)

# Rotation stuff
xcnt = 0
ycnt = 0
zcnt = 0
x_ax_x = y_ax_y = z_ax_z = 1.8
x_ax_y = x_ax_z = y_ax_x = y_ax_z = z_ax_x = z_ax_y = 0
rot = 0.5
rotfactor = 1
theta = pi / TURN_FRAMES

# 3D rotation matrices
rotX = np.array([[1, 0, 0],
                [0, np.cos(theta), np.sin(theta)],
                [0, -np.sin(theta), np.cos(theta)]])
rotY = np.array([[np.cos(theta), 0, -np.sin(theta)],
                [0, 1, 0],
                [np.sin(theta), 0, np.cos(theta)]])
rotZ = np.array([[np.cos(theta), np.sin(theta), 0],
                [-np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]])

while running:
    screen.fill((0, 0, 0))
    
    time = int(pygame.time.get_ticks())-time0
    
    # Initialization
    circuit = QuantumCircuit(1,1) #1 qubit and 1 classical bit
    sv_arr = np.array([sv_arr[0]+B_FIELD, sv_arr[1]])
    sv_arr = sv_arr/((abs(sv_arr[0]))**2+(abs(sv_arr[1]))**2)**0.5
    circuit.initialize(sv_arr, 0)

    circuit.u3(0,0,rot*rotfactor,0)
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
                hit = 1

                # Check if statevector coincides with point here

                # OSU!!!
                hit = 0 #check if there is a valid hit (no double counting)
                for i in range(len(note_time_arr)): #find the closest beat note_time_arr[i] that is after current time, and the associated time diff
                    if note_time_arr[i] > time: #check that the note is later than current time
                        if note_time_arr[i] - time > time - note_time_arr[i-1]:
                            time_diff = time - note_time_arr[i-1] #late for the i-1 the note
                            if checklist[i-1] == 1: #check if note is already played
                                break
                            else:
                                checklist[i-1] = 1
                                hit = 1
                        else:
                            time_diff = note_time_arr[i] - time #early for the ith note
                            if checklist[i] == 1: #check if note is already played
                                break
                            else:
                                checklist[i] = 1
                                hit = 1
                    elif note_time_arr[i] == note_time_arr[-1]: #accounting for last note
                        time_diff = time - note_time_arr[i] #late for the last note
                        if checklist[i] == 1: #check if note is already played
                            break
                        else:
                            checklist[i] = 1
                            hit = 1
                            
                if hit == 1:
                    #measure state, return probability of getting point? +z? as probability
                    if abs(time_diff) > 1000: #if note_time_arr is early
                        combo = 0
                        combotext = "MISS!"
                    elif int(key)==1:  # (1/(1+time_diff) * probability)<0.5:
                        combo = 0
                        combotext = "MISS!"
                    else:
                        combo += 1
                        score += 1/(1+time_diff)*SCORE_PER_NOTE
                        combotext = str(combo)
                else:
                    combo = 0
                    combotext = "MISS!"
        elif event.type == QUIT:
            running = False

    if hit == 1 and time < timing[0] - 1000:
        continue
    elif hit == 0 and time > timing[0] + 1000:
        combo = 0
        combotext = "MISS!"
        np.delete(timing,0)
    elif hit == 1 and abs(time - timing[0]) < 500 and 1-int(key) in zs:
        combo += 1
        combotext = "PERFECT!"
        score += 1/(1+abs(time-timing[0]))*score_per_note
        np.delete(timing,0)
        hit = 0
    elif hit == 1 and abs(time - timing[0]) < 1000 and 1-int(key) in zs:
        combo += 1
        combotext = "GREAT!"
        score += 1/(1+abs(time-timing[0]))*score_per_note
        np.delete(timing,0)
        hit = 0
    elif hit == 1 and abs(time - timing[0]) < 1000 and 1-int(key) not in zs:
        combo = 0
        combotext = "MISS!"
        np.delete(timing,0)
        hit = 0
    
    # Rotation
    if xcnt > 0:
        # axis rotation
        x_ax_arr = np.matmul(rotX, np.array([x_ax_x, x_ax_y, x_ax_z]))
        y_ax_arr = np.matmul(rotX, np.array([y_ax_x, y_ax_y, y_ax_z]))
        z_ax_arr = np.matmul(rotX, np.array([z_ax_x, z_ax_y, z_ax_z]))

        x_ax_y = x_ax_arr[1]
        x_ax_z = x_ax_arr[2]
        y_ax_y = y_ax_arr[1]
        y_ax_z = y_ax_arr[2]
        z_ax_y = z_ax_arr[1]
        z_ax_z = z_ax_arr[2]
        
        # state vector rotation
        circuit.rx(theta, 0)

        xcnt -= 1 

    if ycnt > 0:
        # axis rotation
        x_ax_arr = np.matmul(rotY, np.array([x_ax_x, x_ax_y, x_ax_z]))
        y_ax_arr = np.matmul(rotY, np.array([y_ax_x, y_ax_y, y_ax_z]))
        z_ax_arr = np.matmul(rotY, np.array([z_ax_x, z_ax_y, z_ax_z]))

        x_ax_x = x_ax_arr[0]
        x_ax_z = x_ax_arr[2]
        y_ax_x = y_ax_arr[0]
        y_ax_z = y_ax_arr[2]
        z_ax_x = z_ax_arr[0]
        z_ax_z = z_ax_arr[2]

        # state vector rotation
        circuit.ry(theta, 0)

        ycnt -= 1

    if zcnt > 0:
        # axis rotation
        x_ax_arr = np.matmul(rotZ, np.array([x_ax_x, x_ax_y, x_ax_z]))
        y_ax_arr = np.matmul(rotZ, np.array([y_ax_x, y_ax_y, y_ax_z]))
        z_ax_arr = np.matmul(rotZ, np.array([z_ax_x, z_ax_y, z_ax_z]))

        x_ax_x = x_ax_arr[0]
        x_ax_y = x_ax_arr[1]
        y_ax_x = y_ax_arr[0]
        y_ax_y = y_ax_arr[1]
        z_ax_x = z_ax_arr[0]
        z_ax_y = z_ax_arr[1]

        # state vector rotation
        circuit.rz(theta, 0)

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
    rotfactor = abs(z1[1]) + 0.05
    x1 = [0,2*(np.real(sv_arr[0])*np.real(sv_arr[1])+np.imag(sv_arr[0])*np.imag(sv_arr[1]))]
    y1 = [0,2*(np.imag(sv_arr[0])*np.real(sv_arr[1])+np.real(sv_arr[0])*np.imag(sv_arr[1]))]
    n = (x1[1]**2+y1[1]**2+z1[1]**2)**0.5
    a = Arrow3D(x1/n, y1/n, z1/n, mutation_scale=20,
            lw=1, arrowstyle="-|>", color='r')
    ax.add_artist(a)

    #add points for the rhythm
    for i in range(len(note_time_arr)):
        if note_time_arr[i] - time < time_delay and time < note_time_arr[i]: #fade in
#             plot point list[i] on bloch sphere with opacity = 1- (note_time_arr[i]-time)/time delay
            ax.scatter(xs[i],ys[i],zs[i], s=200, color=(0.5,0,1,1-(note_time_arr[i]-time)/time_delay)) 
            #,alpha = 1- (note_time_arr[i]-time)/time_delay
#             ax.add_artist(a)
#             print(str(time)+"Yes")
        elif time - note_time_arr[i] < time_delay_out and time > note_time_arr[i]: #fade out
#             plot point list[i] on bloch sphere with opacity = 1- (time - note_time_arr[i])/time delay out
            ax.scatter(xs[i],ys[i],zs[i], s=200, color=(0.5,0,1,1- (time - note_time_arr[i])/time_delay_out)) 
#             print(str(time)+"No")
        else:
            continue
    RandomEventGenerator(simulator)
#    if timing[0] - time < time_delay and time < timing[0]: #fade in
#        ax.scatter(xs,ys,zs, s=200, color=(0.5,0,1,1/len(xs)-(timing[0]-time)/time_delay))
#    elif time - timing[0] < time_delay_out and time > timing[0]: #fade out
#        ax.scatter(xs,ys,zs, s=200, color=(0.5,0,1,1/len(xs)-(time-timing[0])/time_delay_out))
#    else:
#        continue

    plt.savefig('bloch.tiff')
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
