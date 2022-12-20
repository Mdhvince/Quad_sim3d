import random
from collections import namedtuple
import numpy as np


def get_path_random():
    Desired = namedtuple(
            "Desired", ["x", "y", "z", "x_vel", "y_vel", "z_vel", "x_acc", "y_acc", "z_acc", "yaw"])
    
    total_time = 20.0
    dt = 0.01
    t = np.linspace(0.0, total_time, int(total_time/dt))

    # Generate random values for omega_x, omega_y, omega_z, a_x, a_y, and a_z within the bounds of -1, 1
    omega_x = 2*random.random() - 1
    omega_y = 2*random.random() - 1
    omega_z = 2*random.random() - 1
    a_x = 2*random.random() - 1
    a_y = 2*random.random() - 1
    a_z = 2*random.random() - 1

    x = a_x * np.sin(omega_x * t) 
    x_vel = a_x * omega_x * np.cos(omega_x * t)
    x_acc = -a_x * omega_x**2 * np.sin(omega_x * t)

    y = a_y * np.cos(omega_y * t) + 2
    y_vel = -a_y * omega_y * np.sin(omega_y * t)
    y_acc = -a_y * omega_y**2 * np.cos(omega_y * t)

    z = np.abs(a_z * np.cos(omega_z * t)) + 2
    z_vel = -a_z * omega_z * np.sin(omega_z * t)
    z_acc = - a_z * omega_z**2 * np.cos(omega_z * t)

    # Compute the yaw angle as the angle between the velocity vector and the x-axis
    # here I ensure the yaw angle always stay in the direction of the trajectory
    yaw = np.arctan2(y_vel, x_vel)

    desired_trajectory = Desired(x, y, z, x_vel, y_vel, z_vel, x_acc, y_acc, z_acc, yaw)
    return t, dt, desired_trajectory


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

    y = a_y * np.cos(omega_y * t) + 2
    y_vel = -a_y * omega_y * np.sin(omega_y * t)
    y_acc = -a_y * omega_y**2 * np.cos(omega_y * t)

    z = a_z * np.cos(omega_z * t) + 2
    z_vel = -a_z * omega_z * np.sin(omega_z * t)
    z_acc = - a_z * omega_z**2 * np.cos(omega_z * t)

    yaw = np.arctan2(y_vel,x_vel)

    desired_trajectory = Desired(x, y, z, x_vel, y_vel, z_vel, x_acc, y_acc, z_acc, yaw)
    return t, dt, desired_trajectory


def get_path_straight():
    Desired = namedtuple(
            "Desired", ["x", "y", "z", "x_vel", "y_vel", "z_vel", "x_acc", "y_acc", "z_acc", "yaw"])
    
    total_time = 20.0
    dt = 0.01
    t = np.linspace(0.0, total_time, int(total_time/dt))

    x = np.zeros(t.shape)
    x_vel = np.zeros(t.shape)
    x_acc = np.zeros(t.shape)

    y = np.zeros(t.shape)
    y_vel = np.zeros(t.shape)
    y_acc = np.zeros(t.shape)

    z = np.ones(t.shape)
    z_vel = np.zeros(t.shape)
    z_acc = np.zeros(t.shape)

    yaw = np.zeros(t.shape)

    desired_trajectory = Desired(x, y, z, x_vel, y_vel, z_vel, x_acc, y_acc, z_acc, yaw)
    return t, dt, desired_trajectory


if __name__ == "__main__":
    pass