import matplotlib.pyplot as plt
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox
import seaborn as sns


def save_bar_graph(x, y, file_name):
    plt.clf()
    sns.set_style("whitegrid")
    ax = sns.barplot(x=x, y=y)
    for item in ax.get_xticklabels():
        item.set_rotation(15)
    plt.savefig(file_name)


def save_graph_with_icon(x, y, images, file_name):
    plt.clf()
    sns.set_style("whitegrid")
    ax = sns.barplot(x=x, y=y, ci=None)

    # erase ticks
    ax.get_xaxis().set_ticklabels([], fontsize=45)  # expand label size by fontsize parameter
    TICK_POS = -0.25
    SIZE_IN_TICK = 1

    scale = ax.transData.transform((1, 1)) - ax.transData.transform((0, 0))
    x_scale = scale[0] / scale[1]

    for i, _x in enumerate(x):
        label_x = _x  # adjustment is not needed in saved file
        left = label_x - (SIZE_IN_TICK / x_scale / 2)
        down = TICK_POS - SIZE_IN_TICK
        right = label_x + (SIZE_IN_TICK / x_scale / 2)
        top = TICK_POS
        leftDown = ax.transData.transform((left, down))
        rightUpper = ax.transData.transform((right, top))
        bbox_image = BboxImage(Bbox([leftDown, rightUpper]),
                               norm=None,
                               origin=None,
                               clip_on=False
                               )
        bbox_image.set_data(images[i])
        ax.add_artist(bbox_image)
    plt.savefig(file_name)


def save_text_graph(titles, values, file_name='rank.png'):
    plt.clf()
    fig, ax = plt.subplots(figsize=(20,3))
    ax.barh(list(range(len(values))), values, 0.8, color="#faf0e6")
    ax.grid("off")
    ax.set_yticks([])
    for p in ["top", "left", "right"]:
        ax.spines[p].set_visible(False)
    for i, t in enumerate(titles):
        ax.text(0, i, t, fontsize=18)
    plt.savefig(file_name)
