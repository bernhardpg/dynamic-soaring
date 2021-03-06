import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as ticker
import matplotlib.animation as animation

import numpy as np

from dynamics.wind_models import *

PLOT_LOCATION = "./results/plots/trajectory_angles/"
GRAPH_MARGIN = 300 # TODO bad solution, delete this


def plot_function_from_thesis():
    def func(x):
        a = 1
        b = 1
        return 1 / (a * x + b / x)

    x = np.arange(-10, 10, 0.1)
    plt.plot(x, func(x))
    plt.grid()
    plt.show()


def plot_sweep_polar(solution_avg_vel, solution_periods):
    fig, axes = plt.subplots(1, 2, subplot_kw={"projection": "polar"})

    avg_vel_list = list(solution_avg_vel.items())
    avg_vel_list_sorted = sorted(avg_vel_list, key=lambda x: float(x[0]))

    avg_vel_x, avg_vel_y = zip(*avg_vel_list_sorted)
    avg_vel_x = [float(i) * np.pi / 180 for i in avg_vel_x]
    avg_vel_y = [float(i) for i in avg_vel_y]
    max_vel = max(avg_vel_y)
    avg_vel_x.append(avg_vel_x[0])
    avg_vel_y.append(avg_vel_y[0])
    axes[0].plot(avg_vel_x, avg_vel_y)
    axes[0].set_title("Average velocities")
    axes[0].set_theta_zero_location("N")
    axes[0].set_theta_direction(-1)
    # Wind direction
    axes[0].annotate(
        "",
        xy=(0, max_vel * 3 / 4),
        xytext=(0, max_vel),
        arrowprops=dict(color="tab:blue", width=1, headlength=5, headwidth=5),
    )

    periods_list = list(solution_periods.items())
    periods_list_sorted = sorted(periods_list, key=lambda x: float(x[0]))

    periods_x, periods_y = zip(*periods_list_sorted)
    periods_x = [float(i) * np.pi / 180 for i in periods_x]
    periods_y = [float(i) for i in periods_y]
    max_period = max(periods_y)
    periods_x.append(periods_x[0])
    periods_y.append(periods_y[0])
    axes[1].plot(periods_x, periods_y)
    axes[1].set_title("Periods")
    axes[1].set_theta_zero_location("N")
    axes[1].set_theta_direction(-1)
    # Wind direction
    axes[1].annotate(
        "",
        xy=(0, max_period * 3 / 4),
        xytext=(0, max_period),
        arrowprops=dict(color="tab:blue", width=1, headlength=5, headwidth=5),
    )

    fig.savefig("./results/plots/polar_plot.pdf")

    max_vel_index = avg_vel_y.index(max_vel)
    max_vel_angle = avg_vel_x[max_vel_index]
    max_vel_period = periods_y[max_vel_index]

    print(
        "max_vel: {0} m/s\n\tpsi: {1} deg, period: {2}".format(
            max_vel, max_vel_angle * 180 / np.pi, max_vel_period
        )
    )
    return


def plot_powers(times, P_tot, P_dissipated, P_gained):
    max_power = max(max(P_tot), max(P_dissipated), max(P_gained))
    min_power = min(min(P_tot), min(P_dissipated), min(P_gained))
    fig, axes = plt.subplots(3, 1)
    tick_spacing = 1

    axes[0].plot(times, P_tot)
    axes[0].set_title("Total power")
    axes[0].set_ylim(min_power - GRAPH_MARGIN, max_power + GRAPH_MARGIN)
    axes[0].grid()
    axes[0].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    axes[1].plot(times, P_dissipated)
    axes[1].set_title("Power dissipated")
    axes[1].set_ylim(min_power - GRAPH_MARGIN, max_power + GRAPH_MARGIN)
    axes[1].grid()
    axes[1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    axes[2].plot(times, P_gained)
    axes[2].set_title("Power gained")
    axes[2].set_ylim(min_power - GRAPH_MARGIN, max_power + GRAPH_MARGIN)
    axes[2].grid()
    axes[2].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))


