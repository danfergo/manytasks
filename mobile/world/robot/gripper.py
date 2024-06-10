from yarok import component
from yarok.platforms.mjc.interface import InterfaceMJC

from yarok.comm.utils.PID import PID


class GripperInterfaceMJC:

    def __init__(self, interface: InterfaceMJC):
        self.interface = interface
        P = 1
        I = 0.1
        D = 0.1
        self.gear = 100
        self.PIDs = [PID(P, I, D) for a in interface.actuators]

    def move_q(self, q):
        qq = min(1, max(0, q)) * 0.025
        [self.PIDs[a].setTarget(qq * self.gear) for a in range(len(self.interface.actuators))]

    def step(self):
        data = self.interface.sensordata()
        self.q = data
        [self.PIDs[a].update(data[a]) for a in range(len(data))]
        [self.interface.set_ctrl(a, self.PIDs[a].output) for a in range(len(self.interface.actuators))]


@component(
    tag='gripper',
    components=[

    ],
    interface_mjc=GripperInterfaceMJC,
    # language=xml
    template="""
        <mujoco>
            <worldbody>
                <body>
                    <geom type="box" size="0.05 0.025 0.025" pos='0 0 0.05'/>
                    
                    <body pos='0.075 0 0.025'>
                        <joint name="f1_joint" type="slide" axis="-1 0 0"
                               frictionloss="100" armature="100"
                               limited="true" range="-1.2 1.2"/>
                        <geom type="box" size="0.025 0.025 0.05" pos='0 0 0.101'/>
                    </body>
                    
                    <body pos='-0.075 0 0.025'>
                        <joint name="f2_joint" type="slide" axis="1 0 0"
                               frictionloss="100" armature="100"
                               limited="true" range="-1.2 1.2"/>
                        <geom type="box" size="0.025 0.025 0.05" pos='0 0 0.101'/>
                    </body>
                    
                </body>
            </worldbody>
            <actuator>
                <motor gear="50" name="f1a" joint="f1_joint" ctrllimited="true"
                       ctrlrange="-0.03 0.03" forcelimited="true" forcerange="-0.03 0.03"/>
                <motor gear="50" name="f2a" joint="f2_joint" ctrllimited="true"
                       ctrlrange="-0.03 0.03" forcelimited="true" forcerange="-0.03 0.03"/>
            </actuator>
            <sensor>
                <actuatorpos name="f1s" actuator="f1a"/>
                <actuatorpos name="f2s" actuator="f2a"/>
            </sensor>
        </mujoco>
    """
)
class Gripper:

    def move_q(self, q):
        pass
