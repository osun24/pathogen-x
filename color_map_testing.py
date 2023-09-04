import matplotlib.pyplot as plt
import matplotlib.cm as cm

def get_color(number):
    colormap = cm.get_cmap("Spectral")  # "bwr" is a blue to white to red colormap
    rgba = colormap(number)
    rgb = rgba[:3]
    rgb = [int(255 * x) for x in rgb]
    return rgb

print(get_color(0.5))