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
cstyle = LineStyle(color=(255,0,0), thickness=5)
print(cstyle)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    renderer.clear()
    renderer.draw_axes()
    renderer.draw_function(Exponential.from_basic(2)*Sinusoid.from_basic(TrigType.COS), style=cstyle)

    pygame.display.flip()

pygame.quit()
