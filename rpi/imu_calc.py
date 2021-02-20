import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import scipy as sp
from scipy import constants     # for "g"
from scipy.integrate import cumtrapz
import re

import asyncio

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

# Analytically calculate position from initial conditions, orientation, and acceleration values
def calc_position(q, accel, initialVelocity, initialPosition, timeVector):
    g_v = np.r_[0, 0, constants.g] 
    accReSensor = accel - vector.rotate_vector(g_v, quat.q_inv(q))
    accReSpace = vector.rotate_vector(accReSensor, q)

    # Position and Velocity through integration, assuming 0-velocity at t=0
    vel = np.nan*np.ones_like(accReSpace)
    pos = np.nan*np.ones_like(accReSpace)

    for ii in range(accReSpace.shape[1]):
        vel[:,ii] = cumtrapz(accReSpace[:,ii], x=timeVector, initial=initialVelocity[ii])
        pos[:,ii] = cumtrapz(vel[:,ii], x=timeVector, initial=initialPosition[ii])
    
    avevel = np.mean(vel, axis=0)
    aveaccel = np.mean(accel, axis=0)
    
    print("Average Accel: {}, Average Velocity: {}, Time taken: {}".format(np.sqrt(aveaccel[0]**2 + aveaccel[1]**2 + aveaccel[2]**2), np.sqrt(avevel[0]**2 + avevel[1]**2 + avevel[2]**2), timeVector[-1] * 1000))

    return pos, vel

