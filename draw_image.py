import math
import turtle
import cv2
import numpy as np


def map_value(x, a, b, c, d):
    """maps a value from one range to another
    """

    # Ensure the original range is not zero
    if a == b:
        raise ValueError("Original range cannot be zero")

    # Perform the mapping
    mapped_value = c + ((x - a) / (b - a)) * (d - c)

    return mapped_value


class ImageDrawer():
    def __init__(self, img_file_name: str, wave_height: int = 10, search_box_padding: int = 10) -> None:
        self.image = cv2.imread(img_file_name)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image_width = len(self.gray_image)
        self.image_height = len(self.gray_image[0])

        self.CANVAS_WIDTH = self.image_width
        self.CANVAS_HEIGHT = self.image_height

        self.screen = turtle.Screen()
        self.screen.setworldcoordinates(
            0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)

        self.plotter = turtle.Turtle()
        self.plotter.pencolor("black")
        self.plotter.speed(0)
        self.plotter.penup()

        self.h = wave_height  # height of the wave
        # the padding of the ROI used to calculate the average darkness
        self.sbp = search_box_padding

    def draw(self):
        sbp = self.sbp
        n = 0
        for y_roi in range(0, self.image_height, self.h):
            def draw_line(x):
                x_roi = round(x)
                # region of interest
                roi = self.gray_image[
                    y_roi-(sbp if y_roi > sbp else y_roi):y_roi+sbp if y_roi+sbp < self.image_height else self.image_height,
                    x_roi-(sbp if x_roi > sbp else x_roi):x_roi+sbp if x_roi+sbp < self.image_width else self.image_width
                ]
                average_brightness = np.mean(roi)
                average_darkness = 255 - average_brightness
                oscillation_intensity = map_value(
                    average_darkness, 0, 255, 0.1, 5)
                wave_height = map_value(
                    average_darkness, 0, 255, 0, self.h)
                sin_intake = x*oscillation_intensity
                return math.sin(sin_intake)*wave_height/2 + (self.h/2) * (1+(2*n))
            self.plotter.getscreen().tracer(0, 0)  # Disable automatic screen updates
            self._plot_function(draw_line)
            # Update the screen once after drawing is complete
            self.plotter.getscreen().update()
            n += 1

    def done(self):
        self.plotter.hideturtle()
        turtle.done()

    def save(self, filename: str):
        canvas = self.screen.getcanvas()
        canvas.postscript(file=filename)

    def _plot_function(self, func):
        # plotting 5 values in between the integers
        plot_n_values_in_between = 5

        # why 'y' is subtracted from canvas height is cuz. y=0 sits on top in opencv but y=0 sits in bottom in turtle (so we are basically reversing it)
        points = [(x/plot_n_values_in_between, self.CANVAS_HEIGHT - func(x/plot_n_values_in_between))
                  for x in range(self.CANVAS_WIDTH*plot_n_values_in_between)]
        self.plotter.penup()
        for point in points:
            x, y = point
            self.plotter.goto(x, y)
            self.plotter.pendown()
