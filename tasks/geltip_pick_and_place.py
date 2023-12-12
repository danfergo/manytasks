import time

import numpy as np
from yarok.comm.components.cam.cam import Cam
from yarok.comm.plugins.cv2_waitkey import Cv2WaitKey

from components.geltip.geltip import GelTip
from components.tumble_tower.tumble_tower import TumbleTower

from yarok import Platform, Injector, component
from yarok.comm.worlds.empty_world import EmptyWorld
from yarok.comm.components.ur5e.ur5e import UR5e
from yarok.comm.components.robotiq_2f85.robotiq_2f85 import Robotiq2f85

from math import pi
import os

import cv2


@component(
    extends=EmptyWorld,
    components=[
        GelTip,
        TumbleTower,
        UR5e,
        Robotiq2f85,
        Cam
    ],
    template="""
        <mujoco>
            <option impratio="50" noslip_iterations="15"/>
            <asset>
                <texture type="skybox" 
                file="assets/robot_lab.png"
                rgb1="0.6 0.6 0.6" 
                rgb2="0 0 0"/>
                <texture 
                    name="white_wood_texture"
                    type="cube" 
                    file="assets/white_wood.png"
                    width="400" 
                    height="400"/>
                <material name="white_wood" texture="white_wood_texture" rgba="0.6 0.6 0.6 1" specular="0.1"/>
                <material name="gray_wood" texture="white_wood_texture" rgba="0.6 0.4 0.2 1" specular="0.1"/>
                <material name="red_wood" texture="white_wood_texture" rgba="0.8 0 0 1" specular="0.1"/>
                <material name="green_wood" texture="white_wood_texture" rgba="0 0.8 0 1" specular="0.1"/>
                <material name="yellow_wood" texture="white_wood_texture" rgba="0.8 0.8 0 1" specular="0.1"/>
            </asset>
            <worldbody>
                <body euler="1.57 -3.14 0" pos="0.25 -1.3 0.4">
                    <cam name="cam" />
                </body>
                
                <!-- blocks -->
                <body>
                    <freejoint/>
                    <geom 
                        type="box" 
                        size="0.03 0.03 0.03" 
                        pos="0.13 -0.135 0.131" 
                        mass="0.0001"
                        material="red_wood"
                        zaxis="0 1 0"/>
                </body>
                <body>
                    <freejoint/>
                    <geom 
                        type="box" 
                        size="0.03 0.03 0.03" 
                        pos="0.13 -0.135 0.191" 
                        mass="0.0001"
                        material="green_wood"
                        zaxis="0 1 0"/>
                </body>
                
                <body>
                    <freejoint/>
                    <geom 
                        type="box" 
                        size="0.03 0.03 0.03" 
                        pos="0.13 -0.135 0.221" 
                        mass="0.0001"
                        material="yellow_wood"
                        zaxis="0 1 0"/>
                </body>
                
               <body pos="0.3 0.11 0">
                    <geom type="box" pos="-0.45 0.29 0" size="0.1 0.1 0.3" material="gray_wood"/>
                    <geom type="box" pos="0 0 0" size="0.4 0.4 0.1" material="white_wood"/>
               </body>  
                
                <body euler="0 0 1.57" pos="-0.15 0.4 0.3">
                    <ur5e name='arm'>
                       <robotiq-2f85 name="gripper" parent="ee_link"> 
                          <body pos="0.02 -0.017 0.053" xyaxes="0 -1 0 1 0 0" parent="right_tip">
                                <geltip name="left_geltip" parent="left_tip"/>
                            </body>
                           <body pos="-0.02 -0.017 0.053" xyaxes="0 1 0 -1 0 0" parent="left_tip">
                                <geltip name="right_geltip" parent="right_tip"/>
                            </body>
                        </robotiq-2f85> 
                    </ur5e> 
                </body>
            </worldbody>
        </mujoco>
    """
)
class BlocksTowerTestWorld:
    pass


DOWN = [3.11, 1.6e-7, 3.11]

START_POS_UP = [0.3, -0.5, 0.21]
START_POS_DOWN = [0.3, -0.5, 0.11]
END_POS_UP = [0.6, -0.5, 0.21]
END_POS_DOWN = [0.6, -0.5, 0.115]

BLOCK_SIZE = 0.06


def z(pos, delta):
    new_pos = pos.copy()
    new_pos[2] += delta
    return new_pos


