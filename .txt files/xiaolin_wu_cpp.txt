#include <GL/glut.h>
#include <cmath>
#include <vector>
#include <string>

const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;

struct Pixel {
    int x, y;
    float intensity;
};

std::vector<Pixel> xiaolinWu(int x0, int y0, int x1, int y1) {
    std::vector<Pixel> pixels;

    bool steep = std::abs(y1 - y0) > std::abs(x1 - x0);
    if (steep) {
        std::swap(x0, y0);
        std::swap(x1, y1);
    }
    if (x0 > x1) {
        std::swap(x0, x1);
        std::swap(y0, y1);
    }

    int dx = x1 - x0;
    int dy = y1 - y0;
    float gradient = dx == 0 ? 1.0f : static_cast<float>(dy) / dx;

    float xend = std::round(x0);
    float yend = y0 + gradient * (xend - x0);
    float xgap = 1.0f - (x0 + 0.5f - std::floor(x0 + 0.5f));
    int xpxl1 = static_cast<int>(xend);
    int ypxl1 = static_cast<int>(std::floor(yend));
    float yfrac1 = yend - ypxl1;
    if (steep) {
        pixels.push_back({ypxl1, xpxl1, (1.0f - yfrac1) * xgap});
        pixels.push_back({ypxl1 + 1, xpxl1, yfrac1 * xgap});
    } else {
        pixels.push_back({xpxl1, ypxl1, (1.0f - yfrac1) * xgap});
        pixels.push_back({xpxl1, ypxl1 + 1, yfrac1 * xgap});
    }

    float intery = yend + gradient;

    xend = std::round(x1);
    yend = y1 - gradient * (xend - x1);
    xgap = x1 + 0.5f - std::floor(x1 + 0.5f);
    int xpxl2 = static_cast<int>(xend);
    int ypxl2 = static_cast<int>(std::floor(yend));
    float yfrac2 = yend - ypxl2;
    if (steep) {
        pixels.push_back({ypxl2, xpxl2, (1.0f - yfrac2) * xgap});
        pixels.push_back({ypxl2 + 1, xpxl2, yfrac2 * xgap});
    } else {
        pixels.push_back({xpxl2, ypxl2, (1.0f - yfrac2) * xgap});
        pixels.push_back({xpxl2, ypxl2 + 1, yfrac2 * xgap});
    }

    for (int x = xpxl1 + 1; x < xpxl2; x++) {
        int y_floor = static_cast<int>(std::floor(intery));
        float y_frac = intery - y_floor;
        if (steep) {
            pixels.push_back({y_floor, x, 1.0f - y_frac});
            pixels.push_back({y_floor + 1, x, y_frac});
        } else {
            pixels.push_back({x, y_floor, 1.0f - y_frac});
            pixels.push_back({x, y_floor + 1, y_frac});
        }
        intery += gradient;
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

    int x0 = 15, y0 = 10;
    int x1 = 23, y1 = 18;

    std::vector<Pixel> pixels = xiaolinWu(x0, y0, x1, y1);

    // Draw the line connecting the endpoints
    glColor3f(0.0f, 0.0f, 0.0f);  
    glBegin(GL_LINES);
    glVertex2i(x0, y0); 
    glVertex2i(x1, y1);  
    glEnd();

    // Draw all pixels with anti-aliasing
    glPointSize(2.0f);
    glBegin(GL_POINTS);
    for (const auto& pixel : pixels) {
        glColor4f(0.0f, 0.0f, 0.0f, pixel.intensity); 
        glVertex2i(pixel.x, pixel.y);
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
    glEnable(GL_POINT_SMOOTH);
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_MULTISAMPLE);
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT);
    glutCreateWindow("Xiaolin Wu Anti-Aliased Line");
    init();
    glutDisplayFunc(drawLine);
    glutMainLoop();
    return 0;
}