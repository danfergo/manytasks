from yarok.components_manager import component
from yarok.mjc.interface import InterfaceMJC

from yarok.utils.PID import PID

class ArmInterfaceMJC:

    def __init__(self, interface: InterfaceMJC):
        self.interface = interface
        P = 1
        I = 0.1
        D = 0.1
        self.gear = 50
        self.PIDs = [PID(P, I, D) for a in interface.actuators]

    def move_q(self, q):
        [self.PIDs[qa].setTarget(q[qa] * self.gear) for qa in range(len(q))]

        # print(q)
        # v = 0.1
        # self.interface.set_ctrl('j0', v)
        # self.interface.set_ctrl('j1v', v)
        # self.interface.set_ctrl('j2v', v)
        # self.interface.set_ctrl('j0p', q[0])
        # self.interface.set_ctrl('j1p', q[1])
        # self.interface.set_ctrl('j2p', q[2])

    def step(self):
        data = self.interface.sensordata()
        self.q = data
        # print(self.q[1], self.PIDs[1].SetPoint, self.PIDs[1].output)
        [self.PIDs[a].update(data[a]) for a in range(len(data))]
        # print(self.PIDs[0].output, self.PIDs[0].output)
        [self.interface.set_ctrl(a, self.PIDs[a].output) for a in range(len(self.interface.actuators))]

@component(
    tag='arm',
    components=[

    ],
    interface_mjc=ArmInterfaceMJC,
    # language=xml
    template="""
        <mujoco>
            <worldbody>
                <body>

                   <joint type="hinge" name="joint0" axis="0 0 1" armature="100" frictionloss="100"/>
                   <geom type="cylinder" size="0.05 0.025" pos='0 0 0.025'/>
                   <geom type="box" size="0.025 0.025 0.025" pos='0 0 0.05'/>

                    <body pos="0 0 0.1">
                        <joint type='hinge' name="joint1"  axis="0 1 0" armature="100" frictionloss="100"/>
                        <!--<inertial pos="0.1 0 0" mass="0.03761" diaginertia="0.1 0.1 0.1"/>-->
                        <geom type="capsule" size=".04 .05"  pos="0 0 0.05" rgba=".8 .2 .1 1"/>

                         <body pos="0 0 0.2">
                            <joint type='hinge' name="joint2" axis="0 1 0"  armature="100" frictionloss="100"/>
                            <!--<inertial pos="0.1 0 0" mass="0.03761" diaginertia="0.1 0.1 0.1"/>-->
                            <geom type="capsule" size=".04 .05"  pos="0 0 0.05" rgba=".8 .2 .1 1"/>
                        
                        
                            <body pos='0 0 0.2' name='tcp'>
                                    
                            </body>
                        
                        </body>
                        
                    </body>
                </body>
            </worldbody>
            <actuator>
                <motor name="j0" 
                    joint="joint0" 
                    gear="50" 
                    ctrllimited="true"
                    ctrlrange="-1 1"/>
                <motor name="j1" 
                    joint="joint1" 
                    gear="100" 
                    ctrllimited="true"
                    ctrlrange="-2 2"/>
                <motor name="j2" 
                    joint="joint2" 
                    gear="100" 
                    ctrllimited="true"
                    ctrlrange="-1 1"/>
            </actuator>
            <sensor>
                <actuatorpos name="s0p" actuator="j0"/>
                <actuatorpos name="s1p" actuator="j1"/>
                <actuatorpos name="s2p" actuator="j2"/>
            </sensor>
        </mujoco>
    """
)
class Arm:

    def move_q(self, q):
        pass