def plot_power_terms(
    times,
    P_dissipated,
    S_dyn_active,
    S_dyn_passive,
    E_dissipated,
    E_dyn_active,
    E_dyn_passive,
):
    max_power = max(max(P_dissipated), max(S_dyn_active), max(S_dyn_passive))
    min_power = min(min(P_dissipated), min(S_dyn_active), min(S_dyn_passive))
    power_limit = max(max_power, -min_power) * 1.25
    fig, axes = plt.subplots(3, 1)
    tick_spacing = 1

    axes[0].plot(times, P_dissipated)
    axes[0].fill_between(times, 0, E_dissipated, color="tab:purple", alpha=0.5)
    axes[0].set_title("Dissipated power")
    axes[0].set_ylim(-power_limit, power_limit)
    axes[0].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    axes[0].set_ylabel("$\mathcal{D} \, [W]$")
    plt.tight_layout()

    axes[1].plot(times, S_dyn_active)
    axes[1].fill_between(times, 0, E_dyn_active, color="tab:purple", alpha=0.5)
    axes[1].set_title("Active soaring power")
    axes[1].set_ylim(-power_limit, power_limit)
    axes[1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    axes[1].set_ylabel("$\mathcal{S}_{dyn, active} \, [W]$")
    plt.tight_layout()

    axes[2].plot(times, S_dyn_passive)
    axes[2].fill_between(times, 0, E_dyn_passive, color="tab:purple", alpha=0.5)
    axes[2].set_title("Passive soaring power")
    axes[2].set_ylim(-power_limit, power_limit)
    axes[2].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    axes[2].set_ylabel("$\mathcal{S}_{dyn, passive}$ \, [W]")
    axes[2].set_xlabel("time [s]")
    plt.tight_layout()


def plot_energies(times, E_tot, E_kin, E_pot):
    max_energy = max(max(E_tot), max(E_kin), max(E_pot))
    fig, axes = plt.subplots(3, 1)

    axes[0].plot(times, E_tot)
    axes[0].set_title("Total energy")
    axes[0].set_ylim(0, max_energy + GRAPH_MARGIN)
    axes[0].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axes[0].set_ylabel("$E \, [J]$")
    plt.tight_layout()

    axes[1].plot(times, E_kin)
    axes[1].set_title("Kinetic energy")
    axes[1].set_ylim(0, max_energy + GRAPH_MARGIN)
    axes[1].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axes[1].set_ylabel("$E_{kin} \, [J]$")
    plt.tight_layout()

    axes[2].plot(times, E_pot)
    axes[2].set_title("Potential energy")
    axes[2].set_ylim(0, max_energy + GRAPH_MARGIN)
    axes[2].set_ylabel("$E_{pot} \, [J]$")
    axes[2].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axes[2].set_xlabel("time [s]")
    plt.tight_layout()


def _plot_wind_profile(ax, wind_function, h_max=20):
    dh_arrows = 2.5

    h = np.arange(0.03, h_max, 0.05)
    ax.plot(wind_function(h), h, color="black")

    arrow_start = np.arange(dh_arrows, h_max, dh_arrows)
    wind_strengths = wind_function(arrow_start)
    zeros = np.zeros(arrow_start.shape[0])
    ax.quiver(
        zeros, arrow_start, wind_strengths, zeros, units="xy", scale=1, color="tab:blue"
    )
    ax.set_aspect("equal")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, h_max)
    # ax.grid()


def plot_wind_profiles():
    fig, axs = plt.subplots(1, 4, constrained_layout=True)
    fig.set_size_inches(10, 3)
    wind_profiles = [
        linear_wind_model,
        log_wind_model,
        exp_wind_model,
        logistic_wind_model,
    ]
    wind_profile_names = [
        "Linear",
        "Logarithmic",
        "Exponential",
        "Logistic",
    ]
    for i in range(len(wind_profiles)):
        ax = axs[i]
        _plot_wind_profile(ax, wind_profiles[i])
        ax.set_title(wind_profile_names[i])
        if i == 0:
            ax.set_xlabel("Wind strength [m/s]")
            ax.set_ylabel("Height [m]")

    plt.savefig(PLOT_LOCATION + "wind_models.eps", bbox_inches="tight")
    return


