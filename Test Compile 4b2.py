# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 10:28:34 2019

@author: Kong
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

class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

SCREEN_WIDTH=640
SCREEN_HEIGHT=640
sv_arr = np.array([1,0])
z1 = [0,1]

pygame.init()

simulator = Aer.get_backend('statevector_simulator')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

running = True

clock = pygame.time.Clock()

time_delay = 3000 #milliseconds
time_delay_out = 1000

#Song stuff:
timing = [5000, 7000]
list = np.array([[0.6,0.8], [-0.8, 0.6]])

# Getting the wav
song = pygame.mixer.Sound("testes.wav") #use wav is best apparently

pygame.mixer.music.load('testes.wav')
pygame.mixer.music.play(0) #i think 0 = play 1 time, 1 is for 2 times, -1 is for infinite

time0 = int(pygame.time.get_ticks())

while running:
    screen.fill((0, 0, 0))

    time = int(pygame.time.get_ticks())-time0

    # Initialization
    circuit = QuantumCircuit(1,1) #1 qubit and 1 classical bit
    sv_arr = np.array([sv_arr[0]+0.03, sv_arr[1]])
    sv_arr = sv_arr/((abs(sv_arr[0]))**2+(abs(sv_arr[1]))**2)**0.5
    circuit.initialize(sv_arr, 0)
    
    # Precession effect
    circuit.u3(0,0,0.3,0)
        
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                print(time)
            elif event.key == K_a:
                circuit.x(0)
            elif event.key == K_s:
                circuit.y(0)
            elif event.key == K_d:
                circuit.z(0)
            elif event.key == K_RETURN:
                circuit.measure([0],[0])
                backend = Aer.get_backend('qasm_simulator')
                result = execute(circuit,backend=backend,shots = 1).result()
                counts = result.get_counts()
                for key in counts:
                    sv_arr[int(key)] = 1
                    sv_arr[1-int(key)] = 0
                # Check if statevector coincides with point here
        elif event.type == QUIT:
            running = False
    
    fig = plt.figure(figsize=(9,9))
    ax = plt.gca(projection='3d')
    ax._axis3don = False

    # draw sphere
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
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
            lw=1, arrowstyle="-|>", color="r")
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
    plt.close(fig)
    
    font = pygame.font.SysFont('comicsans', 30, True)
    timetext = font.render("Time: " + str(time), 1, (0,0,0)) 
    screen.blit(timetext, (200, 0))
    
    pygame.display.flip()
    
    #FPS:
    clock.tick(30)

# print("quitting")
pygame.quit()
