import time

from rems.robots import RobotBase, RobotThread
import numpy as np


class WoodbotModel(RobotThread):
    '''

    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run.DT = 0.1      # Robot run frequency
        self.run.name = 'Model' # robot name

    def drive(self, inpt, timestamp):
        '''
        This is where we drive the robot.
        Robot drive function. Called at every time step.
        Receive inout and timestamp and then "drive" the robot

        :param inpt: Dictionary like object
        :param timestamp: float world timestamp
        :return: None
        '''
        # saving the current input
        self.inpt.update(inpt)

        # get input, note they are in percent -100 to 100%
        inpt_np = self.inpt.ndarray()      # input values in numpy array
        inpt_nptall = self.inpt.ndtall()    # in numpy tall array
        wh_l = self.inpt.get('wh.l')    # or get specific
        wh_r = self.inpt.get('wh.r')

        x = self.state.get('x')
        y = self.state.get('y')
        th = self.state.get('th_z')

        state_np = self.state.ndarray()    # current state in numpy array
        state_nptall = self.state.ndtall()# numpay tall array

        dt = self.run.DT        # delta T, 0.1sec

        # getting dimensions, IDE may complain, but all variables in WoodbotDef are accessible
        W = self.dimension.get('W')
        d = self.dimension.get('d')
        R_env = self.dimension.get('R_env')
        max_vel = self.dimension.get('max_vel')

        th = self.state.get('th_z')
        r = d/2
        jacobian = np.array([r * np.cos(th) / 2, r * np.cos(th) / 2,
                             r * np.sin(th) / 2, r * np.sin(th) / 2,
                             -r / W, r / W]).reshape(3,2)

        inpt = max_vel * inpt.ndtall() / 100
        n_state = self.state.ndtall() + jacobian @ inpt * self.run.DT

        # save next state
        # this will set the data based on positions
        self.state.update(n_state.flatten())




    def sense(self):
        '''
        Sensor implementation
        Called at every timestep
        :return: output values (iterative)
        '''

        inpt = self.inpt.ndarray()  # input values in numpy array
        state = self.state.ndarray()  # current state in numpy array

        # getting dimensions
        W = self.dimension.get('W')
        d = self.dimension.get('d')
        R_env = self.dimension.get('R_env')
        max_vel = self.dimension.get('max_vel')

        # TODO: Implement your sensor model
        ###############################
        # Your model equation here    #
        # output = h(state, inpt)     #
        ###############################

        output = np.array([0, 0, 0, 0, 0])
        self.outpt.update(output)
        return self.outpt

    def observe_state(self):
        '''
        This will return state of the robot at a time step
        :return: state (iterative)
        '''

        # here you have nothing to do because our 'drive' indeed updates the state
        return self.state