def plot_glider_angles(
    t,
    gamma_trj,
    psi_trj,
    phi_trj,
    max_bank_angle,
):
    plt.subplots()

    plt.subplot(3, 1, 1)
    plt.plot(t, phi_trj * 180 / np.pi)
    # plt.xlabel("time [s]")
    plt.title("Bank angle")
    plt.ylabel("$\phi \, [^\circ]$")
    plt.ylim((-110, 110))
    plt.hlines(
        (-max_bank_angle * 180 / np.pi, max_bank_angle * 180 / np.pi),
        t[0],
        t[-1],
        color="tab:red",
        linestyles="dashed",
        linewidth=1,
    )
    plt.xticks(np.arange(min(t), max(t), 1.0))
    plt.yticks(np.arange(-90, 90, 45))

    plt.subplot(3, 1, 2)
    plt.plot(t, gamma_trj * 180 / np.pi)
    plt.title("Rel. flight path angle")
    plt.ylabel("$\gamma \, [^\circ]$")
    plt.xticks(np.arange(min(t), max(t), 1.0))
    plt.ylim((-100, 100))
    plt.yticks(np.arange(-90, 90, 45))

    plt.subplot(3, 1, 3)
    plt.plot(t, psi_trj * 180 / np.pi)
    plt.title("Heading angle")
    plt.ylabel("$\psi \, [^\circ]$")
    plt.xticks(np.arange(min(t), max(t), 1.0))
    plt.ylim((-180, 181))
    plt.yticks(np.arange(-180, 180, 90))

    plt.tight_layout()

    # plt.savefig(PLOT_LOCATION + "attitude.pdf", bbox_inches="tight", pad_inches=0)

    return


def plot_glider_height_and_vel(t, speed_knots, height_knots, min_height, max_height):
    plt.subplots(figsize=(6, 3))
    height_limit = max(height_knots)

    plt.subplot(2, 1, 1)
    plt.plot(t, height_knots)
    plt.title("Height")
    plt.ylabel("$h \, [m]$")
    plt.ylim((0, height_limit * 1.25))
    plt.hlines(
        (min_height, max_height),
        t[0],
        t[-1],
        color="tab:red",
        linestyles="dashed",
        linewidth=1,
    )
    plt.xticks(np.arange(min(t), max(t), 1.0))
    plt.yticks(np.arange(0, height_limit, 5))
    plt.tight_layout()

    plt.subplot(2, 1, 2)
    plt.plot(t, speed_knots)
    plt.title("Inertial speed")
    plt.ylabel("$V [m/s]$")
    plt.ylim((0, max(speed_knots) * 1.25))
    plt.xlabel("time [s]")
    plt.xticks(np.arange(min(t), max(t), 1.0))
    plt.yticks(np.arange(0, max(speed_knots) * 1.25, 10))
    plt.tight_layout()

    return


def plot_glider_phys_quantities(
    t,
    u_trj,
    c_l_trj,
    n_trj,
    height_knots,
    max_lift_coeff,
    min_lift_coeff,
    max_load_factor,
    min_height,
    max_height,
):

    plt.subplots(figsize=(6, 3))

    plt.subplot(2, 1, 1)
    plt.plot(t, c_l_trj)
    # plt.xlabel("time [s]")
    plt.title("Lift coefficient")
    plt.ylabel("$c_L$")
    plt.hlines(
        (min_lift_coeff, max_lift_coeff),
        t[0],
        t[-1],
        color="tab:red",
        linestyles="dashed",
        linewidth=1,
    )
    plt.ylim((0, 2))
    plt.tight_layout()
    plt.xticks(np.arange(min(t), max(t), 1.0))
    plt.yticks(np.arange(0, 2, 1.0))

    plt.subplot(2, 1, 2)
    plt.plot(t, n_trj)
    plt.xlabel("time [s]")
    plt.title("Load factor")
    plt.ylabel("n")
    plt.ylim((0, max_load_factor * 1.25))
    plt.hlines(
        (0, max_load_factor),
        t[0],
        t[-1],
        color="tab:red",
        linestyles="dashed",
        linewidth=1,
    )
    plt.tight_layout()
    plt.xticks(np.arange(min(t), max(t), 1.0))
    plt.yticks(np.arange(0, max_load_factor* 1.25, 1.0))

    # plt.savefig(PLOT_LOCATION + "phys_quantities.pdf", bbox_inches="tight", pad_inches=0)
    return


