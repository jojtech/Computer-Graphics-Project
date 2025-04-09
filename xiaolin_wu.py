from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Window dimensions (scaled to fit the range 0 to 40)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_HEIGHT = 40  # Maximum y-value in the grid

# Colors (normalized to [0, 1] for OpenGL)
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)
GRAY = (0.7, 0.7, 0.7)
RED = (1.0, 0.0, 0.0)

# List to store pixels and their intensities
pixels = []

# Xiaolin Wu's line algorithm
def xiaolin_wu(x0, y0, x1, y1):
    global pixels
    pixels = []

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = float(dy) / dx if dx != 0 else 0

    # First endpoint
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = 1.0 - (x0 + 0.5 - math.floor(x0 + 0.5))
    xpxl1 = int(xend)
    ypxl1 = int(math.floor(yend))
    yfrac1 = yend - ypxl1
    if steep:
        pixels.append((ypxl1, xpxl1, (1.0 - yfrac1) * xgap))
        pixels.append((ypxl1 + 1, xpxl1, yfrac1 * xgap))
    else:
        pixels.append((xpxl1, ypxl1, (1.0 - yfrac1) * xgap))
        pixels.append((xpxl1, ypxl1 + 1, yfrac1 * xgap))

    intery = yend + gradient

    # Second endpoint
    xend = round(x1)
    yend = y1 - gradient * (xend - x1)
    xgap = x1 + 0.5 - math.floor(x1 + 0.5)
    xpxl2 = int(xend)
    ypxl2 = int(math.floor(yend))
    yfrac2 = yend - ypxl2
    if steep:
        pixels.append((ypxl2, xpxl2, (1.0 - yfrac2) * xgap))
        pixels.append((ypxl2 + 1, xpxl2, yfrac2 * xgap))
    else:
        pixels.append((xpxl2, ypxl2, (1.0 - yfrac2) * xgap))
        pixels.append((xpxl2, ypxl2 + 1, yfrac2 * xgap))

    # Main loop
    for x in range(xpxl1 + 1, xpxl2):
        y_floor = int(math.floor(intery))
        y_frac = intery - y_floor
        if steep:
            pixels.append((y_floor, x, 1.0 - y_frac))
            pixels.append((y_floor + 1, x, y_frac))
        else:
            pixels.append((x, y_floor, 1.0 - y_frac))
            pixels.append((x, y_floor + 1, y_frac))
        intery += gradient

# Function to draw text at a given position
def draw_text(text, x, y):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))

# Function to draw the grid, axes, and labels
def draw_grid():
    glColor3f(*GRAY)
    glBegin(GL_LINES)
    for x in range(0, 41, 5):
        glVertex2f(x, 0)
        glVertex2f(x, GRID_HEIGHT)
    for y in range(0, 41, 5):
        glVertex2f(0, y)
        glVertex2f(40, y)
    glEnd()

    glColor3f(*BLACK)
    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(40, 0)
    glVertex2f(0, 0)
    glVertex2f(0, 40)
    glEnd()

    glColor3f(*BLACK)
    for x in range(0, 41, 5):
        draw_text(str(x), x - 0.5, -1)
    for y in range(0, 41, 5):
        if y > 0:
            draw_text(str(y), -2, y)

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grid()

    x0, y0 = 15, 10
    x1, y1 = 23, 18
    xiaolin_wu(x0, y0, x1, y1)

    # Draw the line connecting the endpoints
    glColor3f(*BLACK)  
    glBegin(GL_LINES)
    glVertex2f(x0, y0)  
    glVertex2f(x1, y1)  
    glEnd()

    # Draw all pixels with anti-aliasing
    glPointSize(4.0)
    glBegin(GL_POINTS)
    for x, y, intensity in pixels:
        glColor4f(0.0, 0.0, 0.0, intensity) 
        glVertex2f(x, y)
    glEnd()

    glColor3f(*RED)
    draw_text(f"({x0},{y0})", x0 - 1.5, y0 + 1.5)
    draw_text(f"({x1},{y1})", x1 - 1.5, y1 - 1.5)

    glFlush()

# Initialize OpenGL
def init():
    glClearColor(*WHITE, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-5, 45, -5, 45)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow("Xiaolin Wu Line Drawing".encode())
    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
