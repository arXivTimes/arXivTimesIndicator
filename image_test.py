import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.image import BboxImage, imread
from matplotlib.transforms import Bbox
from PIL import Image
import seaborn as sns

# global setting
matplotlib.rcParams["figure.dpi"] = 70
matplotlib.rcParams["savefig.dpi"] = 70
IMG_ROOT = "./images"


def main():
    image_paths = os.listdir("./images")
    image_paths = [os.path.join(IMG_ROOT, p) for p in image_paths]
    images = [Image.open(p) for p in image_paths]

    draw_icon_bars(images)
    draw_text_chart(images)


def draw_icon_bars(images, max_value=20):
    y = np.random.randint(max_value, size=len(images))
    x = np.array(range(len(images)))
    ax = sns.barplot(x=x, y=y, ci=None)
    ax.set_ylim((0, max_value))

    # erase ticks
    ax.get_xaxis().set_ticklabels([], fontsize=45)  # expand label size by fontsize parameter

    TICK_POS = -0.5  # vertical position of icon in graph y-grid
    SIZE_IN_TICK = 2  # icon size measured in y-grid        

    for i, _x in enumerate(x):
        leftDown, rightUpper = get_icon_position_from_order(ax, i, SIZE_IN_TICK, vertical_position=TICK_POS, offset=-0.25)
        bbox_image = BboxImage(Bbox([leftDown, rightUpper]),
                            norm = None,
                            origin=None,
                            clip_on=False
                            )
        bbox_image.set_data(images[i])
        ax.add_artist(bbox_image)
    
    fig = ax.get_figure()
    fig.savefig("icon_plot.PNG", bbox_inches="tight")


def draw_text_chart(images, max_value=100):
    data = {
    "Optimization as a Model for Few-Shot Learning": 70,
    "Adversarially Regularized Autoencoders for Generating Discrete Structures": 30,
    "Train longer, generalize better: closing the generalization gap in large batch training of neural networks": 50
    }

    titles = []
    values = []

    for d in data:
        titles.append(d)
        values.append(data[d])
    
    paper_count = len(values)
    width = 0.5
    figsize_v = (width * 2) * paper_count

    fig, ax = plt.subplots(figsize=(18, figsize_v))
    ax.set_xlim((0, max_value))
    ax.patch.set_facecolor("white")
    ax.barh(list(range(paper_count)), values, width, color="#faf0e6")
    ax.grid("off")
    ax.set_yticks([])
    for p in ["top", "left", "right"]:
        ax.spines[p].set_visible(False)
    for i, t in enumerate(titles):
        ax.text(0, i, t, fontsize=16)
        
    TICK_POS = -1.25  # horizontal position of icon in graph y-grid
    SIZE_IN_TICK = width  # icon in graph y-grid

    for i, _y in enumerate(range(paper_count)):
        leftDown, rightUpper = get_icon_position_from_order(ax, i, SIZE_IN_TICK, horizontal_position=TICK_POS)
        bbox_image = BboxImage(Bbox([leftDown, rightUpper]),
                            norm = None,
                            origin=None,
                            clip_on=False
                            )
        bbox_image.set_data(images[i])
        ax.add_artist(bbox_image)

    fig = ax.get_figure()
    fig.savefig("text_plot.PNG", bbox_inches="tight")


def get_icon_position_from_order(ax, order, icon_size, vertical_position=None, horizontal_position=None, offset=0):
    if vertical_position is None and horizontal_position is None:
        raise Exception("You have to specify vertical or horizontal position.")
    elif vertical_position is not None and horizontal_position is not None:
        raise Exception("You have to specify vertical or horizontal position.")
    
    if vertical_position is not None:
        vertical_plot = True
    elif horizontal_position is not None:
        vertical_plot = False

    scale = ax.transData.transform((1, 1)) - ax.transData.transform((0, 0))
    x_scale = scale[1] / scale[0]

    if vertical_plot:
        pos = order + offset
        left = pos - (icon_size * x_scale / 2)
        down = vertical_position - icon_size
        right = pos + (icon_size * x_scale / 2)
        top = vertical_position
    else:
        pos = order + offset
        left =  (horizontal_position - icon_size) * x_scale
        down =  pos - (icon_size / 2)
        right = horizontal_position * x_scale
        top = pos + (icon_size / 2)

    leftDown = ax.transData.transform((left, down))
    rightUpper = ax.transData.transform((right, top))
    return leftDown, rightUpper


if __name__ == "__main__":
    main()
