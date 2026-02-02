import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ================== KUBUS 3D ==================
vertices_cube = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1,  1), (1, 1,  1), (-1, -1, 1), (-1, 1, 1)
)

edges = (
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,7),(7,6),(6,4),
    (0,4),(1,5),(2,7),(3,6)
)

def draw_cube():
    glColor3f(1,1,1)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_cube[vertex])
    glEnd()

# ================== PERSEGI 2D ==================
square = [(-1,-1),(1,-1),(1,1),(-1,1)]

def draw_square():
    glColor3f(0,0,1)
    glBegin(GL_QUADS)
    for x,y in square:
        glVertex2f(x,y)
    glEnd()

# ================== MAIN ==================
def main():
    pygame.init()
    display = (900,600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Kubus 3D & Persegi 2D")

    glEnable(GL_DEPTH_TEST)   # PENTING UNTUK 3D
    glClearColor(0,0,0,1)

    # Kamera
    gluPerspective(45, display[0]/display[1], 0.1, 100.0)
    glTranslatef(0,0,-20)

    # Transformasi Kubus
    cube_x, cube_y = -6, 0
    cube_rot = 0
    cube_scale = 1

    # Transformasi Persegi
    sq_x, sq_y = 6, 0
    sq_rot = 0
    sq_scale = 1
    shear = 0
    reflect = 1

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                # === KUBUS 3D ===
                if event.key == K_w: cube_y += 0.3
                if event.key == K_s: cube_y -= 0.3
                if event.key == K_a: cube_x -= 0.3
                if event.key == K_d: cube_x += 0.3
                if event.key == K_q: cube_rot += 5
                if event.key == K_e: cube_rot -= 5
                if event.key == K_z: cube_scale -= 0.1
                if event.key == K_x: cube_scale += 0.1

                # === PERSEGI 2D ===
                if event.key == K_i: sq_y += 0.3
                if event.key == K_k: sq_y -= 0.3
                if event.key == K_j: sq_x -= 0.3
                if event.key == K_l: sq_x += 0.3
                if event.key == K_u: sq_rot += 5
                if event.key == K_o: sq_rot -= 5
                if event.key == K_n: sq_scale -= 0.1
                if event.key == K_m: sq_scale += 0.1
                if event.key == K_h: shear += 0.2
                if event.key == K_r: reflect *= -1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # ----- KUBUS 3D -----
        glPushMatrix()
        glTranslatef(cube_x, cube_y, 0)
        glRotatef(cube_rot, 1,1,0)
        glScalef(cube_scale, cube_scale, cube_scale)
        draw_cube()
        glPopMatrix()

        # ----- PERSEGI 2D -----
        glPushMatrix()
        glTranslatef(sq_x, sq_y, 0)
        glRotatef(sq_rot, 0,0,1)
        glScalef(sq_scale * reflect, sq_scale, 1)

        shear_matrix = [
            1, shear, 0, 0,
            0, 1,     0, 0,
            0, 0,     1, 0,
            0, 0,     0, 1
        ]
        glMultMatrixf(shear_matrix)

        draw_square()
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

main()