class GraspingCylinderBehaviour:

    def __init__(self, injector: Injector):
        self.cam: Cam = injector.get('cam')
        self.arm: UR5e = injector.get('arm')
        self.left_geltip: GelTip = injector.get('left_geltip')
        self.right_geltip: GelTip = injector.get('right_geltip')
        self.gripper: Robotiq2f85 = injector.get('gripper')

        self.arm.set_ws([
            [- pi, pi],  # shoulder pan
            [- pi, -pi / 2],  # shoulder lift,
            [- 2 * pi, 2 * pi],  # elbow
            [-2 * pi, 2 * pi],  # wrist 1
            [0, pi],  # wrist 2
            [- 2 * pi, 2 * pi]  # wrist 3
        ])
        self.arm.set_speed(pi / 3)

        self.pl: Platform = injector.get(Platform)
        self.t = time.time()
        self.i = 0
        self.save_dataset = True
        self.dataset_name = 'pick_and_place'

        self.left_geltip_bkg_depth = None
        self.right_geltip_bkg_depth = None

    def prepare_frame(self, frame):
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = frame[:, 80:80 + 480, :]
        frame = cv2.resize(frame, (448, 448))
        return frame

    def prepare_depth(self, frame, bkg_frame, rgb):
        frame = np.abs(frame - bkg_frame)

        frame = cv2.resize(frame, (640, 480))
        frame = frame[:, 80:80 + 480]
        frame = cv2.resize(frame, (448, 448))

        frame[frame > 1e-5] = 255
        frame[frame <= 1e-6] = 0
        contact_area = np.sum(frame) / 255

        frame = cv2.dilate(frame, np.ones((15, 15), np.uint8), iterations=1)

        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(frame, kernel, iterations=1)
        img_dilation = cv2.dilate(frame, kernel, iterations=1)
        frame = img_dilation - img_erosion

        frame = np.stack([
            frame * 0,
            frame * 0,
            frame
        ], axis=2)
        frame = frame + rgb
        frame[frame > 255] = 255
        frame = frame.astype(np.uint8)
        return frame, contact_area

    def save_frame(self):
        if self.save_dataset:
            cam_frame = self.prepare_frame(self.cam.read())
            left_touch_frame = self.prepare_frame(self.left_geltip.read())
            right_touch_frame = self.prepare_frame(self.right_geltip.read())

            left_touch_depth = self.left_geltip.read_depth()
            right_touch_depth = self.right_geltip.read_depth()
            left_diff, left_contact_area = self.prepare_depth(left_touch_depth, self.left_geltip_bkg_depth,
                                                              left_touch_frame)
            right_diff, right_contact_area = self.prepare_depth(right_touch_depth, self.right_geltip_bkg_depth,
                                                                right_touch_frame)

            v_bar = np.ones((448, 15, 3), np.uint8) * 200

            frame = np.concatenate([
                cam_frame, v_bar, right_diff, v_bar, left_diff
            ], axis=1)
            frame = cv2.putText(frame, 'Camera', (100, 430), cv2.FONT_HERSHEY_SIMPLEX,
                                1.4, (255, 255, 255), 2, cv2.LINE_AA)

            frame = cv2.putText(frame, 'Left GelTip', (600, 430), cv2.FONT_HERSHEY_SIMPLEX,
                                1.4, (255, 255, 255), 2, cv2.LINE_AA)

            if left_contact_area > 10:
                frame = cv2.putText(frame, 'Contact!', (600, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    1.4, (255, 255, 255), 2, cv2.LINE_AA)

            frame = cv2.putText(frame, 'Right GelTip', (1060, 430), cv2.FONT_HERSHEY_SIMPLEX,
                                1.4, (255, 255, 255), 2, cv2.LINE_AA)

            if right_contact_area > 10:
                frame = cv2.putText(frame, 'Contact!', (1060, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    1.4, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('data', frame)
            # cv2.waitKey(1)

            self.i += 1

    def wait(self, arm=None, gripper=None):
        def cb():
            self.save_frame()

            self.pl.wait_seconds(0.1)

            if arm is not None:
                return self.arm.is_at(arm)
            else:
                return self.gripper.is_at(gripper)

        self.pl.wait(cb)

    def on_start(self):
        self.pl.wait_seconds(1)
        self.left_geltip_bkg_depth = self.left_geltip.read_depth()
        self.right_geltip_bkg_depth = self.right_geltip.read_depth()
        self.save_frame()

        # self.pl.wait_seconds(20)

        def move_arm(p):
            q = self.arm.ik(xyz=p, xyz_angles=DOWN)
            self.arm.move_q(q)
            self.wait(arm=q)

        def move_gripper(q):
            self.gripper.close(q)
            self.wait(gripper=q)

        # set the arm in the initial position
        self.pl.wait(self.arm.move_xyz(xyz=START_POS_UP, xyz_angles=DOWN))

        self.save_frame()
        # cv2.waitKey(-1)
        self.arm.set_speed(pi / 24)

        # do the pick and place.
        for i in range(3):
            # before grasping.
            move_arm(START_POS_UP)

            # grasps block.
            move_arm(z(START_POS_DOWN, -i * BLOCK_SIZE))
            move_gripper(0.26)

            # moves.
            move_arm(START_POS_UP)
            move_arm(END_POS_UP)

            # places.
            move_arm(z(END_POS_DOWN, -(2 - i) * BLOCK_SIZE))
            move_gripper(0)

            # moves back
            move_arm(END_POS_UP)
            move_arm(START_POS_UP)


def geltip_pick_and_place():
    Platform.create({
        'world': BlocksTowerTestWorld,
        'behaviour': GraspingCylinderBehaviour,
        'defaults': {
            'plugins': [
                (Cv2WaitKey, {})
                # cv2WaitKey()
            ],
            'components': {
                '/gripper': {
                    'left_tip': False,
                    'right_tip': False
                },
                '/left_geltip': {
                    'cubic_core': True,
                    'label_color': '0 255 0'
                },
                '/right_geltip': {
                    'cubic_core': True,
                    'label_color': '255 0 0'
                }
            }
        },

    }).run()


if __name__ == '__main__':
    geltip_pick_and_place()
