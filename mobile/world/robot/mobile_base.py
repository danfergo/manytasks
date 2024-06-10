from yarok import component
from yarok.platforms.mjc.interface import InterfaceMJC

from .omniwheel import Omniwheel


class MobileBaseInterfaceMJC:

    def __init__(self, interface: InterfaceMJC):
        self.interface = interface

    def set_velocity(self, v):
        self.interface.set_ctrl('flw', -v)
        self.interface.set_ctrl('frw', v)
        self.interface.set_ctrl('blw', v)
        self.interface.set_ctrl('brw', -v)


@component(
    tag="mobile-base",
    components=[
        Omniwheel
    ],
    interface_mjc=MobileBaseInterfaceMJC,
    # language=xml
    template="""
    <mujoco>
        <worldbody>
            <body>
              <freejoint name="joint"/>
              <inertial pos="0 0 0" mass="0.03761" diaginertia="0.1 0.1 0.1"/>
              <body pos='0 0 0.5'>
                  <inertial pos="0 0 0" mass="0.03761" diaginertia="0.1 0.1 0.1"/>
                  <body name='mobile_base_center' pos='0 0 0.045'/>

                  <body pos="0 0 0.025">
                    <geom type="box" size="0.150 0.260 0.02" />
                  </body>

                  <!-- rfw -->
                  <body pos="0.16 0.2 0">
                    <body euler='0 0 0.7853981634'>
                        <joint type='hinge' name="flw_joint" axis='1 0 0'/>
                        <omniwheel name='w1'/>
                    </body>
                  </body>
                  <body pos="-0.16 0.2 0">
                    <body euler='0 0 -0.7853981634'>
                        <joint type='hinge' name="frw_joint" axis='1 0 0'/>
                        <omniwheel name='w2'/>
                    </body>
                  </body>

                  <!-- rbw -->
                  <body pos="0.16 -0.2 0">
                    <body euler='0 0 -0.7853981634'>
                        <joint type='hinge' name="blw_joint" axis='1 0 0'/>
                        <omniwheel name='w3'/>
                    </body>
                  </body>
                  <body pos="-0.16 -0.2 0">
                    <body euler='0 0 0.7853981634'>
                        <joint type='hinge' name="brw_joint" axis='1 0 0'/>
                        <omniwheel name='w4'/>
                    </body>
                  </body>
              </body>
              </body>
        </worldbody>
        <actuator>
                <velocity name="flw" joint="flw_joint"/>
                <velocity name="frw" joint="frw_joint"/>
                <velocity name="blw" joint="blw_joint"/>
                <velocity name="brw" joint="brw_joint"/>
                <!-- <position name="ax" gear="100" joint="xaxis" forcelimited="true" forcerange="-10000 10000"/>
                <position name="ay" gear="100" joint="yaxis" forcelimited="true" forcerange="-10000 10000"/>
                <position name="az" gear="100" joint="zaxis" forcelimited="true" forcerange="-10000 10000"/> -->
        </actuator>
        <sensor>
<!--                <actuatorpos name="x" actuator="ax"/>
                <actuatorpos name="y" actuator="ay"/>
                <actuatorpos name="z" actuator="az"/> -->
        </sensor>
        </mujoco>
    """
)
class MobileBase:

    def set_velocity(self, v):
        pass
