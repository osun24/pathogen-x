import numpy as np
import matplotlib.pyplot as plt

values = np.random.normal(0.5, 0.1, 1000)

plt.hist(values, bins=30, density=True)
plt.show()