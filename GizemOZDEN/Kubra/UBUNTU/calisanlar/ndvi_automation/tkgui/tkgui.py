# try to use a window, so the user can click on the img to chose x,y
# also type in other numeric values to see the change instantly
from tkinter import *
from PIL import ImageTk, Image
from skimage.transform import rotate
from skimage.io import imread, imsave
from skimage.draw import polygon
import numpy as np

src_img = r'IAWatson_E22_24___6_10_16smallplot_400ft.jpg'


def render(x, y, x_offset, y_offset, plot_x, plot_y, net_x, net_y, rownum, rangenum, angle_deg):
    # load image
    image = imread(src_img)

    # rotate
    image_new = rotate(image=image, angle=angle_deg, resize=True)

    # find point's new position
    angle_rad = angle_deg / 180 * np.pi
    cos = np.cos(angle_rad)
    sin = np.sin(angle_rad)
    center_val = np.ceil(len(image_new) / 2)
    shift = (len(image_new) - len(image)) / 2
    point = np.array((x + shift, -y - shift))
    center = np.array((center_val, -center_val))
    matrix = np.array(((cos, -sin), (sin, cos)))
    point_new = matrix.dot(point - center) + center
    x = point_new[0]
    y = -point_new[1]

    # compute ndvi mean
    vals = []
    for i in range(rownum):
        for j in range(rangenum):
            _x1 = x + j * net_x + x_offset
            _y1 = y + i * net_y + y_offset
            _x2 = _x1 + plot_x
            _y2 = _y1 + plot_y
            x1 = np.ceil(_x1)
            y1 = np.ceil(_y1)
            x2 = np.ceil(_x2)
            y2 = np.ceil(_y2)
            r = np.array([y1, y1, y2, y2])
            c = np.array([x1, x2, x2, x1])
            rr, cc = polygon(r, c)
            # pseudo code for ndvi mean
            # values = []
            # for pixel in image_new[rr, cc]:
            #     values.append(pixel.ndvi)
            # vals.append(sum(values)/len(values))
            value = 0
            for pixel in image_new[rr, cc]:
                value += sum(pixel)
            vals.append(value)

    # RGB sum normalisation
    mmax = max(vals)
    mmin = min(vals)
    rrange = mmax - mmin
    vals = tuple(map(lambda v: (mmax - v) / rrange, vals))

    # draw
    for i in range(rownum - 1, -1, -1):
        for j in range(rangenum):
            _x1 = x + j * net_x + x_offset
            _y1 = y + i * net_y + y_offset
            _x2 = _x1 + plot_x
            _y2 = _y1 + plot_y
            x1 = np.ceil(_x1)
            y1 = np.ceil(_y1)
            x2 = np.ceil(_x2)
            y2 = np.ceil(_y2)
            r = np.array([y1, y1, y2, y2])
            c = np.array([x1, x2, x2, x1])
            rr, cc = polygon(r, c)
            colour = vals[i * rangenum + j]
            image_new[rr, cc] = (colour, colour, colour)

    imsave(fname=r'tmp.jpg', arr=image_new)


def preview(event):
    global img
    x_val = int(x_input.get())
    y_val = int(y_input.get())
    net_x_val = float(net_x_input.get())
    net_y_val = float(net_y_input.get())
    plot_x_val = float(plot_x_input.get())
    plot_y_val = float(plot_y_input.get())
    offset_x_val = float(offset_x_input.get())
    offset_y_val = float(offset_y_input.get())
    angle_val = float(angle_input.get())
    rownum_val = int(rownum_input.get())
    rangenum_val = int(rangenum_input.get())
    render(x_val, y_val,
           offset_x_val, offset_y_val,
           plot_x_val, plot_y_val,
           net_x_val, net_y_val,
           rownum_val, rangenum_val,
           angle_val)
    # TODO take parts
    img = ImageTk.PhotoImage(Image.open(r'tmp.jpg').resize((512, 512)))
    img_lbl.configure(image=img)


root = Tk()

# img
open(r'tmp.jpg', "wb").write(open(src_img, "rb").read())
img = ImageTk.PhotoImage(Image.open(r"tmp.jpg").resize((512, 512)))
img_lbl = Label(root, image=img)
img_lbl.grid(row=0, columnspan=5)

# change quadrant
qd1 = Button(root, text="Quadrant 1")
qd1.grid(row=1, column=0)
qd2 = Button(root, text="Quadrant 2")
qd2.grid(row=1, column=1)
qd3 = Button(root, text="Quadrant 3")
qd3.grid(row=1, column=2)
qd4 = Button(root, text="Quadrant 4")
qd4.grid(row=1, column=3)
zoomout = Button(root, text="Zoom Out")
zoomout.grid(row=1, column=4)

# x, y
x = Label(root, text='x')
x.grid(row=2, column=0, sticky=E)
x_input = Entry(root)
x_input.grid(row=2, column=1)

y = Label(root, text='y')
y.grid(row=2, column=2, sticky=E)
y_input = Entry(root)
y_input.grid(row=2, column=3)

# net_x, net_y
net_x = Label(root, text='net_x')
net_x.grid(row=3, column=0, sticky=E)
net_x_input = Entry(root)
net_x_input.grid(row=3, column=1)

net_y = Label(root, text='net_y')
net_y.grid(row=3, column=2, sticky=E)
net_y_input = Entry(root)
net_y_input.grid(row=3, column=3)

# plot_x, plot_y
plot_x = Label(root, text='plot_x')
plot_x.grid(row=4, column=0, sticky=E)
plot_x_input = Entry(root)
plot_x_input.grid(row=4, column=1)

plot_y = Label(root, text='plot_y')
plot_y.grid(row=4, column=2, sticky=E)
plot_y_input = Entry(root)
plot_y_input.grid(row=4, column=3)

# offset_x, offset_y
offset_x = Label(root, text='offset_x')
offset_x.grid(row=5, column=0, sticky=E)
offset_x_input = Entry(root)
offset_x_input.grid(row=5, column=1)

offset_y = Label(root, text='offset_y')
offset_y.grid(row=5, column=2, sticky=E)
offset_y_input = Entry(root)
offset_y_input.grid(row=5, column=3)

# rownum, rangenum
rownum = Label(root, text='rownum')
rownum.grid(row=6, column=0, sticky=E)
rownum_input = Entry(root)
rownum_input.grid(row=6, column=1)

rangenum = Label(root, text='rangenum')
rangenum.grid(row=6, column=2, sticky=E)
rangenum_input = Entry(root)
rangenum_input.grid(row=6, column=3)

# angle_deg
angle = Label(root, text='angle_deg')
angle.grid(row=7, column=0, sticky=E)
angle_input = Entry(root)
angle_input.grid(row=7, column=1)

# preview button
pvu = Button(root, text="Preview")
pvu.grid(row=7, column=2, columnspan=3, sticky='we')
pvu.bind("<Button-1>", preview)

# status bar
status = Label(root, text="scale 1:1 row:1 col:1 display:1", bd=1, relief=SUNKEN, anchor=W)
status.grid(row=18, columnspan=5, sticky='we')

root.mainloop()
