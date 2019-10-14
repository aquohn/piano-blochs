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
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from numpy import pi

TURN_FRAMES = 4
B_FIELD = 0.01
EASY = 10
BPM = 119
B_FIELD = 0.03
SCREEN_WIDTH=1000
SCREEN_HEIGHT=1000
AXIS_SCALE = 1.8
X_COLOR = "green"
Y_COLOR = "orange"
Z_COLOR = "blue"
measured = 0
TAPZONE = [[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]]
#x, y, z = 0, 0, 0
lock = False


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
myname = input("What is your name? ")
sv_arr = np.array([1,0])
z1 = [0,1]
circuit = QuantumCircuit(1,1) #1 qubit and 1 classical bit
simulator = Aer.get_backend('statevector_simulator')
screen = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_WIDTH))

running = True

clock = pygame.time.Clock()

time_delay = 3000 #milliseconds
time_delay_out = 1000

time0 = int(pygame.time.get_ticks())

#Song stuff:
note_time_arr = np.floor(((np.array(range(70)) + 1) * EASY/BPM * 60 + 2) * 1000)
note_cnt = 0

# Generate note distribution for each note
point_idxs = np.random.randint(0,6,len(note_time_arr))

combo=0
combotext=str()
score = 0

# Getting the wav
song = pygame.mixer.Sound("kalimba.wav") #use wav is best apparently

pygame.mixer.music.load('testes.wav')


MAXSCORE = 1000000
SCORE_PER_NOTE = MAXSCORE/len(note_time_arr)

# Rotation stuff
xcnt = 0
ycnt = 0
zcnt = 0
x_ax_x = y_ax_y = z_ax_z = AXIS_SCALE
x_ax_y = x_ax_z = y_ax_x = y_ax_z = z_ax_x = z_ax_y = 0
rot = 0.5
rotfactor = 1
theta = pi / (2 * TURN_FRAMES)

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

# Start screen
black=(0,0,0)
end_it=False

while (end_it==False):
    screen.fill(black)
    myfont=pygame.font.SysFont("Britannic Bold", 40)
    nlabel=myfont.render("Welcome "+myname+" Start Screen", 1, (255, 0, 0))
    for event in pygame.event.get():
        if event.type==MOUSEBUTTONDOWN:
            end_it=True
    screen.blit(nlabel,(150,200))
    pygame.display.flip()

# Start game itself
    
time0 = int(pygame.time.get_ticks())
pygame.mixer.music.play(0) #i think 0 = play 1 time, 1 is for 2 times, -1 is for infinite
persistence = 1
john=0  
#screen = pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_WIDTH))

