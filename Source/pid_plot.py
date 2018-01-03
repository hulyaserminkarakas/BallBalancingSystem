import time, random
from collections import deque
import matplotlib.pyplot as plt

start_time = time.time()


class PositionPlot(object):

    def __init__(self, max_entries=100):
        plt.ion()
        plt.rcParams["figure.figsize"] = [8, 6]
        x_axes = plt.subplot2grid(shape=(2, 2), loc=(0, 0), colspan=2)
        y_axes = plt.subplot2grid(shape=(2, 2), loc=(1, 0), colspan=2)
        x_axes.set_xlabel('Time(s)')
        x_axes.set_ylabel('X-Axis Position')
        y_axes.set_xlabel('Time(s)')
        y_axes.set_ylabel('Y-Axis Position')

        self.pos_x = deque(maxlen=max_entries)
        self.pos_y = deque(maxlen=max_entries)
        self.ref_pos_x = deque(maxlen=max_entries)
        self.ref_pos_y = deque(maxlen=max_entries)
        self.time = deque(maxlen=max_entries)

        self.x_axes = x_axes
        self.y_axes = y_axes

        self.lineplot_x_pos, = x_axes.plot([], [], label='X Current Pos')
        self.lineplot_x_ref, = x_axes.plot([], [], 'r', label='Set Point')
        self.x_axes.legend()
        self.x_axes.set_autoscaley_on(True)

        self.lineplot_y_pos, = y_axes.plot([], [], label='Y Current Pos')
        self.lineplot_y_ref, = y_axes.plot([], [], 'r', label='Set Point')
        self.y_axes.legend()
        self.y_axes.set_autoscaley_on(True)

    def add(self, pos_x, pos_y, ref_x, ref_y):
        cur_time = time.time() - start_time
        self.time.append(cur_time)

        self.ref_pos_x.append(ref_x)
        self.pos_x.append(pos_x)

        self.ref_pos_y.append(ref_y)
        self.pos_y.append(pos_y)

        self.lineplot_x_pos.set_data(self.time, self.pos_x)
        self.lineplot_x_ref.set_data(self.time, self.ref_pos_x)

        self.lineplot_y_pos.set_data(self.time, self.pos_y)
        self.lineplot_y_ref.set_data(self.time, self.ref_pos_y)

        self.x_axes.relim()
        self.x_axes.autoscale_view()

        self.y_axes.relim()
        self.y_axes.autoscale_view()
        # plt.pause(0.0000001)


    @staticmethod
    def example():
        plot = PositionPlot()
        while True:
            plot.add(random.random() * 800, random.random() * 600, 400, 300)
            plt.pause(0.001)



