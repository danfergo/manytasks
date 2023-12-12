from yarok.components_manager import component

from src.world.robot.arm import Arm
from src.world.robot.gripper import Gripper
from src.world.robot.mobile_base import MobileBase


@component(
    tag='crab-robot',
    components=[
        MobileBase,
        Arm,
        Gripper
    ],
    # language=xml
    template="""
        <mujoco>
            <visual>

            </visual>
            <asset>

            </asset>
            <worldbody>
                  <mobile-base name="base">
                        <body parent='mobile_base_center'>
                           <body pos="0 -0.25 0">
                                <arm name='left_arm'>
                                    <gripper parent='tcp' name='left_gripper'/>
                                </arm>
                           </body>
                           <body pos="0 0.25 0">
                                <arm name='right_arm'>
                                    <gripper parent='tcp' name='right_gripper'/>
                                </arm>
                           </body>
                        </body> 
                   </mobile-base>
            </worldbody>    
        </mujoco>
    """
)
class CrabRobot:

    def __init__(self, base: MobileBase,
                 left_arm: Arm,
                 right_arm: Arm,
                 right_gripper: Gripper,
                 left_gripper: Gripper):
        self.base = base
        self.arms = [left_arm, right_arm]
        self.left_arm = left_arm
        self.right_arm = right_arm
        self.left_gripper = left_gripper
        self.right_gripper = right_gripper
