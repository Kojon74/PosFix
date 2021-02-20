import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import scipy as sp
from scipy import constants     # for "g"
from scipy.integrate import cumtrapz
import re

# The following construct is required since I want to run the module as a script
# inside the skinematics-directory
import os
import sys

from skinematics import quat, vector, misc, rotmat

# For deprecation warnings
# import deprecation
import warnings

# For the definition of the abstract base class IMU_Base
import abc

def analytical(R_initialOrientation=np.eye(3),
               omega=np.zeros((5,3)),
               initialPosition=np.zeros(3),
               initialVelocity=np.zeros(3),
               accMeasured=np.column_stack((np.zeros((5,2)), 9.81*np.ones(5))),
               rate=100):
    ''' Reconstruct position and orientation with an analytical solution,
    from angular velocity and linear acceleration.
    Assumes a start in a stationary position. No compensation for drift.

    Parameters
    ----------
    R_initialOrientation: ndarray(3,3)
        Rotation matrix describing the initial orientation of the sensor,
        except a mis-orienation with respect to gravity
    omega : ndarray(N,3)
        Angular velocity, in [rad/s]
    initialPosition : ndarray(3,)
        initial Position, in [m]
    accMeasured : ndarray(N,3)
        Linear acceleration, in [m/s^2]
    rate : float
        sampling rate, in [Hz]

    Returns
    -------
    q : ndarray(N,3)
        Orientation, expressed as a quaternion vector
    pos : ndarray(N,3)
        Position in space [m]
    vel : ndarray(N,3)
        Velocity in space [m/s]

    Example
    -------
     
    >>> q1, pos1 = analytical(R_initialOrientation, omega, initialPosition, acc, rate)

    '''

    if omega.ndim == 1:
        raise ValueError('The input to "analytical" requires matrix inputs.')
        
    # Transform recordings to angVel/acceleration in space --------------

    # Orientation of \vec{g} with the sensor in the "R_initialOrientation"
    g = constants.g
    g0 = np.linalg.inv(R_initialOrientation).dot(np.r_[0,0,g])

    # for the remaining deviation, assume the shortest rotation to there
    q0 = vector.q_shortest_rotation(accMeasured[0], g0)    
    
    q_initial = rotmat.convert(R_initialOrientation, to='quat')
    
    # combine the two, to form a reference orientation. Note that the sequence
    # is very important!
    q_ref = quat.q_mult(q_initial, q0)
    
    # Calculate orientation q by "integrating" omega -----------------
    q = quat.calc_quat(omega, q_ref, rate, 'bf')

    # Acceleration, velocity, and position ----------------------------
    # From q and the measured acceleration, get the \frac{d^2x}{dt^2}
    g_v = np.r_[0, 0, g] 
    accReSensor = accMeasured - vector.rotate_vector(g_v, quat.q_inv(q))
    accReSpace = vector.rotate_vector(accReSensor, q)

    # Make the first position the reference position
    q = quat.q_mult(q, quat.q_inv(q[0]))

    # compensate for drift
    #drift = np.mean(accReSpace, 0)
    #accReSpace -= drift*0.7

    # Position and Velocity through integration, assuming 0-velocity at t=0
    vel = np.nan*np.ones_like(accReSpace)
    pos = np.nan*np.ones_like(accReSpace)

    for ii in range(accReSpace.shape[1]):
        vel[:,ii] = cumtrapz(accReSpace[:,ii], dx=1./rate, initial=initialVelocity[ii])
        pos[:,ii] = cumtrapz(vel[:,ii], dx=1./rate, initial=initialPosition[ii])

    return (q, pos, vel)

# Copied and modified frmo the scipy-kinematics library
def calc_quat(omega, q0, rate, CStype):
    '''
    Take an angular velocity (in rad/s), and convert it into the
    corresponding orientation quaternion.
    Parameters
    ----------
    omega : array, shape (3,) or (N,3)
        angular velocity [rad/s].
    q0 : array (3,)
        vector-part of quaternion (!!)
    rate : float
        sampling rate (in [Hz])
    CStype:  string
        coordinate_system, space-fixed ("sf") or body_fixed ("bf")
    Returns
    -------
    quats : array, shape (N,4)
        unit quaternion vectors.
    Notes
    -----
    1) The output has the same length as the input. As a consequence, the last velocity vector is ignored.
    2) For angular velocity with respect to space ("sf"), the orientation is given by
      .. math::
          q(t) = \\Delta q(t_n) \\circ \\Delta q(t_{n-1}) \\circ ... \\circ \\Delta q(t_2) \\circ \\Delta q(t_1) \\circ q(t_0)
      .. math::
        \\Delta \\vec{q_i} = \\vec{n(t)}\\sin (\\frac{\\Delta \\phi (t_i)}{2}) = \\frac{\\vec \\omega (t_i)}{\\left| {\\vec \\omega (t_i)} \\right|}\\sin \\left( \\frac{\\left| {\\vec \\omega ({t_i})} \\right|\\Delta t}{2} \\right)
    3) For angular velocity with respect to the body ("bf"), the sequence of quaternions is inverted.
    4) Take care that you choose a high enough sampling rate!
    Examples
    --------
    >>> v0 = np.r_[0., 0., 100.] * np.pi/180.
    >>> omega = np.tile(v0, (1000,1))
    >>> rate = 100
    >>> out = quat.calc_quat(omega, [0., 0., 0.], rate, 'sf')
    array([[ 1.        ,  0.        ,  0.        ,  0.        ],
       [ 0.99996192,  0.        ,  0.        ,  0.00872654],
       [ 0.9998477 ,  0.        ,  0.        ,  0.01745241],
       ..., 
       [-0.74895572,  0.        ,  0.        ,  0.66262005],
       [-0.75470958,  0.        ,  0.        ,  0.65605903],
       [-0.76040597,  0.        ,  0.        ,  0.64944805]])
    '''
    
    omega_05 = np.atleast_2d(omega).copy()
    
    # The following is (approximately) the quaternion-equivalent of the trapezoidal integration (cumtrapz)
    if omega_05.shape[1]>1:
        omega_05[:-1] = 0.5*(omega_05[:-1] + omega_05[1:])

    omega_t = np.sqrt(np.sum(omega_05**2, 1))
    omega_nonZero = omega_t>0

    # initialize the quaternion
    q_delta = np.zeros(omega_05.shape)
    q_pos = np.zeros((len(omega_05),4))
    q_pos[0,:] = q0

    # magnitude of position steps
    dq_total = np.sin(omega_t[omega_nonZero]/(2.*rate))

    q_delta[omega_nonZero,:] = omega_05[omega_nonZero,:] * np.tile(dq_total/omega_t[omega_nonZero], (3,1)).T

    for ii in range(len(omega_05)-1):
        q1 = q_delta[ii,:]
        q2 = q_pos[ii,:]
        if CStype == 'sf':            
            qm = quat.q_mult(q1,q2)
        elif CStype == 'bf':
            qm = quat.q_mult(q2,q1)
        else:
            print('I don''t know this type of coordinate system!')
        q_pos[ii+1,:] = qm

    # print(q_pos)

    return q_pos

