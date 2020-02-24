from tkinter import Tk, Button, Canvas

from routes import RoutePlan
from simple_traffic_learning import QAgent


class Renderer:
    def __init__(self):
        self.shape = 2
        self.dimensions = '900x900'
        self.drawable = 600
        self.step = self.drawable // self.shape

        self.is_clicked = None

        self.buttons = [[None, None, None], [None, None, None], [None, None, None]]

        self.connections = []

        self.window = Tk()
        self.window.geometry(self.dimensions)
        self.canvas = Canvas(self.window)

    def initialize_window(self):

        for row in range(self.shape):
            for col in range(self.shape):
                x = self.step * (col + 1)
                y = self.step * (row + 1)

                self.buttons[row][col] = Button(
                    self.window,
                    text="p{}".format(row * 10 + col),
                    command=lambda xr=row, yr=col: self.clicked(xr, yr)).place(x=x,
                                                                               y=y)

        # TODO: add button to finish the routing planning
        Button(self.window, text='Finish', command=self.start_algorithm).place(x=0,
                                                                               y=0)

        self.window.mainloop()

    def clicked(self, x_ind, y_ind):
        if self.is_clicked is None:
            self.is_clicked = (x_ind, y_ind)
        else:
            self.connections.append([self.is_clicked, (x_ind, y_ind)])

            # TODO: draw a line to the connections
            # current_pos = (self.step * (self.is_clicked[0] + 1),
            #                self.step * (self.is_clicked[1] + 1))
            # target_pos = (self.step * (x_ind + 1), self.step * (y_ind + 1))
            # self.canvas.create_line(*current_pos, *target_pos)
            # self.window.update()

            self.is_clicked = None

    def start_algorithm(self):
        gamma = 0.75
        alpha = 0.9

        rp = RoutePlan((self.shape, self.shape), self.connections, 4)
        rp.form_rewards()
        rp.add_light((0, 1), 1, 1)

        qagent = QAgent(gamma, alpha, rp)
        qagent.training((0, 0), (1, 1), 1000)


rd = Renderer()
rd.initialize_window()