def plot_glider_pos(
    x_trj,
    u_trj,
    traj_time,
    travel_angle,
    plot_axis="",
    save_traj=False,
):
    fig = plt.figure()
    ax = fig.gca(projection="3d")

    pos_trj = x_trj[:, 0:3]
    axis_limits = np.array(
        [
            [min(pos_trj[:, 0]), max(pos_trj[:, 0])],
            [min(pos_trj[:, 1]), max(pos_trj[:, 1])],
            [min(pos_trj[:, 2]), max(pos_trj[:, 2])],
        ]
    )
    #axis_limits[0,0] = -10 NOTE useful when plotting some trajectories
    # Draw projections on walls
    if "x" in plot_axis:
        _draw_trajectory_projection(pos_trj, axis_limits, ax, axis="x")
    if "y" in plot_axis:
        _draw_trajectory_projection(pos_trj, axis_limits, ax, axis="y")
    _draw_trajectory_projection(pos_trj, axis_limits, ax, axis="z")
    #    if draw_soaring_power == True:
    #        _draw_soaring_power_projection(
    #            pos_trj, soaring_power, axis_limits, ax, axis=plot_axis
    #        )

    # Draw trajectory
    _draw_pos_trajectory(pos_trj, travel_angle, axis_limits, ax)
    _draw_direction_vector(x_trj[0, :], travel_angle, axis_limits, ax)
    _draw_wind_field(axis_limits, ax)
    _draw_gliders(x_trj, u_trj, traj_time, ax)
    _set_real_aspect_ratio(axis_limits, ax)

    # ax.view_init(30, 50) # TODO change this to rotate plot
    fig.set_size_inches((13, 9))

    if save_traj:
        plt.savefig(
            PLOT_LOCATION + "trajectory_{:.1f}.pdf".format(travel_angle * 180 / np.pi),
            bbox_inches="tight",
            pad_inches=0,
        )
        plt.savefig(
            PLOT_LOCATION + "trajectory_{:.1f}.jpg".format(travel_angle * 180 / np.pi),
            bbox_inches="tight",
            pad_inches=0,
        )
    return


