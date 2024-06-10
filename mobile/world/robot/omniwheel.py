from yarok import component

@component(
    tag='omniwheel',
    # language=xml
    template="""
    <mujoco>
            <worldbody>
                   <inertial pos="0 -0.02561 0.00193" mass="0.01" diaginertia="0.1 0.1 0.1"/>
                   <body pos='0 0 0' xyaxes='0 1 0 -1 0 0'>

                   <!-- pos -->
                   <body pos='0 0.005 0.0' euler='0 0.2617993878 0'>
                        <body euler='0 0 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 0.5235987756 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 1.047197551 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body> 
                         <body euler='0 1.570796327 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 2.094395102 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 2.617993878 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 3.141592654 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 3.665191429 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 4.188790205 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 4.71238898 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 5.235987756 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 5.759586532 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 6.283185307 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                   </body>

                   <body pos='0 -0.005 0.0'>
                        <body euler='0 0 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 0.5235987756 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 1.047197551 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body> 
                         <body euler='0 1.570796327 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 2.094395102 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 2.617993878 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 3.141592654 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 3.665191429 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 4.188790205 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 4.71238898 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 5.235987756 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 5.759586532 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                         <body euler='0 6.283185307 0'>
                            <geom type="capsule" size=".0045 .002" zaxis='-1 0 0' pos="0 0 0.025" rgba=".8 .2 .1 1"/>
                         </body>
                   </body>
              </body>
          </worldbody>
        </mujoco>

    """
)
class Omniwheel:
    pass