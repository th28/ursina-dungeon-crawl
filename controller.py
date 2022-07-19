from ursina import *

class FirstPersonController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)
        self.go_bwd = False
        self.go_fwd = False
        self.turn_l = False
        self.turn_r = False
        self.strf_r = False
        self.strf_l = False
        self.anim_dur = .2
        self.step_scale = 2.0
        self.animator = None
        self.target = None
        self.dir = None
        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 75
        self.mouse_sensitivity = Vec2(40, 40)

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def animate_move(self, target, duration, rotate=False):
        progress = 0
        if not rotate:
            hit_info = raycast(self.world_position + self.up*.5, self.dir, distance=1, debug=True)
            print(hit_info.hit)
            if hit_info.hit:
                pass
            else:
                while (progress <= duration):
                    progress = progress + time.dt
                    pct = clamp(progress / duration, 0, 1)
                    if rotate:
                        self.rotation = lerp(self.rotation, target, pct)
                    else:
                        self.position = lerp(self.position, target, pct)
                    yield 
        else:
            while (progress <= duration):
                    progress = progress + time.dt
                    pct = clamp(progress / duration, 0, 1)
                    if rotate:
                        self.rotation = lerp(self.rotation, target, pct)
                    else:
                        self.position = lerp(self.position, target, pct)
                    yield 

        
    def update(self):
            #print(self.position)
            if self.animator:
                try:
                    next(self.animator)
                except StopIteration:
                    self.animator = None

            if self.animator is None:
                if self.go_fwd:
                        self.target = round(self.position + self.dir.__mul__(self.step_scale), 0)
                        self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=False)
                        self.go_fwd = False
                elif self.go_bwd:
                        self.target = round(self.position + self.dir.__mul__(self.step_scale), 0)  
                        self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=False)                    
                        self.go_bwd = False
                elif self.turn_r:  
                        self.target = self.rotation + self.dir
                        self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=True)                    
                        self.turn_r = False
                elif self.turn_l: 
                        self.target = self.rotation + self.dir
                        self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=True)                  
                        self.turn_l = False
                elif self.strf_l:
                        self.target = round(self.position + self.dir.__mul__(self.step_scale), 0)      
                        self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=False)                
                        self.strf_l = False
                elif self.strf_r:
                        self.target = round(self.position + self.dir.__mul__(self.step_scale), 0)
                        self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=False)
                        self.strf_r = False
                
    def input(self, key):
        if key == 'w':
            self.go_fwd = True
            self.dir = self.forward
        elif key == 's':
            self.go_bwd = True
            self.dir = self.back
        elif key == 'd':
            self.turn_r = True
            self.dir = Vec3(0,90,0)
        elif key == 'a':
            self.turn_l = True
            self.dir = Vec3(0,-90,0)
        elif key == 'e':
            self.strf_r = True
            self.dir = self.right
        elif key == 'q':
            self.strf_l = True
            self.dir = self.left