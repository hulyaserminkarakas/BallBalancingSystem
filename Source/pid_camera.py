from collections import deque
import numpy as np
import imutils
import cv2


class PIDCamera:
    def __init__(self):
        self.pos_x = 0

        self.pos_y = 0

        self.colorLower = (20, 70, 10)
        self.colorUpper = (200, 250, 200)

        self.buffer_pts = deque([])
        self.camera = cv2.VideoCapture(0)

        self.counter = 0
        self.coords = ""

    def calculate_position(self):

        (grabbed, frame) = self.camera.read()

        if not grabbed:
            exit(-1)

        frame = imutils.resize(frame, width=800)


        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (255, 0, 0), -1)
                self.buffer_pts.appendleft(center)

        for i in np.arange(1, len(self.buffer_pts)):
            if self.buffer_pts[i - 1] is None or self.buffer_pts[i] is None:
                continue

            if self.counter >= 10 and i == 1:
                self.pos_x = self.buffer_pts[i][0]
                self.pos_y = self.buffer_pts[i][1]
                (dir_x, dir_y) = ("", "")

                if dir_x != "" and dir_y != "":
                    self.coords = "{}-{}".format(self.pos_x, self.pos_y)

                else:
                    self.coords = dir_x if dir_x != "" else dir_y

        #    thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        # cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        cv2.putText(frame,  self.coords, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dx: {}, dy: {}".format(self.pos_x, self.pos_y),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)

        cv2.imshow("Frame", frame)
        self.counter += 1

    def reset(self):
        self.camera.release()
        cv2.destroyAllWindows()





