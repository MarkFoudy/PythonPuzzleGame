from turtle import *

def draw_rec(t,x,y,width,height,size,color):
    #t.setup(fill)
    t.hideturtle()
    t.pencolor(color)
    t.pensize(size)
    t.setheading(0)
    t.speed(10)

    #board.begin_fill()
    t.up()
    t.goto(x,y)
    t.down()
    # draw top
    t.forward(width)
    # draw right
    t.right(90)
    t.forward(height)
    # draw bottom
    t.right(90)
    t.forward(width)
    # draw left
    t.right(90)
    t.forward(height)
    #board.end_fill()
