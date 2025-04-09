#include <GL/glut.h>
#include <cmath>
#include <vector>
#include <string>

const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;

struct Pixel {
    int x, y;
    float intensity;
    bool isPrimary;
};

// Cubic polynomial filter for intensity
float filter(float distance) {
    if (distance < 0.5f) return 1.0f - 2.0f * distance * distance;
    if (distance < 1.5f) return 2.0f * (1.5f - distance) * (1.5f - distance);
    return 0.0f;
}

std::vector<Pixel> guptaSproull(int x0, int y0, int x1, int y1) {
    std::vector<Pixel> pixels;

    int dx = x1 - x0;
    int dy = y1 - y0;
    bool steep = std::abs(dy) > std::abs(dx);

    if (steep) {
        std::swap(x0, y0);
        std::swap(x1, y1);
        dx = x1 - x0;
        dy = y1 - y0;
    }
    if (x0 > x1) {
        std::swap(x0, x1);
        std::swap(y0, y1);
        dx = x1 - x0;
        dy = y1 - y0;
    }

    int x = x0, y = y0;
    int d = 2 * dy - dx; // Bresenham’s Initial Decision Parameter
    float length = std::sqrt(dx * dx + dy * dy);
    float sin_theta = dx / length;
    float cos_theta = dy / length;
    float D = 0.0f; // Perpendicular distance

    while (x <= x1) {
        int plot_x = steep ? y : x;
        int plot_y = steep ? x : y;
        pixels.push_back({plot_x, plot_y, 1.0f, true});

        // Anti-aliasing for three pixels
        for (int offset = -1; offset <= 1; offset++) {
            float distance = D + offset * cos_theta;
            float intensity = filter(std::abs(distance));
            if (intensity > 0.0f && offset != 0) {
                int yp = plot_y + offset;
                pixels.push_back({plot_x, yp, intensity, false});
            }
        }

        x++;
        if (d <= 0) {
            D += sin_theta;
            d += 2 * dy;
        } else {
            y++;
            D += sin_theta - cos_theta;
            d += 2 * (dy - dx);
        }
    }

    return pixels;
}

void drawText(const char* text, float x, float y) {
    glRasterPos2f(x, y);
    for (const char* c = text; *c != '\0'; c++) {
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, *c);
    }
}

void drawGrid() {
    glColor3f(0.7f, 0.7f, 0.7f);
    glBegin(GL_LINES);
    for (int x = 0; x <= 40; x += 5) {
        glVertex2i(x, 0);
        glVertex2i(x, 40);
    }
    for (int y = 0; y <= 40; y += 5) {
        glVertex2i(0, y);
        glVertex2i(40, y);
    }
    glEnd();

    glColor3f(0.0f, 0.0f, 0.0f);
    glBegin(GL_LINES);
    glVertex2i(0, 0);
    glVertex2i(40, 0);
    glVertex2i(0, 0);
    glVertex2i(0, 40);
    glEnd();

    for (int x = 0; x <= 40; x += 5) {
        std::string label = std::to_string(x);
        drawText(label.c_str(), x - 1, -2);
    }
    for (int y = 5; y <= 40; y += 5) {
        std::string label = std::to_string(y);
        drawText(label.c_str(), -3, y - 1);
    }
}

void drawLine() {
    glClear(GL_COLOR_BUFFER_BIT);
    drawGrid();

    int x0 = 20, y0 = 10;
    int x1 = 30, y1 = 18;

    std::vector<Pixel> pixels = guptaSproull(x0, y0, x1, y1);

    glLineWidth(1.0f);
    glColor3f(0.0f, 0.0f, 0.0f);
    glBegin(GL_LINE_STRIP);
    for (const auto& pixel : pixels) {
        if (pixel.isPrimary) glVertex2i(pixel.x, pixel.y);
    }
    glEnd();

    glPointSize(2.0f);
    glBegin(GL_POINTS);
    for (const auto& pixel : pixels) {
        if (!pixel.isPrimary) {
            glColor4f(0.0f, 0.0f, 0.0f, pixel.intensity);
            glVertex2i(pixel.x, pixel.y);
        }
    }
    glEnd();

    glColor3f(1.0f, 0.0f, 0.0f);
    std::string startLabel = "(" + std::to_string(x0) + "," + std::to_string(y0) + ")";
    std::string endLabel = "(" + std::to_string(x1) + "," + std::to_string(y1) + ")";
    drawText(startLabel.c_str(), x0, y0 - 1.5f);
    drawText(endLabel.c_str(), x1, y1 + 1.5f);

    glFlush();
}

void init() {
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(-5, 45, -5, 45);
    glMatrixMode(GL_MODELVIEW);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    glEnable(GL_POINT_SMOOTH);
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_MULTISAMPLE);
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT);
    glutCreateWindow("Gupta-Sproull Anti-Aliased Line");
    init();
    glutDisplayFunc(drawLine);
    glutMainLoop();
    return 0;
}