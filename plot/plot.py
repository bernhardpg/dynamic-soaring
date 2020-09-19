import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_input_slotine_glider(t, u_trj):
    plt.subplots(figsize=(5, 3))

    plt.subplot(2, 1, 1)
    plt.title("Input")
    plt.plot(t, u_trj[:, 0])
    plt.xlabel("time (seconds)")
    plt.ylabel("Lift coefficient")

    plt.subplot(2, 1, 2)
    plt.plot(t, u_trj[:, 1])
    plt.xlabel("time (seconds)")
    plt.ylabel("Roll (radians)")

    return


def plot_trj_3_wind(x_trj, wind_field_fn, dir_vector):
    # To make the plot function general:
    #   x_trj.shape = (N, 3)
    #   x_trj = [x, y, z]
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    x0 = x_trj[0, :]

    x_min = min(x_trj[:, 0])
    x_max = max(x_trj[:, 0])
    y_min = min(x_trj[:, 1])
    y_max = max(x_trj[:, 1])
    z_min = 0
    z_max = max(x_trj[:, 2])

    dx = np.abs(x_min - x_max) / 5 - 1
    dy = np.abs(y_min - y_max) / 5 - 1
    dz = np.abs(z_min - z_max) / 3 - 1

    # Plot wind field
    x, y, z = np.meshgrid(
        # (-min, max, step_length)
        np.arange(x_min, x_max, dx),
        np.arange(y_min, y_max, dy),
        np.arange(z_min, z_max, dz),
    )
    u, v, w = wind_field_fn(x, y, z)
    ax.quiver(
        x,
        y,
        z,
        u,
        v,
        w,
        length=1,#np.sqrt(dx ** 2 + dy ** 2) / 15,
        linewidth=0.7,
        arrow_length_ratio=0.1,
        pivot="middle",
    )

    # Plot trajectory
    ax.plot(
        x_trj[:, 0],
        x_trj[:, 1],
        x_trj[:, 2],
        label="Flight path",
        color="red",
        linewidth=1,
    )

    # Plot start position
    ax.scatter(x0[0], x0[1], x0[2])

    # Plot direction vector
    ax.quiver(
        x0[0],
        x0[1],
        x0[2],
        dir_vector[0],
        dir_vector[1],
        0,
        color="green",
        label="Desired direction",
        length=np.sqrt(dx ** 2 + dy ** 2),
        arrow_length_ratio=0.1,
    )

    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title("Trajectory")

    return