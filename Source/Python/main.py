import pid
import pid_camera
import cv2
import serial_com as arduino_com
import math


def circle_position(theta, x_center=400, y_center=300, radius=100):
    return x_center+radius*math.cos(theta), y_center+radius*math.sin(theta)


def main():

    pid_x = pid.PID_Controller("pid_x.config")
    pid_y = pid.PID_Controller("pid_x.config")

    camera = pid_camera.PIDCamera()

    mode = 0

    x_center = 400
    y_center = 300

    square_refresh_period = 5

    square_side = 125
    square_period = 120
    circle_position_list = list()

    circle_divider = 18
    circle_period = 120
    circle_refresh_period = 5

    j = 0
    for i in range(0, 360, circle_divider):
        circle_position_list.append(circle_position(i))
        j += 1

    if mode == 0:
        while 1:

            camera.calculate_position((x_center, y_center))
            pid_x.compute_pid(x_center - camera.pos_x)
            pid_y.compute_pid(y_center - camera.pos_y)
            arduino_com.set_angles(pid_x.output, pid_y.output)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    elif mode == 1:
        corner = 0
        x_corner = x_center - square_side
        y_corner = y_center - square_side
        while 1:
            corner += 1
            if corner == square_period / square_refresh_period * 1:

                x_corner = x_center + square_side
                y_corner = y_center - square_side

            if corner == square_period / square_refresh_period * 2:
                x_corner = x_center + square_side
                y_corner = y_center + square_side

            if corner == square_period / square_refresh_period * 3:
                x_corner = x_center - square_side
                y_corner = y_center + square_side

            if corner == square_period / square_refresh_period * 4:
                x_corner = x_center - square_side
                y_corner = y_center - square_side
                corner = 0

            camera.calculate_position((x_corner, y_corner))

            pid_x.compute_pid(x_corner - camera.pos_x)
            pid_y.compute_pid(y_corner - camera.pos_y)

            arduino_com.set_angles(pid_x.output, pid_y.output)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            pass
    elif mode == 2:
        corner = 0
        k = 0
        while 1:
            corner += 1
            for i in range(0, circle_divider):
                if corner == circle_period / circle_refresh_period * i:
                    if k < circle_divider - 1:
                        k += 1
                    else:
                        k = 0
                    if i == circle_divider - 1:
                        corner = 0

            (x_corner, y_corner) = circle_position_list[j]
            camera.calculate_position((x_corner, y_corner))

            pid_x.compute_pid(x_corner - camera.pos_x)
            pid_y.compute_pid(y_corner - camera.pos_y)

            arduino_com.set_angles(pid_x.output, pid_y.output)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            pass

    camera.reset()
    arduino_com.close_connection()


if __name__ == "__main__":

    main()
