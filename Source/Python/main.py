import pid
import pid_camera
import cv2
import serial_com as arduino_com


def main():

    pid_x = pid.PID_Controller("pid_x.config")
    pid_y = pid.PID_Controller("pid_y.config")

    camera = pid_camera.PIDCamera()

    mode = 0

    x_center = 400
    y_center = 300

    REFRESH_PERIOD = 2
    ESC_SC = 27

    SQUARE_SIDE = 140
    SQUARE_PERIOD = 250

    if mode == 0:

        while 1:

            camera.calculate_position()
            pid_x.compute_pid( x_center - camera.pos_x )
            pid_y.compute_pid( y_center - camera.pos_y )

            arduino_com.set_angles( pid_x.output, pid_y.output )

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    elif mode == 1:
        while 1:
            #camera.refresh()
            pass

    camera.reset()
    arduino_com.close_connection()

if __name__ == "__main__":
    main()