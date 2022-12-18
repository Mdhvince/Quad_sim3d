import configparser
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

from quadrotor import Quadrotor
from controller import Controller

# We want to control the drone in the world frame BUT we get some sensore measurement from the IMU that are in the body frame.
# And our controls (especially the moments that we command) have a more intuitive interpretation in the body frame.

G = 9.81


def get_path():
    Desired = namedtuple(
            "Desired", ["x", "y", "z", "x_vel", "y_vel", "z_vel", "x_acc", "y_acc", "z_acc", "yaw"])
    
    total_time = 20.0
    dt = 0.01
    t = np.linspace(0.0, total_time, int(total_time/dt))

    omega_x = 0.8
    omega_y = 0.4
    omega_z = 0.4

    a_x = 1.0 
    a_y = 1.0
    a_z = 1.0

    x = a_x * np.sin(omega_x * t) 
    x_vel = a_x * omega_x * np.cos(omega_x * t)
    x_acc = -a_x * omega_x**2 * np.sin(omega_x * t)

    y = a_y * np.cos(omega_y * t)
    y_vel = -a_y * omega_y * np.sin(omega_y * t)
    y_acc = -a_y * omega_y**2 * np.cos(omega_y * t)

    z = a_z * np.cos(omega_z * t)
    z_vel = -a_z * omega_z * np.sin(omega_z * t)
    z_acc = - a_z * omega_z**2 * np.cos(omega_z * t)

    yaw = np.arctan2(y_vel,x_vel)

    desired_trajectory = Desired(x, y, z, x_vel, y_vel, z_vel, x_acc, y_acc, z_acc, yaw)
    return t, dt, desired_trajectory


def animate_trajectory(quad, R, desired_traj):
    origin = np.array([quad.x, quad.y, quad.z])
    x_axis = np.array([1, 0, 0])
    y_axis = np.array([0, 1, 0])
    z_axis = np.array([0, 0, 1])

    # Transform the body-fixed axes into the world frame using the rotation matrix
    x_axis_world = np.dot(R, x_axis)
    y_axis_world = np.dot(R, y_axis)
    z_axis_world = np.dot(R, z_axis)

    # Plot the x, y, and z axes in the world frame
    ax.clear()
    ax.plot3D([origin[0], x_axis_world[0]], [origin[1], x_axis_world[1]], [origin[2], x_axis_world[2]], 'r')
    ax.plot3D([origin[0], y_axis_world[0]], [origin[1], y_axis_world[1]], [origin[2], y_axis_world[2]], 'g')
    ax.plot3D([origin[0], z_axis_world[0]], [origin[1], z_axis_world[1]], [origin[2], z_axis_world[2]], 'b')
    ax.plot(desired_traj.x, desired_traj.y, desired_traj.z, linestyle='-', marker='.',color='red')

    ax.set_xlabel('$x$ [$m$]').set_fontsize(12)
    ax.set_ylabel('$y$ [$m$]').set_fontsize(12)
    ax.set_zlabel('$z$ [$m$]').set_fontsize(12)
    plt.legend(['Planned path'],fontsize=10)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    plt.pause(.001)


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config_file = "config.ini"
    config.read(config_file)
    
    inner_loop_relative_to_outer_loop = 10
    t, dt, desired = get_path()

    quad = Quadrotor(config)
    control_system = Controller(config)
    
    
    # declaring the initial state
    quad.X = np.array([
        desired.x[0], desired.y[0], desired.z[0],
        0.0, 0.0, desired.yaw[0],
        desired.x_vel[0], desired.y_vel[0], desired.z_vel[0],
        0.0, 0.0, 0.0
    ])
    
    # arrays for recording the state history, 
    drone_state_history = quad.X
    omega_history = quad.omega
    accelerations = quad.linear_acceleration()
    accelerations_history= accelerations
    angular_vel_history = quad.get_euler_derivatives()


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    n_waypoints = desired.z.shape[0]

    for i in range(0, n_waypoints):
        rot_mat = quad.R()
        c = control_system.altitude_controller(
                desired.z[i], desired.z_vel[i], desired.z_acc[i], rot_mat, quad)

        bxy_cmd = control_system.lateral_controller(
                desired.x[i], desired.x_vel[i], desired.x_acc[i],
                desired.y[i], desired.y_vel[i], desired.y_acc[i], c, quad)
        
        for _ in range(inner_loop_relative_to_outer_loop):
            rot_mat = quad.R()
            ubar_pqr = control_system.attitude_controller(bxy_cmd, desired.yaw[i], rot_mat, quad)
            quad.set_propeller_angular_velocities(c, ubar_pqr)
            quad_state = quad.advance_state(dt/inner_loop_relative_to_outer_loop)

        animate_trajectory(quad, rot_mat, desired)

        # generating a history
        # drone_state_history = np.vstack((drone_state_history, quad_state))
        # omega_history = np.vstack((omega_history, quad.omega))
        # accelerations = quad.linear_acceleration()
        # accelerations_history= np.vstack((accelerations_history, accelerations))
        # angular_vel_history = np.vstack((angular_vel_history, quad.get_euler_derivatives()))


    # ax.plot(desired.x, desired.y, desired.z,linestyle='-',marker='.',color='red')
    # ax.plot(drone_state_history[:,0],
    #         drone_state_history[:,1],
    #         drone_state_history[:,2],
    #         linestyle='-',color='blue')

    # plt.title('Flight path').set_fontsize(20)
    # ax.set_xlabel('$x$ [$m$]').set_fontsize(20)
    # ax.set_ylabel('$y$ [$m$]').set_fontsize(20)
    # ax.set_zlabel('$z$ [$m$]').set_fontsize(20)
    # plt.legend(['Planned path','Executed path'],fontsize = 14)

    # ax.set_xlim(-2, 2)
    # ax.set_ylim(-2, 2)
    # ax.set_zlim(-2, 2)

    # plt.show()


    # plt.plot(t,desired.yaw,marker='.')
    # plt.plot(t,drone_state_history[:-1,5])
    # plt.title('Yaw angle').set_fontsize(20)
    # plt.xlabel('$t$ [$s$]').set_fontsize(20)
    # plt.ylabel('$\psi$ [$rad$]').set_fontsize(20)
    # plt.legend(['Planned yaw','Executed yaw'],fontsize = 14)
    # plt.show()



    