while running:
    
    if persistence == 1:
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
                if not lock:
                    lock = True
                    if event.key == K_a:
                        xcnt += TURN_FRAMES
                    elif event.key == K_s:
                        ycnt += TURN_FRAMES
                    elif event.key == K_d:
                        zcnt += TURN_FRAMES
                    else:
                        lock = False
                
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_f:
                    persistence = 0
                elif event.key == K_RETURN:
                    circuit.measure([0],[0])
                    backend = Aer.get_backend('qasm_simulator')
                    result = execute(circuit,backend=backend,shots = 1).result()
                    counts = result.get_counts()
                    for key in counts:
                        if int(key) == 0:
                            sv_arr[0] = 1
                            sv_arr[1] = 0
                        else:
                            sv_arr[0] = 0
                            sv_arr[1] = 1
                    measured = 1
            elif event.type == QUIT:
                running = False
        
        #print("Note " + str(note_cnt) + ", z has value " + str(z))
        #valid_hit = (np.real(sv_arr[0]) == 0  and point_idxs[note_cnt] == -3) or (np.real(sv_arr[0]) == 1 and point_idxs[note_cnt] == 2)
        valid_hit = (np.real(sv_arr[0]) == 0 and john < -0.8) or (np.real(sv_arr[0]) == 1 and john > 0.8)

        if measured == 0 :
            if time >= note_time_arr[note_cnt] + 1000:
                combo = 0
                #print("miss!")
                combotext = "MISS!"
                note_cnt += 1
        if measured == 1:
            #measured = 0
            #print("measurement!")
            #print(note_time_arr[note_cnt])
            #print("sv_arr is " + str(sv_arr))
            #print("Target z is " + str(john))
            #print(time)
            
            #if valid_hit:
                #print("Valid hit!")
            if time < note_time_arr[note_cnt] - 1000:
                #print("Too early!")
                combotext = "TOO EARLY!"
            elif abs(time - note_time_arr[note_cnt]) < 500 and valid_hit:
                combo += 1
                combotext = "PERFECT!"
                #print("perfect!")
                score += 1/(1+abs(time-note_time_arr[note_cnt]))*SCORE_PER_NOTE
                note_cnt += 1
            elif abs(time - note_time_arr[note_cnt]) < 1000:
                if valid_hit:
                    combo += 1
                    combotext = "GREAT!"
                    #print("great!")
                    score += 1/(1+abs(time-note_time_arr[note_cnt]))*SCORE_PER_NOTE
                else:
                    #print("wrong side!")
                    combo = 0
                    combotext = "MISS!"
                note_cnt += 1
        
        if note_cnt == len(note_time_arr):
            persistence = 0
        #cheat code
        #print(note_time_arr)
        
        # Rotation
        if xcnt > 0:
            assert(lock == True)
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
            assert(lock == True)
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
            assert(lock == True)
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
        
        if (xcnt == ycnt == zcnt == 0):
            lock = False
        
        fig = plt.figure(figsize=(10,10))
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

        # draw sphere
        u, v = np.mgrid[0:2*pi:50j, 0:pi:25j]
        sphere_x = np.cos(u)*np.sin(v)
        sphere_y = np.sin(u)*np.sin(v)
        sphere_z = np.cos(v)
        ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color=(0,0,0,0.2))
        
        if not measured:
            result = execute(circuit, backend = simulator).result()
            sv_arr = result.get_statevector()
        else:
            measured = False
        z1 = [0,-np.real(1-2*np.conj(sv_arr[0])*sv_arr[0])]
        rotfactor = abs(z1[1]) + 0.05 # smooth precession
        x1 = [0,2*(np.real(sv_arr[0])*np.real(sv_arr[1])+np.imag(sv_arr[0])*np.imag(sv_arr[1]))]
        y1 = [0,2*(np.imag(sv_arr[0])*np.real(sv_arr[1])+np.real(sv_arr[0])*np.imag(sv_arr[1]))]
        n = (x1[1]**2+y1[1]**2+z1[1]**2)**0.5
        a = Arrow3D(x1/n, y1/n, z1/n, mutation_scale=20,
                lw=1, arrowstyle="-|>", color='r')
        ax.add_artist(a)
        
        #add points for the rhythm
        for i in range(len(note_time_arr)):
            xarr = [x_ax_x, y_ax_x, z_ax_x]
            yarr = [x_ax_y, y_ax_y, z_ax_y]
            zarr = [x_ax_z, y_ax_z, z_ax_z]
            
            idx = point_idxs[i] - 3
            if idx < 0:
                idx = (-1 * idx) - 1
                x = -xarr[idx] / AXIS_SCALE
                y = -yarr[idx] / AXIS_SCALE
                z = -zarr[idx] / AXIS_SCALE

            else:
                x = xarr[idx] / AXIS_SCALE
                y = yarr[idx] / AXIS_SCALE
                z = zarr[idx] / AXIS_SCALE
                         
            #TODO: fix the case where more than one note is present
            #TODO: fix the case where "too early" is reported on the wrong side, even though we missed the thing alrieady (because we hit the passed note while it's fading out)
            
            
            if note_time_arr[i] - time < time_delay and time < note_time_arr[i]: #fade in
#             plot point list[i] on bloch sphere with opacity = 1- (note_time_arr[i]-time)/time delay
                ax.scatter(x,y,z, s=200, color=(0.5,0,1,1-(note_time_arr[i]-time)/time_delay)) 
                john = z
            elif time - note_time_arr[i] < time_delay_out and time > note_time_arr[i]: #fade out
#             plot point list[i] on bloch sphere with opacity = 1- (time. - note_time_arr[i])/time delay out
                ax.scatter(x,y,z, s=200, color=(0.5,0,1,1- (time - note_time_arr[i])/time_delay_out)) 
#             print(str(time)+"No")
                john = z
            else:
                continue

        plt.savefig('bloch.tiff')
        surf = pygame.image.load("bloch.tiff")
        screen.blit(surf,(0,0))

        font = pygame.font.SysFont('comicsans', 30, True)
        timetext = font.render("Score: " + str(int(score)), 1, (0,0,0)) 
        combohaha = font.render("Combo: " + str(combo), 1, (0,0,0))
        combotext2 = font.render(str(combotext), 1, (0,0,0))
        screen.blit(timetext, (0, 0))
        screen.blit(combohaha, (200, 0))
        screen.blit(combotext2, (400, 0))

        pygame.display.flip()
        
        clock.tick(30)
        plt.close(fig)
    else:
        screen.fill(black)
        myfont=pygame.font.SysFont("Britannic Bold", 40)
        nlabel=myfont.render("Gameover", 1, (255, 0, 0))
        pygame.mixer.music.stop()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key==K_ESCAPE:
                    running = False
                if event.key==K_f:
                    persistence = 1
                    time0=int(pygame.time.get_ticks())
                    pygame.mixer.music.play(0)
            elif event.type == QUIT:
                running = False
        screen.blit(nlabel,(200,200))
        pygame.display.flip()

pygame.quit()
