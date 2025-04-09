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

# Lists to store pixels and their intensities
pixels = []

# Cubic polynomial filter for intensity
def filter(distance):
    if distance < 0.5:
        return 1.0 - 2.0 * distance * distance
    if distance < 1.5:
        return 2.0 * (1.5 - distance) * (1.5 - distance)
    return 0.0

# Gupta-Sproull line drawing algorithm
def gupta_sproull(x0, y0, x1, y1):
    global pixels
    pixels = []

    dx = x1 - x0
    dy = y1 - y0
    steep = abs(dy) > abs(dx)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        dx, dy = dy, dx

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        dx, dy = dx, dy

    x = x0
    y = y0
    d = 2 * dy - dx  # Bresenham’s initial decision parameter
    length = math.sqrt(dx * dx + dy * dy)
    sin_theta = dx / length
    cos_theta = dy / length
    D = 0.0  # Perpendicular distance

    while x <= x1:
        plot_x = y if steep else x
        plot_y = x if steep else y
        pixels.append((plot_x, plot_y, 1.0))  # Primary pixel

        # Anti-aliasing for three pixels
        for offset in [-1, 0, 1]:
            distance = D + offset * cos_theta
            intensity = filter(abs(distance))
            if intensity > 0.0:
                yp = plot_y + offset
                pixels.append((plot_x, yp, intensity))

        x += 1
        if d <= 0:
            D += sin_theta
            d += 2 * dy
        else:
            y += 1
            D += sin_theta - cos_theta
            d += 2 * (dy - dx)

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

    x0, y0 = 20, 10
    x1, y1 = 30, 18
    gupta_sproull(x0, y0, x1, y1)

    # Draw primary path
    glLineWidth(2.0)
    glColor3f(*BLACK)
    glBegin(GL_LINE_STRIP)
    for x, y, intensity in pixels:
        if intensity == 1.0:  # Primary pixels
            glVertex2f(x, y)
    glEnd()

    # Draw anti-aliased pixels
    glPointSize(4.0)
    glBegin(GL_POINTS)
    for x, y, intensity in pixels:
        if intensity < 1.0:  # Neighboring pixels
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
    glutCreateWindow("Gupta-Sproull Line Drawing".encode())
    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
