import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# initialize geometry requirements
height = 500
width = 500
num_particles = 400
num_of_repeats = 3
diameter = 50
domain = np.zeros((height, width), np.uint8)
MAX_TRY = 500000


def generate_particle():
    # randomly choose two points within the domain with distance of the diameter of the particle
    x1, y1 = np.random.randint(height), np.random.randint(width)
    theta = np.random.randint(360)
    particle = np.zeros((height, width), np.uint8)
    x2 = x1 + int(np.cos(np.pi * theta / 180) * diameter)
    y2 = y1 - int(np.sin(np.pi * theta / 180) * diameter)

    # Handling Periodic Boundary Condition
    horizontal_offset = 0
    vertical_offset = 0
    if x2 < 0:
        horizontal_offset = x2
    if y2 < 0:
        vertical_offset = y2
    if x2 > height - 1:
        horizontal_offset = x2 - (height - 1)
    if y2 > width - 1:
        vertical_offset = y2 - (width - 1)
    particle = cv.line(particle, (x1 - horizontal_offset, y1 - vertical_offset),
                       (x2 - horizontal_offset, y2 - vertical_offset), 1, 2)
    particle = np.roll(particle, vertical_offset, axis=0)
    particle = np.roll(particle, horizontal_offset, axis=1)
    return particle


# adding particles into the domain and avoid over-lapping
def add_particle(particle):
    global domain
    overlap = particle * domain
    if overlap.any() == 0:
        domain += particle
        return True
    else:
        return False


def output_geometry():
    np.savetxt(f'{height}_{width}_{num_particles}.csv', domain, delimiter=",")
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(1 - domain, interpolation='none', cmap='gray')
    fig.savefig(f'{height}_{width}_{num_particles}.png', dpi=300)
    plt.close()


def main():
    # for repeat in range(num_of_repeats):
    stop = 0
    num = 0
    while (num < num_particles) & (stop < MAX_TRY):
        particle = generate_particle()
        if add_particle(particle):
            num += 1
        stop += 1
    output_geometry()


if __name__ == '__main__':
    main()
