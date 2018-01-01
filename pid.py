import re


class PID_Controller(object):

    def __init__(self, file_path=None):
        if file_path is not None:
            self.read_file(file_path)
            self.integral_sum = .0
            self.l_input = .0
            return

        self.P = .0
        self.I = .0
        self.D = .0

        self.l_input = .0
        self.integral_sum = .0

        self.output = .0
        self.period = .0

        self.min_out = .0
        self.max_out = .0

    def read_file(self, file_path):
        with open(file_path) as file:

            lines = file.readlines()

            self.P = float(re.split('\s+', lines[0])[1])
            self.I = float(re.split('\s+', lines[1])[1])
            self.D = float(re.split('\s+', lines[2])[1])
            self.period = float(re.split('\s+', lines[3])[1])
            self.max_out = float(re.split('\s+', lines[4])[1])
            self.min_out = float(re.split('\s+', lines[5])[1])

    def compute_pid(self, error):
        #proportional = self.P * error
        #derivative = self.D * (error - self.l_input) / self.period
        #integral = self.integral_sum + self.I * error * self.period
        derivative = (error - self.l_input)/self.period
        integral = self.integral_sum + (error * self.period)

        if integral > 20:
            integral = 20
        elif integral < -20:
            integral = -20

        self.integral_sum = integral
        self.l_input = error

        #result = proportional + integral + derivative
        result = self.P * error + self.I * integral + self.D * derivative
        self.output = result

        if result > self.max_out:
            self.output = self.max_out
        if result < self.min_out:
            self.output = self.min_out


