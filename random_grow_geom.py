import matplotlib.pyplot as plt
import numpy as np

# Define model constants:
height = 500
width = 500
initial_seeds = 0.01
porosity = 0.5
particles = np.zeros((height, width), bool)

# Define growing possibility for different directions
directional_grow = np.array([0, 4, 4, 4, 4, 1, 1, 1, 1]) * 0.0001
top = np.random.rand(height, width)
bottom = np.random.rand(height, width)
right = np.random.rand(height, width)
left = np.random.rand(height, width)
topRight = np.random.rand(height, width)
bottomRight = np.random.rand(height, width)
topLeft = np.random.rand(height, width)
bottomLeft = np.random.rand(height, width)


# Define initial seeds
def seed(cd):
    mask = np.random.rand(height, width)
    particles[mask < cd] = True


# Define initial growing possibility for different seeds
def initiate():
    global particles, top, bottom, right, left, topRight, topLeft, bottomRight, bottomLeft
    top = np.random.rand(height, width) * particles
    bottom = np.random.rand(height, width) * particles
    right = np.random.rand(height, width) * particles
    left = np.random.rand(height, width) * particles
    topRight = np.random.rand(height, width) * particles
    bottomRight = np.random.rand(height, width) * particles
    topLeft = np.random.rand(height, width) * particles
    bottomLeft = np.random.rand(height, width) * particles


# Passing growing possibilities to surrounded cells
def stream():
    global top, bottom, right, left, topRight, topLeft, bottomRight, bottomLeft
    top = np.roll(top, 1, axis=0)  # axis 0 is north-south; + direction is north
    topRight = np.roll(topRight, 1, axis=0)
    topLeft = np.roll(topLeft, 1, axis=0)
    bottom = np.roll(bottom, -1, axis=0)
    bottomRight = np.roll(bottomRight, -1, axis=0)
    bottomLeft = np.roll(bottomLeft, -1, axis=0)
    right = np.roll(right, 1, axis=1)  # axis 1 is east-west; + direction is east
    topRight = np.roll(topRight, 1, axis=1)
    bottomRight = np.roll(bottomRight, 1, axis=1)
    left = np.roll(left, -1, axis=1)
    topLeft = np.roll(topLeft, -1, axis=1)
    bottomLeft = np.roll(bottomLeft, -1, axis=1)


# Grow cells according to weighted possibilities
def grow():
    global top, bottom, right, left, topRight, topLeft, bottomRight, bottomLeft, particles
    particles[(top < directional_grow[1]) & (top > 0)] = True
    particles[(bottom < directional_grow[2]) & (bottom > 0)] = True
    particles[(right < directional_grow[3]) & (right > 0)] = True
    particles[(left < directional_grow[4]) & (left > 0)] = True
    particles[(topRight < directional_grow[5]) & (topRight > 0)] = True
    particles[(topLeft < directional_grow[6]) & (topLeft > 0)] = True
    particles[(bottomRight < directional_grow[7]) & (bottomRight > 0)] = True
    particles[(bottomLeft < directional_grow[8]) & (bottomLeft > 0)] = True
    print(particles.sum() / (height * width))


# Grow cells according to weighted possibilities, including weighted direction
def grow_weighted():
    global top, bottom, right, left, topRight, topLeft, bottomRight, bottomLeft, particles
    rho = np.where(top == 0, 0, 1) + np.where(bottom == 0, 0, 1) + np.where(right == 0, 0, 1) + \
          np.where(left == 0, 0, 1) + 0.25 * np.where(topRight == 0, 0, 1) + 0.25 * \
          np.where(topLeft == 0, 0, 1) + 0.25 * np.where(bottomRight == 0, 0, 1) \
          + 0.25 * np.where(bottomLeft == 0, 0, 1)

    # Divide
    particles[(np.divide(top, rho, top, where=rho != 0) < directional_grow[1]) & (top > 0)] = True
    particles[(np.divide(bottom, rho, bottom, where=rho != 0) < directional_grow[2]) & (bottom > 0)] = True
    particles[(np.divide(right, rho, right, where=rho != 0) < directional_grow[3]) & (right > 0)] = True
    particles[(np.divide(left, rho, left, where=rho != 0) < directional_grow[4]) & (left > 0)] = True
    particles[(np.divide(topRight, rho, topRight, where=rho != 0) < directional_grow[5]) & (topRight > 0)] = True
    particles[(np.divide(topLeft, rho, topLeft, where=rho != 0) < directional_grow[6]) & (topLeft > 0)] = True
    particles[(np.power(bottomRight, rho) < directional_grow[7]) & (bottomRight > 0)] = True
    particles[(np.power(bottomLeft, rho) < directional_grow[8]) & (bottomLeft > 0)] = True
    print(particles[particles].sum() / (height * width))


def output_geom():
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(particles, interpolation='none', cmap='gray')
    plt.axis('off')
    fig.savefig(f'{height}_{width}_{initial_seeds}_{porosity}.png', dpi=300)
    plt.close()


def main():
    seed(initial_seeds)
    while particles.sum() / (height * width) < porosity:
        initiate()
        stream()
        grow_weighted()
    np.savetxt(f'{height}_{width}_{initial_seeds}_{porosity}.csv', particles, delimiter=",")
    output_geom()


if __name__ == '__main__':
    main()
