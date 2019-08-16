import aacgmv2
import numpy
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

print(numpy.array(aacgmv2.get_aacgm_coord(60, 15, 300, datetime(2019, 8, 16))))

def plotHeatmap(Data, Display, x, y):
    try:
        fig, ax = plt.subplots()
        im, cbar = heatmap(Data, y, x, ax=ax, cmap="afmhot", cbarlabel="Data Points/Hr")
        #texts = annotate_heatmap(im, valfmt="{x:.1f} t")
        #ax.set_title("{RADAR} RADAR points/hr {date} UTC".format(date=Data.date, RADAR=RADAR_Dict[Data.stid].name))
        plt.xlabel("Lattitude (deg)")
        plt.ylabel("Altitude (m)")
        fig.tight_layout()
        ax = plt.gca()
        ax.invert_yaxis()
        #saveLoc = "processed/point_heatmaps/{Location}_{date}_Red.png".format(Location=RADAR_Dict[Data.stid].name,date=Data.date)
        #fig.savefig(saveLoc)
        if Display == True:
            plt.show()
        else:
            plt.close()
    except Exception as err:
        print(err)

    return;


def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.
    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(numpy.arange(data.shape[1]))
    ax.set_yticks(numpy.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on bottom.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(numpy.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(numpy.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.
    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, numpy.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


date = datetime(2019, 8, 16)
division = 1
error = numpy.zeros((int(360/division),int(90/division)))
lattitude = range(0, 90, division)
longitude = range(-180, 180, division)
altitude = 100
i = 0

for lat in lattitude:
	for lon in longitude:
		print("{lat}, {lon}, {alt}".format(lat=lat, lon=lon, alt=altitude))
		Magnetic = aacgmv2.wrapper.convert_latlon(lat, lon, altitude, date, code='G2A')
		Magnetic = aacgmv2.convert(lat, lon, altitude, date, a2g=False)
		#Geographic = aacgmv2.convert_mlt([Magnetic[0], Magnetic[1], Magnetic[2]], date, m2a=True)
		Geographic = aacgmv2.convert_mlt([lat, lon, altitude], date, m2a=True)
		latError = lat - Geographic[0]
		lonError = lon - Geographic[1]
		altError = alt - Geographic[2]
		error[i] = sqrt(pow(latError, 2) + pow(lonError, 2) + pow(altError, 2))
		i += 1
plotHeatmap(error, True, lattitude, longitude)