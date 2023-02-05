import sqlite3
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()
count_blocks=0
# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.

conn = sqlite3.connect('blocks.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS block(
   blockid INT ,
   model NONE,
   c_name NONE,
   x NONE,
   y NONE,
   z NONE);
""")
conn.commit()

class Voxel(Button):
    def __init__(self, position=(0,0,0),id = 0):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )

      


    def input(self, key):
         if self.hovered:
             if key == 'left mouse down':
                global count_blocks
                count_blocks=count_blocks+1
                voxel = Voxel( position=self.position + mouse.normal)
                #имя из координат создаваемого блока
                c_name = (str(voxel.position.x)+', '+str(voxel.position.y)+', '+str(voxel.position.z))
                db_block = (count_blocks,
                    voxel.model.name, 
                    c_name,
                    voxel.position.x, 
                    voxel.position.y, 
                    voxel.position.z)
                cur.execute("INSERT INTO block VALUES(?, ?, ?, ?, ?, ?);", db_block)
                conn.commit()
                print('set:')
                print(c_name)
             if key == 'right mouse down': 
                #имя из координат удвляемого блока
                rc_name = str(self.position.x)+', '+str(self.position.y)+', '+str(self.position.z)
                sql_update_query ="""DELETE FROM block where c_name = ?"""  
                cur.execute(sql_update_query, (rc_name, ))      
                conn.commit()
                print('remove:')
                print(rc_name)#теперь сделать удаление из базы
                destroy(self)


for z in range(32):
    for x in range(32):
        count_blocks=count_blocks+1
        voxel = Voxel( position=(x-16,0,z-16))
        c_name = (str(voxel.position.x)+', '+str(voxel.position.y)+', '+str(voxel.position.z))
        db_block = (count_blocks,
                    voxel.model.name,
                    c_name, 
                    voxel.position.x, 
                    voxel.position.y, 
                    voxel.position.z)
        print(voxel.position)            
        cur.execute("INSERT INTO block VALUES(?, ?, ?, ?, ?, ?);", db_block)
        conn.commit() 
        

player = FirstPersonController()
#player.gravity = 0
print('блоков: '+str(count_blocks)+' штук')
app.run()
