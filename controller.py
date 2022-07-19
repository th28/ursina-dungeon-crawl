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
        self.animator = None
        self.target = None
        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 75
        self.mouse_sensitivity = Vec2(40, 40)

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def animate_move(self, target, duration, rotate=False):
        progress = 0
        while (progress <= duration):
            progress = progress + time.dt
            pct = clamp(progress / duration, 0, 1)
            if rotate:
                self.rotation = lerp(self.rotation, target, pct)
            else:
                self.position = lerp(self.position, target, pct)
            yield 
        
    def update(self):
            #print(self.target)
            print(self.position)
            if self.animator:
                try:
                    next(self.animator)
                except StopIteration:
                    self.animator = None
                    #self.position = round(self.position,0)

            if self.animator == None:
                if self.go_fwd:
                        self.target = round(self.position + self.forward.__mul__(2.0), 0)
                        self.go_fwd = False
                elif self.go_bwd:
                        self.target = round(self.position + self.back.__mul__(2.0), 0)                      
                        self.go_bwd = False
                elif self.turn_r:  
                        self.target = self.rotation + Vec3(0,90,0)
                        #self.animator = self.animate_move(self.rotation + Vec3(0,90,0), duration=self.anim_dur, rotate=True)                    
                        #self.turn_r = False
                elif self.turn_l: 
                        self.animator = self.animate_move(self.rotation + Vec3(0,90,0), duration=self.anim_dur, rotate=True)                  
                        #self.turn_l = False
                elif self.strf_l:
                        self.target = round(self.position + self.left.__mul__(2.0), 0)                      
                        self.strf_l = False
                elif self.strf_r:
                        self.target = round(self.position + self.right.__mul__(2.0), 0)
                        self.strf_r = False
                
                if self.target != None:
                        
                    #hit_info = raycast(self.world_position + Vec3(0,0.5,0), direction=self.target, distance=0.5)
                    #if not hit_info.hit:
                        if self.turn_r or self.turn_l:
                            self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=True)
                        else:
                            self.animator = self.animate_move(self.target, duration=self.anim_dur, rotate=False)


    def input(self, key):
        if key == 'w up':
            self.go_fwd = True
        elif key == 's up':
            self.go_bwd = True
        elif key == 'd up':
            self.turn_r = True
        elif key == 'a up':
            self.turn_l = True
        elif key == 'e up':
            self.strf_r = True
        elif key == 'q up':
            self.strf_l = True