def _polygon_under_graph(xlist, ylist):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (xlist, ylist) line graph.  Assumes the xs are in ascending order.
    """
    return [(xlist[0], 0.0), *zip(xlist, ylist), (xlist[-1], 0.0)]


def _draw_soaring_power_projection(pos_trj, soaring_power, axis_limits, ax, axis="x"):
    N = pos_trj.shape[0]
    max_value = 5
    soaring_power *= max_value / max(soaring_power)

    if axis == "x":
        min_axis_value = axis_limits[0, 0]
        verts = [_polygon_under_graph(pos_trj[:, 1], soaring_power)]
        poly = PolyCollection(verts, facecolors="r", alpha=0.3)
        ax.add_collection3d(poly, zs=min_axis_value, zdir="x")

    if axis == "y":
        min_axis_value = axis_limits[1, 1]
        verts = [_polygon_under_graph(pos_trj[:, 0], soaring_power)]
        poly = PolyCollection(verts, facecolors="r", alpha=0.3)
        ax.add_collection3d(poly, zs=min_axis_value, zdir="y")


def _draw_trajectory_projection(pos_trj, axis_limits, ax, axis="x", filled=False):
    N = pos_trj.shape[0]
    if axis == "x":  # TODO are the axes switched here?
        min_axis_value = axis_limits[0, 0]
        traj_plot = ax.plot(
            np.ones(N) * min_axis_value,
            pos_trj[:, 1],
            pos_trj[:, 2],
            "--k",
            alpha=0.5,
            linewidth=0.7,
        )

    if axis == "y":
        min_axis_value = axis_limits[1, 1]
        traj_plot = ax.plot(
            pos_trj[:, 0],
            np.ones(N) * min_axis_value,
            pos_trj[:, 2],
            "--k",
            alpha=0.5,
            linewidth=0.7,
        )
    if axis == "z":
        min_axis_value = np.zeros(N)
        traj_plot = ax.plot(
            pos_trj[:, 0],
            pos_trj[:, 1],
            np.ones(N) * min_axis_value,
            "--k",
            alpha=0.5,
            linewidth=0.7,
        )


# Params:
# x_trj.shape = (N, 3)
# x_trj = [x, y, z]
def _draw_pos_trajectory(pos_trj, travel_angle, axis_limits, ax):
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = axis_limits
    x_diff = np.abs(x_min - x_max)
    y_diff = np.abs(y_min - y_max)
    z_diff = np.abs(z_min - z_max)

    traj_plot = ax.plot(
        pos_trj[:, 0],
        pos_trj[:, 1],
        pos_trj[:, 2],
        color="tab:red",
        linewidth=1,
    )

    # plot start position
    x0 = pos_trj[0, :]
    ax.scatter(x0[0], x0[1], 0, color="tab:red")

    if False:
        # plot end position
        N = pos_trj.shape[0]
        xf = pos_trj[N - 1, :]
        ax.scatter(xf[0], xf[1], 0, color="grey")

    # Set labels
    ax.set_xlabel(
        "East [m]", labelpad=20
    )  # TODO these padds must be adjusted for each plot
    ax.set_ylabel("North [m]", labelpad=20)
    ax.set_zlabel("Height [m]")

    # Set ticks
    x_ticks_spacing = 20 if x_diff >= 40 else 5
    y_ticks_spacing = 20 if y_diff >= 40 else 5
    z_ticks_spacing = 10 if z_diff >= 10 else 5

    ax.xaxis.set_ticks(
        np.arange(
            np.ceil(x_min / x_ticks_spacing) * x_ticks_spacing, x_max, x_ticks_spacing
        )
    )
    ax.yaxis.set_ticks(
        np.arange(
            np.ceil(y_min / y_ticks_spacing) * y_ticks_spacing, y_max, y_ticks_spacing
        )
    )
    ax.zaxis.set_ticks(np.arange(0, z_max, z_ticks_spacing))


def _draw_direction_vector(x0, travel_angle, axis_limits, ax):
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = axis_limits
    x_diff = np.abs(x_min - x_max)
    y_diff = np.abs(y_min - y_max)

    dir_vector = np.array([np.sin(travel_angle), np.cos(travel_angle)])
    dir_vector_length = np.sqrt(x_diff / 10 ** 2 + y_diff / 10 ** 2) * 15
    ax.quiver(
        x0[0],
        x0[1],
        0,
        dir_vector[0],
        dir_vector[1],
        0,
        color="grey",
        label="Desired direction",
        length=dir_vector_length,
        linewidth=1,
        arrow_length_ratio=0.1,
    )


def _draw_wind_field(axis_limits, ax):
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = axis_limits
    x_diff = np.abs(x_min - x_max)
    y_diff = np.abs(y_min - y_max)
    z_diff = np.abs(z_min - z_max)

    dz = 2.5

    # Plot wind field
    xs = np.ones(1) * np.ceil(x_min)
    ys = np.ones(4) * y_max
    zs = np.arange(0, z_max, dz)
    zs[0] = z_min

    X, Y, Z = np.meshgrid(xs, ys, zs)
    u, v, w = get_wind_field(X, Y, Z)
    ax.quiver(
        X,
        Y,
        Z,
        u,
        v,
        w,
        length=1,  # np.sqrt(dx ** 2 + dy ** 2) / 15,
        linewidth=0.8,
        arrow_length_ratio=0.1,
        color="tab:blue",
        alpha=0.7,
    )

    # Plot wind field graph
    xs = np.ones(100) * np.ceil(x_min)
    zs = np.linspace(0, z_max, 100)
    zs[0] = z_min
    ys = np.ones(100) * y_max - wind_model(zs)
    ax.plot(xs, ys, zs, color="tab:blue", alpha=0.7)


def _set_real_aspect_ratio(axis_limits, ax):
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = axis_limits
    x_diff = np.abs(x_min - x_max)
    y_diff = np.abs(y_min - y_max)
    z_diff = np.abs(z_min - z_max)

    origin = np.mean(axis_limits, axis=1)
    radius = 0.5 * np.max(np.abs(axis_limits[:, 1] - axis_limits[:, 0]))

    x, y, z = origin
    ax.set_xlim3d([x - x_diff / 2, x + x_diff / 2])
    ax.set_ylim3d([y - y_diff / 2, y + y_diff / 2])
    ax.set_zlim3d([0, z_diff])

    ax.set_box_aspect([x_diff, y_diff, z_diff])


def _draw_gliders(x_trj, u_trj, traj_time, ax):
    glider_interval = 1  # s
    scale = 1

    N = x_trj.shape[0]
    dt = int(N // traj_time)
    times = np.arange(0, traj_time, glider_interval)

    for t in times:
        i = int(t * dt)

        x = x_trj[i, :]
        c = u_trj[i, :]
        # Draw time in glider
        ax.text(x[0], x[1], x[2], "  {0}s".format(t))

        F, RF, RB, LF, LB, i_body, j_body, k_body = _get_glider_corners(x, c, scale)
        vertices = np.vstack([F, RF, RB, LB, LF, F]).T

        # Draw polygons
        ax.add_collection3d(
            Poly3DCollection(
                [vertices.T.tolist()], linewidths=1, facecolors="orange", alpha=1
            )
        )
        ax.add_collection3d(
            Line3DCollection([vertices.T.tolist()], linewidths=1, colors="k")
        )

        if False:  # NOTE set to true to enable axes on the glider
            _plot_glider_axes(x[0:3], i_body, j_body, k_body, scale, ax, axes="xyz")

        if False:  # NOTE Set to true to enable red and green "lights" on the glider
            ax.scatter(RF[0], RF[1], RF[2], color="red", s=6)
            ax.scatter(RB[0], RB[1], RB[2], color="red", s=6)
            ax.scatter(LF[0], LF[1], LF[2], color="green", s=6)
            ax.scatter(LB[0], LB[1], LB[2], color="green", s=6)

    return


def _plot_glider_axes(com, i_body, j_body, k_body, scale, ax, axes="xyz"):
    if "x" in axes:
        # Plot x axis
        ax.quiver(
            com[0],
            com[1],
            com[2],
            i_body[0],
            i_body[1],
            i_body[2],
            linewidth=2,
            color="red",
            length=scale * 3,
        )
    if "y" in axes:
        # Plot y axis
        ax.quiver(
            com[0],
            com[1],
            com[2],
            j_body[0],
            j_body[1],
            j_body[2],
            linewidth=2,
            color="green",
            length=scale * 3,
        )
    if "z" in axes:
        # Plot z axis
        ax.quiver(
            com[0],
            com[1],
            com[2],
            k_body[0],
            k_body[1],
            k_body[2],
            linewidth=2,
            color="blue",
            length=scale * 3,
        )


def _get_glider_corners(x, c, scale):
    sweep = 0.7
    tip_chord = 0.3
    b = 3.03
    dist_cg_front = 0.5
    # TODO chord =

    # Extract values
    p = x[0:3]
    v_r = x[3:6]
    h = p[2]

    # Define glider corners
    com_to_F = np.array([dist_cg_front, 0, 0]) * scale
    com_to_RF = np.array([dist_cg_front - sweep, b / 2, 0]) * scale
    com_to_RB = np.array([dist_cg_front - sweep - tip_chord, b / 2, 0]) * scale
    com_to_LF = np.array([com_to_RF[0], -com_to_RF[1], com_to_RF[2]])
    com_to_LB = np.array([com_to_RB[0], -com_to_RB[1], com_to_RB[2]])

    # Calculate heading
    # alpha = zhukovskii_glider.calc_rel_flight_path_angle(v_r)  # TODO fix this

    # TODO rotate by angle of attack??
    #    i_body = np.array(
    #        [
    #            [np.cos(alpha), 0, np.sin(alpha)],
    #            [0, 1, 0],
    #            [-np.sin(alpha), 0, np.cos(alpha)],
    #        ]
    #    ).dot(
    #        i_stability
    #    )  # Rotate i_stab by alpha around y axis to get i_body

    i_body = v_r / np.linalg.norm(v_r)  # i unit vec in stability frame
    j_body = -c / np.linalg.norm(c)  # j unit vector in body frame
    k_body = np.cross(i_body, j_body)
    R_ned_to_body = np.stack((i_body, j_body, k_body), axis=1)

    # Rotate glider vectors by rotation matrix
    rotated_com_to_F = R_ned_to_body.dot(com_to_F)
    rotated_com_to_RF = R_ned_to_body.dot(com_to_RF)
    rotated_com_to_RB = R_ned_to_body.dot(com_to_RB)
    rotated_com_to_LF = R_ned_to_body.dot(com_to_LF)
    rotated_com_to_LB = R_ned_to_body.dot(com_to_LB)

    # Calculate glider corners
    F = p + rotated_com_to_F  # Front
    RF = p + rotated_com_to_RF  # Right front
    RB = p + rotated_com_to_RB  # Right back
    LF = p + rotated_com_to_LF  # Left front
    LB = p + rotated_com_to_LB  # Left back

    # Plot all corners as vectors without arrowheads
    return F, RF, RB, LF, LB, i_body, j_body, k_body


# TODO old from here


# TODO OUTDATED with new relative model
def save_trajectory_gif(zhukovskii_glider, traj, travel_angle):
    ## ANIMATION FILE SETTINGS
    filepath = "./animations/"
    filename = "glider_psi_{0}_degs.mp4".format(int(travel_angle * (180 / np.pi)))
    Writer = animation.writers["ffmpeg"]
    writer = Writer(fps=int(1 / dt), metadata=dict(artist="Me"), bitrate=1800)

    # SETUP FIGURE
    fig = plt.figure(figsize=(13, 10))
    ax = fig.gca(projection="3d")

    t, x_trj, u_trj = traj
    N = x_trj.shape[0]
    dt = times[1] - times[0]
    T = 1 / dt

    x0 = x_trj[0, :]

    x_min = min(x_trj[:, 0])
    x_max = max(x_trj[:, 0])
    y_min = min(x_trj[:, 1])
    y_max = max(x_trj[:, 1])
    z_min = 0
    z_max = max(x_trj[:, 2])

    # Spacing for wind field
    dx = np.abs(x_min - x_max)
    dy = np.abs(y_min - y_max)
    dz = np.abs(z_min - z_max)
    max_axis = max([dx, dy, dz])

    x, y, z = np.meshgrid(
        # (-min, max, step_length)
        np.arange(x_min, x_min + max_axis, max_axis / 5 - 1),
        np.arange(y_min, y_min + max_axis, max_axis / 5 - 1),
        np.arange(z_min, z_min + max_axis, max_axis / 5 - 1),
    )
    u, v, w = get_wind_field(x, y, z)

    # Define three points on glider, defined in body frame
    scale = 8
    com_to_wing_vec = np.array([0, zhukovskii_glider.b / 2, 0]) * scale
    com_to_front_vec = np.array([zhukovskii_glider.glider_length, 0, 0]) * scale

    pos = ax.scatter([], [], [])
    w1 = ax.quiver([], [], [], [], [], [])
    w2 = ax.quiver([], [], [], [], [], [])
    w3 = ax.quiver([], [], [], [], [], [])

    def init():
        ax.set_zlim(0, max_axis)
        ax.set_xlim(x_min, x_min + max_axis)
        ax.set_ylim(y_min, y_min + max_axis)
        ax.plot(x_trj[:, 0], x_trj[:, 1], x_trj[:, 2], linewidth=0.7)  # Plot trajectory
        ax.scatter(x0[0], x0[1], x0[2])  # Plot initial position

        # plot wind field
        ax.quiver(
            x,
            y,
            z,
            u,
            v,
            w,
            length=1,
            linewidth=0.5,
            arrow_length_ratio=0.2,
            pivot="middle",
            color="tab:blue",
        )

        # Plot direction vector
        dir_vector = np.array([np.sin(travel_angle), np.cos(travel_angle)])
        ax.quiver(
            x0[0],
            x0[1],
            x0[2],
            dir_vector[0],
            dir_vector[1],
            0,
            color="green",
            label="Desired direction",
            length=10,
            arrow_length_ratio=0.1,
        )

        return (
            pos,
            w1,
            w2,
            w3,
        )

    def update(frame):
        plt.cla()
        init()
        time, x, u = frame

        com = x[0:3]  # Center of mass
        c = u[:]
        pos = ax.scatter(
            com[0], com[1], com[2], color="red", s=0.5
        )  # plot current position

        vel_rel = zhukovskii_glider.get_vel_rel(x[:])
        alpha = zhukovskii_glider.get_angle_of_attack(x[:], u[:])

        j_body = c / np.linalg.norm(c)  # j unit vector in body frame

        i_stability = vel_rel / np.linalg.norm(vel_rel)  # i unit vec in stability frame
        i_body = np.array(
            [
                [np.cos(alpha), 0, np.sin(alpha)],
                [0, 1, 0],
                [-np.sin(alpha), 0, np.cos(alpha)],
            ]
        ).dot(
            i_stability
        )  # Rotate i_stab by alpha around y axis to get i_body
        # TODO which way rotate by alpha here??
        k_body = np.cross(j_body, i_body)

        R_ned_to_body = np.stack((i_body, j_body, k_body), axis=1)
        curr_com_to_wing_vec = R_ned_to_body.dot(com_to_wing_vec)
        curr_com_to_front_vec = R_ned_to_body.dot(com_to_front_vec)

        # Draw glider
        # wing line
        w1 = ax.quiver(
            com[0] - curr_com_to_wing_vec[0],
            com[1] - curr_com_to_wing_vec[1],
            com[2] - curr_com_to_wing_vec[2],
            curr_com_to_wing_vec[0] * 2,
            curr_com_to_wing_vec[1] * 2,
            curr_com_to_wing_vec[2] * 2,
            linewidth=2,
            arrow_length_ratio=0.0,
            color="black",
        )
        # left wing to front
        w2 = ax.quiver(
            com[0] - curr_com_to_wing_vec[0],
            com[1] - curr_com_to_wing_vec[1],
            com[2] - curr_com_to_wing_vec[2],
            curr_com_to_wing_vec[0] + curr_com_to_front_vec[0],
            curr_com_to_wing_vec[1] + curr_com_to_front_vec[1],
            curr_com_to_wing_vec[2] + curr_com_to_front_vec[2],
            linewidth=2,
            arrow_length_ratio=0.0,
            color="black",
        )
        # left wing to front
        w3 = ax.quiver(
            com[0] + curr_com_to_wing_vec[0],
            com[1] + curr_com_to_wing_vec[1],
            com[2] + curr_com_to_wing_vec[2],
            -curr_com_to_wing_vec[0] + curr_com_to_front_vec[0],
            -curr_com_to_wing_vec[1] + curr_com_to_front_vec[1],
            -curr_com_to_wing_vec[2] + curr_com_to_front_vec[2],
            linewidth=2,
            arrow_length_ratio=0.0,
            color="black",
        )

        # Plot x axis
        ax.quiver(
            com[0],
            com[1],
            com[2],
            i_body[0],
            i_body[1],
            i_body[2],
            linewidth=2,
            color="red",
            length=scale * 3,
        )
        # Plot y axis
        ax.quiver(
            com[0],
            com[1],
            com[2],
            j_body[0],
            j_body[1],
            j_body[2],
            linewidth=2,
            color="yellow",
            length=scale * 3,
        )
        # Plot z axis
        ax.quiver(
            com[0],
            com[1],
            com[2],
            -k_body[0],
            -k_body[1],
            -k_body[2],
            linewidth=2,
            color="green",
            length=scale * 3,
        )

        return (
            pos,
            w1,
            w2,
            w3,
        )

    ani = FuncAnimation(
        fig, update, frames=list(zip(times, x_trj, u_trj)), init_func=init, blit=True
    )

    ## SAVE ANIMATION
    ani.save(filepath + filename, writer=writer)
    print("Saved animation as: {0}".format(filename))
    plt.close()

    return
