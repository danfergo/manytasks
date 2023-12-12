from math import pi

import yarok
from yarok import PlatformMJC
from yarok.components_manager import component

from src.world.robot.arm import Arm
from src.world.robot.crab_robot import CrabRobot
from src.world.robot.gripper import Gripper


@component(
    tag='arena-world',
    components=[
        CrabRobot,
        Gripper
    ],
    # language=xml
    template="""
        <mujoco>
         <option timestep="0.01" solver="Newton" iterations="30" tolerance="1e-10" jacobian="auto" cone="pyramidal"/>
            <compiler angle="radian"/>
            <visual>
                <!-- important for the Geltips, to ensure the its camera frustum captures the close-up elastomer -->
                <map znear="0.001" zfar="50"/>
                <quality shadowsize="2048"/>
            </visual>
            <asset>
                <!-- empty world -->
                <texture name="texplane" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 0.15 0.2"
                         width="512" height="512" mark="cross" markrgb=".8 .8 .8"/>    
                <material name="matplane" reflectance="0.3" texture="texplane" texrepeat="1 1" texuniform="true"/>
                <!-- object set -->
                <material name="black_plastic" rgba=".3 .3 .3 1"/>
                <!-- <mesh name="object" file="../object_set/${object}.stl" scale="0.001 0.001 0.001"/> -->
            </asset>
            <worldbody>
                <light directional="true" diffuse=".9 .9 .9" specular="0.1 0.1 0.1" pos="0 0 5.0" dir="0 0 -1"/>
                <camera name="viewer" pos="0 0 0.5" mode="fixed" zaxis="0 0 1"/>
                <body name="floor">
                    <geom name="ground" type="plane" size="0 0 1" pos="0 0 0" quat="1 0 0 0" material="matplane" condim="1"/>
                </body>

               <crab-robot name='crab'/>
                
                <!--
                  <mobile-base name="mb">
                        <body parent='mobile_base_center'>
                           <body pos="0 -0.25 0">
                                <arm name='left_arm'/>
                           </body>
                           <body pos="0 0.25 0">
                                <arm name='right_arm'/>
                           </body>
                        </body> 
                   </mobile-base> -->
              
            </worldbody>    

        </mujoco>
    """
)
class ArenaWorld:
    pass


class Behave:
    def __init__(self, crab: CrabRobot):
        self.crab = crab
        self.i = 0

    def on_start(self):
        self.crab.base.set_velocity(-0.2)

    def on_update(self):
        for i in range(3):
            self.crab.left_arm.move_q([i * pi/4, i * pi/4, i * pi/4])
            self.crab.right_gripper.move_q(i * 0.5/4)

            yarok.wait_seconds(5)

        # if self.i > 20000:
        #     return False
        return True


# for i in range(1000):
yarok.run({
    'world': ArenaWorld,
    'behaviour': Behave,
    'defaults': {
        'environment': 'sim'
    },
    'environments': {
        'sim': {
            'platform': {
                'class': PlatformMJC
            },
            'inspector': False,
            # 'behaviour': {
            # 'dataset_name': 'sim_depth'
            # }
        },
    }
})
