#-----------Minecraft3D-----------
#-------Minecraft in Python-------
#------Made by Dimitrigamer1------

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import *
from perlin_noise import *
import random
import time

app = Ursina(title="Minecraft3D")
application.development_mode = False
window.cog_button.enabled = False
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.show_fps = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.color = color.rgb(0, 200,211)
window.fps_limit = False

grass_block = load_texture('assets/blocks/grass_block.png')
stone_block = load_texture('assets/blocks/stone_block.png')
crosshair = load_texture('assets/crosshair.png')
WireFrame = load_texture('assets/wireframe.png')

random_seed = random.randint(0,18446744073709551616)

noise = PerlinNoise(octaves=2,seed=random_seed)
amp = 12
freq = 32
terrainWidth = 100
subsets = []
subCubes = []
subWidth = int(terrainWidth/1)
sci = 0
currentSubset = 0
terrain = Entity(model=None, collider=None)

player = FirstPersonController()
player.y = 12
player.gravity = 0.9
player.jump_height = 1.2
player.jump_duration = 0.45
player.speed = 4.317

player.mouse_sensitivity = Vec2(50, 50)
player.cursor.texture = crosshair
player.cursor.color = color.white
player.cursor.scale = 0.03
player.cursor.rotation_z = 90

prevTime = time.time()
prevZ = player.z
prevX = player.x

bte = Entity(model='cube', texture=WireFrame)

def BuildTool():
    bte.position = round(player.position + camera.forward * 3.5)
    bte.y += 2
    bte.y = round(bte.y)
    bte.x = round(bte.x)
    bte.z = round(bte.z)

def build():
    e = duplicate(bte)
    e.collider = 'mesh'
    e.texture = stone_block

def update():
    global prevZ, prevX, prevTime, amp
    if abs(player.z - prevZ) > 1 or abs(player.x - prevX) > 1:
        generateShell()
        prevZ = player.z
        prevX = player.x

    if time.time() - prevTime > 0.001:
        generateSubset()
        prevTime = time.time()

    if player.y < -amp-1:
        player.y = 2 + floor((noise([player.x / freq, player.z / freq])) * amp)
        player.land()

    if held_keys['control']:
        player.speed = 5.621
    elif held_keys['shift']:
        player.speed = 1.31
    else:
        player.speed = 4.317

    BuildTool()

for i in range(subWidth):
    terrain_blocks = Entity(model='cube')
    subCubes.append(terrain_blocks)

for i in range(int((terrainWidth * terrainWidth) / subWidth)):
    terrain_blocks = Entity(model=None)
    terrain_blocks.parent = terrain
    subsets.append(terrain_blocks)

def generateSubset():
    global sci, currentSubset, freq, amp
    if currentSubset >= len(subsets):
        finishTerrain()
        return

    for i in range(subWidth):
        x = subCubes[i].x = floor((i+sci) / terrainWidth)
        z = subCubes[i].z = floor((i+sci) % terrainWidth)
        y = subCubes[i].y = floor(((noise([x / freq, z / freq])) * amp))
        subCubes[i].parent = subsets[currentSubset]
        subCubes[i].color = color.green
        subCubes[i].visible = False

    subsets[currentSubset].combine(auto_destroy = False)
    subsets[currentSubset].texture = grass_block
    sci += subWidth
    currentSubset += 1

terrainFinished = False

def finishTerrain():
    global terrainFinished
    if terrainFinished == True:
        return

    terrain.combine()
    terrainFinished = True
    terrain.texture = grass_block

#for i in range(terrainWidth * terrainWidth):
    #terrain_blocks = Entity(model='cube', color=color.green, parent=terrain)
    #terrain_blocks.x = floor(i/terrainWidth)
    #terrain_blocks.z = floor(i%terrainWidth)
    #terrain_blocks.y = floor(((noise([terrain_blocks.x/freq, terrain_blocks.z/freq])) * amp))

#terrain.combine()
#terrain.texture = grass_block
#terrain.collider = 'mesh'

shellies = []
shellWidht = 18
for i in range(shellWidht * shellWidht):
    terrain_blocks = Entity(model='cube',color=color.green, collider='box')
    terrain_blocks.visible = False
    shellies.append(terrain_blocks)

def generateShell():
    global shellWidht, amp, freq
    for i in range(len(shellies)):
        x = shellies[i].x = floor((i/shellWidht) + player.x - 0.5 * shellWidht)
        z = shellies[i].z = floor((i%shellWidht) + player.z - 0.5 * shellWidht)
        shellies[i].y = floor(((noise([x/freq, z/freq])) * amp))

def input(key):
    if key == 'escape':
        quit()
    if key == 'g':
        generateSubset()
    if key == 'right mouse down':
        build()
    if key == "left mouse down":
        if mouse.hovered_entity:
            if mouse.hovered_entity != terrain:
                destroy(mouse.hovered_entity)

generateShell()

app.run()