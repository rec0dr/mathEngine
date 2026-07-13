import pygame
from graphing.renderer import Renderer
from graphing.viewport import Viewport
from functions.__init__ import Exponential, LinEq, Logarithm, Polynomial, Sinusoid, TrigType
from functions.symbols import X
from styles.line_style import LineStyle

pygame.init()
w,h = (800, 800)
screen = pygame.display.set_mode((w,h))
viewport = Viewport(w,h)

renderer = Renderer(screen, viewport)
cstyle = LineStyle(color=(255,0,0), opacity=128, thickness=1)
print([(*cstyle.color, cstyle.opacity), cstyle.thickness])
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dx, dy = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0]:
        dx, dy = -dx, dy
        viewport.pan_pixels(dx,dy, sensitivity=50)

    renderer.clear()
    renderer.draw_axes()
    renderer.draw_function(Sinusoid.from_basic(TrigType.TAN), style=cstyle)

    screen.blit(renderer.overlay, (0,0))
    pygame.display.flip()

pygame.quit()
