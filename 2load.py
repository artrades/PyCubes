import sys,time
import sqlite3
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()


count_blocks=0

sqlite_connection = sqlite3.connect('blocks.db')
cursor = sqlite_connection.cursor()

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
            )

      

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
        print('блоков: '+str(count_blocks)+' штук')

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite1", error)
    finally:
        if sqlite_connection:
            print("Ошибка при работе с SQLite2")

read_sqlite_table(None)

def input(key):
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)#Добавить в блок настроек
        if hit_info.hit:
            voxel=Voxel(position=hit_info.entity.position + hit_info.normal)
            global count_blocks
            count_blocks=count_blocks+1 
            c_name = (str(voxel.position.x)+', '+str(voxel.position.y)+', '+str(voxel.position.z))
            db_block = (count_blocks,  #ОПТИМИЗИРОВАТЬ
                    voxel.model.name, 
                    c_name,
                    voxel.position.x, 
                    voxel.position.y, 
                    voxel.position.z)
            cursor.execute("INSERT INTO block VALUES(?, ?, ?, ?, ?, ?);", db_block)        
            sqlite_connection.commit()
            print('блоков: '+str(count_blocks)+' штук')
            print(str(voxel.position.x), 
                  str(voxel.position.y), 
                  str(voxel.position.z))
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5) #Добавить в блок настроек
        if hit_info.hit:
            rc_name = str((hit_info.world_point - hit_info.point).x)+', '+str((hit_info.world_point - hit_info.point).y)+', '+str((hit_info.world_point - hit_info.point).z)
            destroy(hit_info.entity)
            count_blocks=count_blocks-1 
            sql_update_query ="""DELETE FROM block where c_name = ?"""  
            cursor.execute(sql_update_query, (rc_name, ))      
            sqlite_connection.commit()
            print('remove:')
            print(rc_name) 
            
player = FirstPersonController()


def update():
    pass

player.gravity = 0
skybox_image = load_texture("skybox.png")
Sky(texture=skybox_image)

AmbientLight(color=(0.5, 0.5, 0.5, 1))
DirectionalLight(color=(0.5, 0.5, 0.5, 1), direction=(23, 45, 77),shadows = True)

app.run()
