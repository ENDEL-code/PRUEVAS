from turtle import *

bgcolor("black")
speed(0)
penup()
hideturtle()

pixel_size = 50  # Tamaño más pequeño para que quepan 50x50 en pantalla

# Tu diseño original de 20x20
diseño_original = [
    [0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
    [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],
    [0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0]
]

# Crear matriz 50x50 con el diseño centrado
matriz = [[0 for _ in range(50)] for _ in range(50)]
offset_x = 15  # margen izquierdo
offset_y = 15  # margen superior

for y in range(len(diseño_original)):
    for x in range(len(diseño_original[0])):
        matriz[y + offset_y][x + offset_x] = diseño_original[y][x]

# Dibujar la matriz
for y in range(50):
    for x in range(50):
        valor = matriz[y][x]
        if valor == 1:
            color("white")
        else:
            color("black")
        goto(x * pixel_size - 250, -y * pixel_size + 250)
        begin_fill()
        for _ in range(4):
            forward(pixel_size)
            right(90)
        end_fill()

done()
