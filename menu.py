# в отдельном файле menu.py

from ursina import *
import os

app = Ursina(title='Minecraft-Menu')

def main_start():
    print("Выбран пункт Start")
    os.system("start cmd /k python main.py")
    pass

# создаем объект на базе Entity, настраиваем камеру и бэкграунд
class MenuMenu(Entity):
   def __init__(self, **kwargs):
       super().__init__(parent=camera.ui, ignore_paused=True)

       self.main_menu = Entity(parent=self, enabled=True)
       self.background = Sky(model = "cube", double_sided = True, 
                             texture = Texture("textures/skybox.jpg"), 
                             rotation = (0, 90, 0))
       
# вписать lambda-функцию для запуска игры
       ButtonList(button_dict ={"Начать игру": Func(lambda: (main_start())),
                                "Выход":  Func(lambda: application.quit())},
                                y=0,
                                parent=self.main_menu)

main_menu = MenuMenu()

app.run()
