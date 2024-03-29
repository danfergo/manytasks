from yarok import ConfigBlock, component, interface
from yarok.platforms.mjc import InterfaceMJC

import numpy as np
import cv2
import os

from time import time

from sim_model.model import SimulationModel
from sim_model.utils.camera import circle_mask

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@interface(
    defaults={
        'frame_size': (480, 640),
        'field_size': (120, 160),
        'field_name': 'geodesic',
        'elastic_deformation': True,
        'texture_sigma': 0.000005,
        'ia': 0.8,
        'fov': 90,
        'light_constants': [
            {'color': [196, 94, 255], 'id': 0.5, 'is': 0.1},  # red # [108, 82, 255]
            {'color': [154, 144, 255], 'id': 0.5, 'is': 0.1},  # green # [255, 130, 115]
            {'color': [104, 175, 255], 'id': 0.5, 'is': 0.1},  # blue  # [120, 255, 153]
        ],
    }
)
class GelTipInterfaceMJC:

    def __init__(self,
                 interface_mjc: InterfaceMJC,
                 config: ConfigBlock):
        self.interface = interface_mjc
        self.frame_size = config['frame_size']
        self.mask = circle_mask(self.frame_size)
        self.mask3 = np.stack([self.mask.T, self.mask.T, self.mask.T], axis=2)
        n_lights = len(config['light_constants'])

        bkg_zeros = np.zeros(self.frame_size + (3,), dtype=np.float32)


        print('-->shape', bkg_zeros.shape)

        try:
            assets_path = os.path.join(__location__, 'sim_assets/')
            real_bkg = cv2.imread(os.path.join(assets_path, 'bkg.png'))
            real_bkg = cv2.cvtColor(real_bkg, cv2.COLOR_BGR2RGB) / 255.0

            # bkg_bgr = cv2.imread(f'{dataset_path}/real_rgb_aligned/{obj}/bkg.png')
            print('-->', os.path.join(__location__, 'sim_assets/'))
            fields = SimulationModel.load_assets(
                assets_path,
                config['field_size'],
                self.frame_size[::-1],
                config['field_name'],
                n_lights
            )
            print('-xxx-', )

            self.model = SimulationModel(**{
                'ia': config['ia'],
                'fov': config['fov'],
                'light_sources': [{
                    'field': fields[l],
                    **config['light_constants'][l]}
                    for l in range(n_lights)
                ],
                'background_depth': np.load(assets_path + 'bkg.npy'),
                # 'cloud_map': cloud,
                'rectify_fields': True,
                'background_img': real_bkg,  # bkg_rgb if use_bkg_rgb else
                'texture_sigma': config['texture_sigma'],
                'elastic_deformation': config['elastic_deformation']
            })
            self.last_update = 0
        except Exception as e:
            # print(e)
            raise e
            print('[warning] failed to load simulation model')

    def read(self):
        t = time()
        if self.last_update > t - 1.0:
            return self.tactile
        self.last_update = t
        depth = self.read_depth()
        print('--> ', depth.shape)
        self.tactile = self.model.generate(depth) \
            .astype(np.uint8) * self.mask3
        return self.tactile

    def read_depth(self):
        return self.interface.read_camera('camera', self.frame_size, depth=True, rgb=False)


@interface()
class GelTipInterfaceHW:

    def __init__(self, config: ConfigBlock):
        self.cap = cv2.VideoCapture(config['cam_id'])
        if not self.cap.isOpened():
            raise Exception('GelTip cam ' + str(config['cam_id']) + ' not found')

        self.fake_depth = np.zeros((640, 480), np.float32)

    def read(self):
        [self.cap.read() for _ in range(10)]  # skip frames in the buffer.
        ret, frame = self.cap.read()
        return frame

    def read_depth(self):
        return self.fake_depth


@component(
    tag="geltip",
    defaults={
        'interface_mjc': GelTipInterfaceMJC,
        'interface_hw': GelTipInterfaceHW,
        'probe': lambda c: {'camera': c.read()},
        'label_color': '255 255 255',
        'cubic_core': False
    },
    # language=xml
    template="""
        <mujoco>
            <asset>
                <material name="glass_material" rgba="1 1 1 0.1"/>
                <material name="white_elastomer" rgba="1 1 1 1"/>
                <material name="black_plastic" rgba=".3 .3 .3 1"/>
                
                <material name="label_color" rgba="${label_color} 1.0"/>
        
                <mesh name="geltip_shell" file="meshes/shell_open.stl" scale="0.001 0.001 0.001"/>
                <mesh name="geltip_sleeve" file="meshes/sleeve_open.stl" scale="0.001 0.001 0.001"/>
                <mesh name="geltip_mount" file="meshes/mount.stl" scale="0.001 0.001 0.001"/>
                
                <!-- the glass -->
                <mesh name="geltip_glass" file="meshes/glass_long.stl" scale="0.00099 0.00099 0.00099"/>
                
                <!-- the outter elastomer, for visual purposes -->
                <mesh name="geltip_elastomer" file="meshes/elastomer_long.stl" scale="0.00099 0.00099 0.00099"/>  
                
                <!-- inverted mesh, for limiting the depth map-->
                <!-- changing this mesh changes the depth maps -->
                <mesh name="geltip_elastomer_inv" file="meshes/elastomer_very_long_voxel_e-6_inv.stl" scale="0.001 0.001 0.001"/>
        
            </asset>
            <worldbody>
                <body name="geltip">
                    <geom type="sphere" 
                        density="0.1"
                        material="label_color" 
                        size="0.005" 
                        pos="0.0 0.012 -0.025"/>
                    <geom density="0.1" type="mesh" mesh="geltip_shell" material="black_plastic"/>
                    <geom density="0.1" type="mesh" mesh="geltip_sleeve" material="black_plastic"/>
                    <geom density="0.1" type="mesh" mesh="geltip_mount" material="black_plastic"/>
                    <camera name="camera" pos="0 0 0.01" zaxis="0 0 -1" fovy="90"/>
                    <body>
                    
                       <!-- mesh, to serve as the glass and detect collisions -->
                       <geom  if='not cubic_core'
                              density="0.1" type="mesh" 
                              mesh="geltip_glass" 
                              pos="0.0 0.0 -0.003"
                              solimp="1.0 1.2 0.001 0.5 2" 
                              solref="0.02 1"
                              material="glass_material" />
                      <geom if="cubic_core" 
                            mass="0.1" 
                            type="box" 
                            pos="0 0 0.03" 
                            rgba="0 0 0 0" 
                            condim="6"
                            solimp="1.0 1.2 0.001 0.5 2" 
                            solref="0.02 1"
                            size="0.011 0.011 0.02"/> 
                            
                       <!-- inverted, mesh, for limiting the depth-map -->
                       <!-- changing this geom/mesh changes the depth maps -->
                       <!-- 32 for contype and conaffinity disables collisions -->     
                       <geom  type="mesh" 
                              mesh="geltip_elastomer_inv" 
                              contype="32"  
                              conaffinity="32" 
                              material="white_elastomer" /> 
                       
                       <!-- white elastomer, for visual purposes -->
                       <geom density="0.1" 
                              type="mesh" 
                              mesh="geltip_elastomer" 
                              friction="1 0.05 0.01" 
                              contype="32" 
                              conaffinity="32" 
                              material="white_elastomer"/> 
                    </body>
        
                </body>
            </worldbody>
        </mujoco>
    """
)
class GelTip:

    def __init__(self):
        """
            Geltip driver as proposed in
            https://danfergo.github.io/geltip-simulation/

        """
        pass

    def read(self):
        pass

    def read_depth(self):
        pass
