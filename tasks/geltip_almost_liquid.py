from yarok import Platform, PlatformMJC, component, Injector
from yarok.comm.plugins.cv2_inspector import Cv2Inspector
from yarok.comm.plugins.cv2_waitkey import Cv2WaitKey
from yarok.comm.toys.bucket_particles.bucket_particles import BucketParticles

from yarok.comm.worlds.empty_world import EmptyWorld
from yarok.comm.components.robotiq_2f85.robotiq_2f85 import Robotiq2f85
from yarok.comm.components.ur5e.ur5e import UR5e
from yarok.comm.components.digit.digit import Digit

from math import pi

from components.geltip.geltip import GelTip


@component(
    extends=EmptyWorld,
    components=[
        UR5e,
        Robotiq2f85,
        Digit,
        BucketParticles,
        GelTip
    ],
    # language=xml
    template="""
        <mujoco>
            <asset>
                <material name='glass' rgba='1 1 1 0.1'/>
                <material name='red' rgba='.8 .2 .1 1'/>
                <material name='green' rgba='.2 .8 .1 1'/>
            </asset>

            <worldbody>
                <bucket-particles name="bucket"/>

                 <body name="base-table" pos='-0.135 -0.48 0.018'>
                    <geom type='box' size='0.2 0.2 0.16'/>
                 </body>

                <ur5e name="arm"> 
                   <robotiq-2f85 name="gripper" parent="ee_link"> 
                        <body pos="0.02 -0.017 0.053" xyaxes="0 -1 0 1 0 0" parent='right_tip'>
                            <geltip name="geltip1" /> 
                        </body>
                        <body pos="-0.02 -0.017 0.053" xyaxes="0 1 0 -1 0 0" parent='left_tip'>
                            <geltip name="geltip2" /> 
                        </body>
                    </robotiq-2f85> 
                </ur5e>  
            </worldbody>        
        </mujoco>
    """
)
class AlmostLiquidWorld:
    pass


class AlmostLiquidPouringBehaviour:

    def __init__(self, pl: Platform, injector: Injector):
        self.arm: UR5e = injector.get('arm')
        self.gripper = injector.get('gripper')
        self.pl = pl

    def on_update(self):
        self.arm.set_speed(100 * pi)
        q = [0, -pi / 2, -pi / 2 + pi / 4, 0, pi / 2, pi / 2]
        self.arm.move_q(q)
        self.gripper.move(0)
        self.pl.wait(lambda: self.arm.is_at(q) and self.gripper.is_at(0))

        # self.arm.set_speed(pi/1000)
        q = [0, -pi / 2, -pi / 2, -pi / 2, pi / 2, pi / 2]
        self.arm.move_q(q)
        self.pl.wait(lambda: self.arm.is_at(q))

        # self.gripper.move(0.78)

        # self.pl.wait_seconds(10)

        self.arm.set_speed(pi/200)
        q = [0, -pi / 2, - pi / 2 - pi / 10, -pi / 2 + pi / 10, pi / 2, pi / 2]
        self.arm.move_q(q)

        self.pl.wait(lambda: self.arm.is_at(q))
        self.pl.wait_seconds(30)

def geltip_almost_liquid():
    conf = {
        'world': AlmostLiquidWorld,
        'behaviour': AlmostLiquidPouringBehaviour,
        'defaults': {
            'environment': 'sim',
            'components': {
                '/gripper': {
                    'left_tip': False,
                    'right_tip': False,
                }
            },
            'plugins': [
                (Cv2Inspector, {}),
                (Cv2WaitKey, {}),
            ]
        },
        'environments': {
            'sim': {
                'platform': {
                    'class': PlatformMJC,
                    'width': 1000,
                    'height': 800,
                }
            }
        },
    }
    Platform.create(conf).run()

if __name__ == '__main__':
    geltip_almost_liquid()