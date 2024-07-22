import matplotlib.pyplot as plt
import numpy as np

##--------------------------------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------------------------------##

## Figure Setup :

# Axis range
x_data = [x for x in range(-18, 19)]
y_data = [y for y in range(-9, 10)]

# Width/Height in Inch (DPI = 100)
fig_width = 16
fig_height = 9.5

fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)

# Axis limits
ax.set_xlim(min(x_data), max(x_data))
ax.set_ylim(min(y_data), max(y_data))
ax.axhline(0, color='black',linewidth=2)
ax.axvline(0, color='black',linewidth=2)

# Ticks (Numerical labels)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Tick positions
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Plot covers the entire figure area
plt.tight_layout()

# Set the axis limits to be symmetric around the origin
limit_x, limit_y = max(x_data), max(y_data)
ax.set_xlim(-limit_x, limit_x)
ax.set_ylim(-limit_y, limit_y)
# Set the ticks and labels
ax.set_xticks(range(-limit_x+1, limit_x+1, 1))
ax.set_yticks(range(-limit_y+1, limit_y+1, 1))

# Add grid lines
ax.grid(True)

# Adjust the subplots to remove any margins if needed
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)


##--------------------------------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------------------------------##

## Calculations / Plotting :

X = np.linspace(-18, 18, 200)
xSqr = [x**2 for x in X]


## PI-Scape DPI : (43 for X values, 52 for the Y ones)

plt.plot(X, xSqr)

xSqr = [(x,y) for x,y in zip(X,xSqr)]
print(xSqr)
# Display the plot
plt.show()

