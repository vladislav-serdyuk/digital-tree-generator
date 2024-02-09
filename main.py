import tkinter
from tkinter import Tk, Canvas

from TreeTools import Genome, rand_genome, interbreed_with_mut
import TreeTools


def create_tree(genome):
    global cur_gen
    global cur_tree
    print('delete')
    TreeTools.delete(cur_tree)
    print('end')
    print('create_tree')
    cur_tree = TreeTools.create_tree(canvas, genome, width // 2, height * 3 // 4)
    print('end')
    # root.after(5000, lambda: create_tree(rand_genome()))


def move(x: Genome, y: Genome):
    y.genome = x.genome.copy()
    create_tree(cur_gen)


def go_full_screen():
    global full_screen
    if full_screen:
        root.overrideredirect(False)
        # root.state('zoomed')  # full screen
    else:
        root.overrideredirect(True)  # delete - o x
        root.state('zoomed')  # full screen
    full_screen = not full_screen


root = Tk()

# for c in range(100):
#     root.columnconfigure(c, weight=1)
# for r in range(11):
#     root.rowconfigure(r, weight=1)

generate_button = tkinter.Button(root, text='generate', command=lambda: create_tree(rand_genome()))
generate_button.grid(row=0, column=0)

full_screen = False

go_full_screen_button = tkinter.Button(root, text='go full screen', command=go_full_screen)
go_full_screen_button.grid(row=0, column=1)

height = 870
width = 1596

canvas = Canvas(root, height=height, width=width, bg='#9b21a2')
canvas.grid(row=1, column=0, columnspan=100)

img = tkinter.PhotoImage(file='gorshok.png')
canvas.create_image(width / 2, height * 3 / 4 + 50, image=img)

cur_gen = rand_genome()
cur_tree = TreeTools.create_tree(canvas, rand_genome(), width // 2, height * 3 // 4)

# a = rand_genome()

# tkinter.Button(root, text='cur->a', command=lambda: move(cur_gen, a)).grid(row=0, column=1)
# tkinter.Button(root, text='a->cur', command=lambda: move(a, cur_gen)).grid(row=0, column=2)
# tkinter.Button(root, text='a+cur->a', command=lambda: move(interbreed_with_mut(a, cur_gen), a)).grid(row=0, column=3)
# tkinter.Button(root, text='a+cur->cur',
#                command=lambda: move(interbreed_with_mut(a, cur_gen), cur_gen)).grid(row=0, column=4)

create_tree(cur_gen)

root.bind('<space>', lambda event: create_tree(rand_genome()))

root.mainloop()
