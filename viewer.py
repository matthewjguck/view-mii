
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import pi, sin, cos

from pyjoycon import JoyCon, get_R_id


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.model = self.loader.loadModel("models/panda-model")  # Replace with your model file
        self.model.reparentTo(self.render)
        self.model.setScale(.005, .005, .005)  # Adjust scale as needed
        self.model.setPos(-8, 42, 0)  # Adjust position as needed
        
        # Initial rotation angles
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0

        self.cam_x = 0
        self.cam_y = 0
        self.cam_z = 0

        self.camera.setPos(-20, -20, -20)  

        self.taskMgr.add(self.updateModelRotation, "UpdateModelRotationTask")
        self.taskMgr.add(self.walk, "walk")

    
    def updateModelRotation(self, task):
        # Get gyro data
        gyro_x, gyro_y, gyro_z = joycon.get_gyro_x(), joycon.get_gyro_y(), joycon.get_gyro_z()

        # Map gyro data to rotation - you may need to adjust scaling and offsets
        self.rotation_x += gyro_x * 0.001
        self.rotation_y += gyro_y * 0.001
        self.rotation_z += gyro_z * 0.001
        
        # Apply rotation to model
        self.model.setHpr(-self.rotation_z, self.rotation_y, self.rotation_x)
        
        return task.cont
    
    def walk(self, task):

        right = joycon.get_button_a()
        down = joycon.get_button_b()
        up = True # joycon.get_button_x()
        left = joycon.get_button_y()

        dt = self.clock.dt()

        if up:
            quaternion = self.camera.getQuat()
            fwd = quaternion.getForward()            
            self.camera.setPos(self.camera.getPos() + fwd*dt*5)

        return task.cont





if __name__ == "__main__":
    joycon_id = get_R_id()
    joycon = JoyCon(*joycon_id)
    joycon.get_status()

    app = MyApp()
    app.run()
    print(joycon.color_body)