# Similar to above analytical solver but with changes for real time use, and varying dx for the integration steps
# This is modified from the scipy-kinematics library function
def calc_orientation_position(initialOrientation=np.eye(3),
                                omega=np.zeros((5,3)),
                                initialPosition=np.zeros(3),
                                initialVelocity=np.zeros(3),
                                timeVector=np.zeros((5,1)),
                                accMeasured=np.column_stack((np.zeros((5,2)), 9.81*np.ones(5))),
                                rate=100,
                                referenceOrientation=np.array([1., 0., 0., 0.])):
    ''' Reconstruct position and orientation with an analytical solution,
    from angular velocity and linear acceleration.
    Assumes a start in a stationary position. No compensation for drift.

    Parameters
    ----------
    R_initialOrientation: ndarray(3,3)
        Rotation matrix describing the initial orientation of the sensor,
        except a mis-orienation with respect to gravity
    omega : ndarray(N,3)
        Angular velocity, in [rad/s]
    initialPosition : ndarray(3,)
        initial Position, in [m]
    accMeasured : ndarray(N,3)
        Linear acceleration, in [m/s^2]
    rate : float
        sampling rate, in [Hz]

    Returns
    -------
    q : ndarray(N,3)
        Orientation, expressed as a quaternion vector
    pos : ndarray(N,3)
        Position in space [m]
    vel : ndarray(N,3)
        Velocity in space [m/s]
    '''

    if omega.ndim == 1:
        raise ValueError('The input to "analytical" requires matrix inputs.')
        
    # Transform recordings to angVel/acceleration in space --------------

    # Orientation of \vec{g} with the sensor in the "R_initialOrientation"
    g = constants.g
    g0 = np.linalg.inv(initialOrientation).dot(np.r_[0,0,g])

    # for the remaining deviation, assume the shortest rotation to there
    q0 = vector.q_shortest_rotation(accMeasured[0], g0)    
    
    q_initial = rotmat.convert(initialOrientation, to='quat')

    # print("*** INITIAL ORIENTATION")
    # print(q_initial)

    # print("*** Q0")
    # print(q0)
    
    # combine the two, to form a reference orientation. Note that the sequence
    # is very important!
    q_ref = quat.q_mult(q_initial, q0)
    
    # print("*** QREF")
    # print(q_ref)
    
    # Calculate orientation q by "integrating" omega -----------------
    q = calc_quat(omega, q_ref, rate, 'bf')

    # Acceleration, velocity, and position ----------------------------
    # From q and the measured acceleration, get the \frac{d^2x}{dt^2}
    g_v = np.r_[0, 0, g] 
    accReSensor = accMeasured - vector.rotate_vector(g_v, quat.q_inv(q))
    accReSpace = vector.rotate_vector(accReSensor, q)

    # print("Initial Position")
    # print(initialPosition)

    # print("Initial Velocity")
    # print(initialVelocity)

    # print("Time")
    # print(accReSpace)

    # Make the first position the reference position
    q = quat.q_mult(q, quat.q_inv(referenceOrientation))

    # print(q)

    # compensate for drift
    #drift = np.mean(accReSpace, 0)
    #accReSpace -= drift*0.7

    # Position and Velocity through integration, assuming 0-velocity at t=0
    vel = np.nan*np.ones_like(accReSpace)
    pos = np.nan*np.ones_like(accReSpace)

    for ii in range(accReSpace.shape[1]):
        vel[:,ii] = cumtrapz(accReSpace[:,ii], x=timeVector, initial=initialVelocity[ii])
        pos[:,ii] = cumtrapz(vel[:,ii], x=timeVector, initial=initialPosition[ii])

    return (q, pos, vel)
    