# Kalman filter data for getting orientation based off of magnetic strength, its taken from the scipy-kinematics library
# Taken from a paper of some sort
# I've modified it to also give position based off of the analytical function above
def kalman(rate, acc, omega, mag,
           D = [0.4, 0.4, 0.4],          
           tau = [0.5, 0.5, 0.5],
           Q_k = None,
           R_k = None,
           initialPosition=np.zeros(3),
           initialVelocity=np.zeros(3),
           initialOrientation=np.zeros(3),
           timeVector=np.zeros((5,1)),
           accMeasured=np.column_stack((np.zeros((5,2)), 9.81*np.ones(5))),
           referenceOrientation=np.array([1., 0., 0., 0.])):
    '''
    Calclulate the orientation from IMU magnetometer data.
    Parameters
    ----------
    rate : float
    	   sample rate [Hz]	
    acc : (N,3) ndarray
    	  linear acceleration [m/sec^2]
    omega : (N,3) ndarray
    	  angular velocity [rad/sec]
    mag : (N,3) ndarray
    	  magnetic field orientation
    D : (,3) ndarray
          noise variance, for x/y/z [rad^2/sec^2]
          parameter for tuning the filter; defaults from Yun et al.
          can also be entered as list
    tau : (,3) ndarray
          time constant for the process model, for x/y/z [sec]
          parameter for tuning the filter; defaults from Yun et al.
          can also be entered as list
    Q_k : None, or (7,7) ndarray
          covariance matrix of process noises
          parameter for tuning the filter
          If set to "None", the defaults from Yun et al. are taken!
    R_k : None, or (7,7) ndarray
          covariance matrix of measurement noises
          parameter for tuning the filter; defaults from Yun et al.
          If set to "None", the defaults from Yun et al. are taken!
          
    Returns
    -------
    qOut : (N,4) ndarray
    	   unit quaternion, describing the orientation relativ to the coordinate
           system spanned by the local magnetic field, and gravity
    pos  : (N,3) ndarray
            Position array
    vel  : (N,3) ndarray
            Velocity
    Notes
    -----
    Based on "Design, Implementation, and Experimental Results of a Quaternion-
       Based Kalman Filter for Human Body Motion Tracking" Yun, X. and Bachman,
       E.R., IEEE TRANSACTIONS ON ROBOTICS, VOL. 22, 1216-1227 (2006)
    '''

    numData = len(acc)

    # Set parameters for Kalman Filter
    tstep = 1./rate
    
    # check input
    assert len(tau) == 3
    tau = np.array(tau)

    # Initializations 
    x_k = np.zeros(7)	# state vector
    z_k = np.zeros(7)   # measurement vector
    z_k_pre = np.zeros(7)
    P_k = np.eye(7)		 # error covariance matrix P_k

    Phi_k = np.eye(7)    # discrete state transition matrix Phi_k
    for ii in range(3):
        Phi_k[ii,ii] = np.exp(-tstep/tau[ii])

    H_k = np.eye(7)		# Identity matrix

    D = np.r_[0.4, 0.4, 0.4]		# [rad^2/sec^2]; from Yun, 2006
    
    if Q_k is None:
        # Set the default input, from Yun et al.
        Q_k = np.zeros((7,7)) 	# process noise matrix Q_k
        for ii in range(3):
            Q_k[ii,ii] =  D[ii]/(2*tau[ii])  * ( 1-np.exp(-2*tstep/tau[ii]) )
    else:
        # Check the shape of the input
        assert Q_k.shape == (7,7)

    # Evaluate measurement noise covariance matrix R_k
    if R_k is None:
        # Set the default input, from Yun et al.
        r_angvel = 0.01;      # [rad**2/sec**2]; from Yun, 2006
        r_quats = 0.0001;     # from Yun, 2006
        
        r_ii = np.zeros(7)
        for ii in range(3):
            r_ii[ii] = r_angvel
        for ii in range(4):
            r_ii[ii+3] = r_quats
            
        R_k = np.diag(r_ii)    
    else:
        # Check the shape of the input
        assert R_k.shape == (7,7)

    # Calculation of orientation for every time step
    qOut = np.zeros( (numData,4) )

    for ii in range(numData):
        accelVec  = acc[ii,:]
        magVec    = mag[ii,:]
        angvelVec = omega[ii,:]
        z_k_pre = z_k.copy()  # watch out: by default, Python passes the reference!!

        # Evaluate quaternion based on acceleration and magnetic field data 
        accelVec_n = vector.normalize(accelVec)
        magVec_hor = magVec - accelVec_n * (accelVec_n @ magVec)
        magVec_n   = vector.normalize(magVec_hor)
        basisVectors = np.column_stack( [magVec_n,
                                np.cross(accelVec_n, magVec_n), accelVec_n] )
        quatRef = quat.q_inv(rotmat.convert(basisVectors, to='quat')).ravel()

        # Calculate Kalman Gain
        # K_k = P_k * H_k.T * inv(H_k*P_k*H_k.T + R_k)
        K_k = P_k @ np.linalg.inv(P_k + R_k)

        # Update measurement vector z_k
        z_k[:3] = angvelVec
        z_k[3:] = quatRef

        # Update state vector x_k
        x_k += np.array( K_k@(z_k-z_k_pre) ).ravel()

        # Evaluate discrete state transition matrix Phi_k
        Delta = np.zeros((7,7))
        Delta[3,:] = np.r_[-x_k[4], -x_k[5], -x_k[6],      0, -x_k[0], -x_k[1], -x_k[2]]
        Delta[4,:] = np.r_[ x_k[3], -x_k[6],  x_k[5], x_k[0],       0,  x_k[2], -x_k[1]]
        Delta[5,:] = np.r_[ x_k[6],  x_k[3], -x_k[4], x_k[1], -x_k[2],       0,  x_k[0]]
        Delta[6,:] = np.r_[-x_k[5],  x_k[4],  x_k[3], x_k[2],  x_k[1], -x_k[0],       0]
        
        Delta *= tstep/2
        Phi_k += Delta

        # Update error covariance matrix
        P_k = (np.eye(7) - K_k) @ P_k

        # Projection of state
        # 1) quaternions
        x_k[3:] += tstep * 0.5 * quat.q_mult(x_k[3:], np.r_[0, x_k[:3]]).ravel()
        x_k[3:] = vector.normalize( x_k[3:] )
        # 2) angular velocities
        x_k[:3] -= tstep * tau * x_k[:3]

        qOut[ii,:] = x_k[3:]

        # Projection of error covariance matrix
        P_k = Phi_k @ P_k @ Phi_k.T + Q_k

    # Calculate Position from Orientation
    # pos, vel = calc_position(qOut, acc, initialVelocity, initialPosition, timeVector)

    # Make the first position the reference position
    qOut = quat.q_mult(qOut, quat.q_inv(referenceOrientation))

    return qOut