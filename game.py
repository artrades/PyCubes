import sys,time
import sqlite3
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()

glass_texture = load_texture('assets/glass_block.png')
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1

soundtrack = Audio('Ambient.mp3',loop = True, autoplay = True)
count_blocks=0
sqlite_connection = sqlite3.connect('blocks.db')
cursor = sqlite_connection.cursor()

# Create an Entity for handling pausing an unpausing.
# Make sure to set ignore_paused to True so the pause handler itself can still receive input while the game is paused.
pause_handler = Entity(ignore_paused=True)
pause_text = Text('PAUSED', origin=(0,0), scale=2, enabled=False) # Make a Text saying "PAUSED" just to make it clear when it's paused.

def update():
    global block_pick
    if held_keys['-']: block_pick = -1 #блок не ставит
    if held_keys['0']: block_pick = 0
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5
    if held_keys['6']: block_pick = 6 #магнитный блок

    if held_keys['g']: player.gravity = 0
    if held_keys['h']: player.gravity = 1  


class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.yellow,)

def read_sqlite_table(records):
    try:  
        print("Подключен к SQLite")
        sqlite_select_query = """SELECT * from block"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Всего строк:  ", len(records))
        global count_blocks
        count_blocks=len(records)
        for row in records:
            voxel = Voxel(position=(row[3],row[4],row[5]))
            if row[6]==1:
                voxel.texture = grass_texture
            if row[6]==2:
                voxel.texture = stone_texture
            if row[6]==3:
                voxel.texture  = brick_texture
            if row[6]==4:
                voxel.texture = dirt_texture
            if row[6]==5:
                voxel.texture = glass_texture
            if row[6]==6:
                voxel.color = color.brown
                voxel.on_click = Func(player.animate_position, voxel.position, duration=.5, curve=curve.linear)      
        print('блоков: '+str(count_blocks)+' штук')
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite1", error)
    finally:
        if sqlite_connection:
            print("Ошибка при работе с SQLite2")

def input(key):
    if key == 'left mouse down':
        punch_sound.play()
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:  
            if block_pick == 0:
                voxel=Voxel(position=hit_info.entity.position + hit_info.normal)
            if block_pick == 1: 
                voxel = Voxel(position = hit_info.entity.position + hit_info.normal)
                voxel.texture = grass_texture
            if block_pick == 2:
                voxel = Voxel(position = hit_info.entity.position + hit_info.normal)
                voxel.texture = stone_texture
            if block_pick == 3: 
                voxel = Voxel(position = hit_info.entity.position + hit_info.normal)
                voxel.texture  = brick_texture
            if block_pick == 4:  
                voxel = Voxel(position = hit_info.entity.position + hit_info.normal)
                voxel.texture = dirt_texture
            if block_pick == 5: 
                voxel = Voxel(position = hit_info.entity.position + hit_info.normal)
                voxel.texture = glass_texture 
            if block_pick == 6:    #магнитный блок!!!
                voxel = Voxel(position = hit_info.entity.position + hit_info.normal)
                voxel.color = color.brown
                voxel.on_click = Func(player.animate_position, voxel.position, duration=.5, curve=curve.linear)      
            if block_pick == -1:   # блок не ставит
                return(None) 
                
             

            global count_blocks
            count_blocks=count_blocks+1 
            c_name = (str(voxel.position.x)+', '+str(voxel.position.y)+', '+str(voxel.position.z))
            db_block = (count_blocks,
                    voxel.model.name, 
                    c_name,
                    voxel.position.x, 
                    voxel.position.y, 
                    voxel.position.z,
                    block_pick)
            cursor.execute("INSERT INTO block VALUES(?, ?, ?, ?, ?, ?, ?);", db_block)        
            sqlite_connection.commit()
            print('блоков: '+str(count_blocks)+' штук')
            print(c_name)
    if key == 'right mouse down':
        punch_sound.play()
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            rc_name = str((hit_info.world_point - hit_info.point).x)+', '+str((hit_info.world_point - hit_info.point).y)+', '+str((hit_info.world_point - hit_info.point).z)
            destroy(hit_info.entity)
            count_blocks=count_blocks-1 
            sql_update_query ="""DELETE FROM block where c_name = ?"""  
            cursor.execute(sql_update_query, (rc_name, ))      
            sqlite_connection.commit()
            print('remove:')
            print(rc_name) 
    if key == 'o': # кнопка выхода из игры
        quit()     # не активна во время паузы
    if key == 'shift': # кнопка изменения скорости бега
        if player.speed == 5:
            player.speed = 10
        else:
            player.speed = 5
        print("скорость = " + str(player.speed))


def pause_handler_input(key):
    if key == 'escape':
        application.paused = not application.paused # Пауза/продолжение.
        pause_text.enabled = application.paused     # Надпись "PAUSED" .

pause_handler.input = pause_handler_input   # Assign the input function to the pause handler.

            
read_sqlite_table(None)
soundtrack.play

#МОДЕЛЬ ИГРОКА
#player = FirstPersonController(model='cube')
#ВИД ОТ ТРЕТЬЕГО ЛИЦА
#camera.z=-9

skybox_image = load_texture("skybox.png")
Sky(texture=skybox_image)

AmbientLight(color=(0.5, 0.5, 0.5, 1))
DirectionalLight(color=(0.5, 0.5, 0.5, 1), direction=(23, 45, 77),shadows = True)

app.run()
