def plot_borders(borders):
    fig, ax = plt.subplots(figsize = (10, 8)) # increase the figure size to 10 x 8 
    borders.plot(ax=ax, edgecolor='black', linewidth=0.2) # set the borders to fine black lines
    plt.tick_params(left = False, bottom = False) # remove the spines
    plt.tick_params(labelleft = False, labelbottom = False) # remove the numbers
    plt.show()