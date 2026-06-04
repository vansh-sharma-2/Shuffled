import pygame,random

pygame.init()

screen_size=700
screen=pygame.display.set_mode((screen_size,screen_size))
pygame.display.set_caption("Slide Puzzle")
fps=60
fpsClock=pygame.time.Clock()
tile_size=(screen_size-200)/5

BOARD_X=110
BOARD_Y=110
GAP=3

move_count=0
selected_i=None
adj_i=[]
won=False

anim_active=False
anim_from=None
anim_to=None
anim_tile_id=None
anim_t=0.0
ANIM_SPEED=10.0

font_ui=pygame.font.SysFont("consolas",24,bold=True)
font_win=pygame.font.SysFont("consolas",48,bold=True)
font_sub=pygame.font.SysFont("consolas",22)

class tile:
    def __init__(self,id):
        self.id=id

    def load(self):
        return pygame.transform.scale(pygame.image.load("assets\\"+str(self.id)+".png"),(int(tile_size-GAP*2),int(tile_size-GAP*2)))

T=[]
for i in range(25):
    T.append(tile(i))

temp=[]
Data=[]
for i in range(25):
    temp.append(i)
for i in range(25):
    Data.append(temp.pop(random.randint(0,(len(temp)-1))))

def idx_to_px(i):
    col=i%5
    row=i//5
    return (BOARD_X+col*tile_size,BOARD_Y+row*tile_size)

def get_idx(x,y):
    if x<BOARD_X or x>(BOARD_X+5*tile_size) or y>(BOARD_Y+5*tile_size) or y<BOARD_Y:
        return None
    nx=int((x-BOARD_X)//tile_size)
    ny=int((y-BOARD_Y)//tile_size)
    return ny*5+nx

def update_adj_i(i):
    global adj_i
    adj_i=[]
    col=i%5
    row=i//5
    if col>0: adj_i.append(i-1)
    if col<4: adj_i.append(i+1)
    if row>0: adj_i.append(i-5)
    if row<4: adj_i.append(i+5)

def check_win():
    return Data==list(range(25))

def update_tiles():
    for i in range(25):
        if anim_active and i==anim_dst_i:
            continue
        px,py=idx_to_px(i)
        rx,ry=int(px)+GAP,int(py)+GAP
        rw,rh=int(tile_size)-GAP*2,int(tile_size)-GAP*2
        if Data[i]==0:
            pygame.draw.rect(screen,(0,80,160),(rx,ry,rw,rh),border_radius=6)
            continue
        color=(80,160,255) if i==selected_i else (0,100,200)
        if i in adj_i and selected_i is not None and Data[i]==0:
            color=(0,180,120)
        pygame.draw.rect(screen,color,(rx,ry,rw,rh),border_radius=6)
        try:
            img=T[Data[i]].load()
            screen.blit(img,(rx,ry))
        except Exception:
            pass

def draw_anim_tile():
    ease=anim_t*anim_t*(3-2*anim_t)
    cx=anim_from[0]+(anim_to[0]-anim_from[0])*ease
    cy=anim_from[1]+(anim_to[1]-anim_from[1])*ease
    rx,ry=int(cx)+GAP,int(cy)+GAP
    rw,rh=int(tile_size)-GAP*2,int(tile_size)-GAP*2
    pygame.draw.rect(screen,(80,160,255),(rx,ry,rw,rh),border_radius=6)
    try:
        img=T[anim_tile_id].load()
        screen.blit(img,(rx,ry))
    except Exception:
        pass

def draw_ui():
    label=font_ui.render("Moves: "+str(move_count),True,(255,255,255))
    screen.blit(label,(BOARD_X,BOARD_Y+int(tile_size*5)+14))
    hint=font_sub.render("Select tile, then click blank neighbour  |  R = restart",True,(180,220,255))
    screen.blit(hint,hint.get_rect(centerx=screen_size//2,y=BOARD_Y-38))

def draw_win():
    overlay=pygame.Surface((screen_size,screen_size),pygame.SRCALPHA)
    overlay.fill((0,30,80,210))
    screen.blit(overlay,(0,0))
    w=font_win.render("PUZZLE SOLVED!",True,(80,255,180))
    s=font_sub.render("Completed in "+str(move_count)+" moves   |   R to restart",True,(200,230,255))
    screen.blit(w,w.get_rect(center=(screen_size//2,screen_size//2-28)))
    screen.blit(s,s.get_rect(center=(screen_size//2,screen_size//2+34)))

def restart():
    global Data,move_count,selected_i,adj_i,won,anim_active
    t2=list(range(25))
    Data=[]
    for _ in range(25):
        Data.append(t2.pop(random.randint(0,len(t2)-1)))
    move_count=0
    selected_i=None
    adj_i=[]
    won=False
    anim_active=False

anim_dst_i=None

run=True
while run:
    dt=fpsClock.tick(fps)/1000.0

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                restart()
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and not anim_active and not won:
            i=get_idx(*pygame.mouse.get_pos())
            if i is not None:
                if Data[i]!=0:
                    selected_i=i
                    update_adj_i(i)
                elif selected_i is not None and i in adj_i and Data[i]==0:
                    anim_active=True
                    anim_from=idx_to_px(selected_i)
                    anim_to=idx_to_px(i)
                    anim_tile_id=Data[selected_i]
                    anim_t=0.0
                    anim_src_i=selected_i
                    anim_dst_i=i
                    Data[i]=Data[selected_i]
                    Data[selected_i]=0
                    selected_i=None
                    adj_i=[]
                    move_count+=1

    if anim_active:
        anim_t+=dt*ANIM_SPEED
        if anim_t>=1.0:
            anim_t=1.0
            anim_active=False
            anim_dst_i=None
            if check_win():
                won=True

    screen.fill((0,145,255))
    border=pygame.transform.scale(pygame.image.load("assets\\border1.png"),(screen_size-172,screen_size-172))
    screen.blit(border,(96,96))

    update_tiles()
    if anim_active:
        draw_anim_tile()

    draw_ui()
    if won:
        draw_win()

    pygame.display.update()

pygame.quit()