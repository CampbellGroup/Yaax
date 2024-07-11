#!/usr/bin/env python3

import numpy as np
import scipy.ndimage
import pyqtgraph
from PyQt5.QtCore import Qt

import artiq.applets.simple

from widget import PlotWidget


class XYPlot(PlotWidget):
    """Extended and backwards compatible version of the standard ARTIQ plot XY applet."""

    def __init__(self, args, **kwargs):
        # Call super
        super().__init__(args, **kwargs)

        # Set attributes
        self.x = None
        self.y = None
        self.ch_hline = None
        self.ch_vline = None
        self.crosshair = args.crosshair

        # Set labels
        self.plotItem.setLabel('bottom', args.x_label)
        self.plotItem.setLabel('left', args.y_label)

        # Configure crosshair
        self.setMouseTracking(self.crosshair)

    def update_applet(self, args):
        # Obtain input data
        y = np.asarray(self.get_dataset(args.y))
        x = np.asarray(self.get_dataset(args.x, np.arange(len(y))))
        error = self.get_dataset(args.error, None)  # Can be a single value or a sequence
        fit = self.get_dataset(args.fit, None)
        fit_x = self.get_dataset(args.fit_x, None)
        h_lines = self.get_dataset(args.h_lines, [])
        v_lines = self.get_dataset(args.v_lines, [])

        # Verify input data
        if not len(y) or len(y) > len(x):
            return
        if len(x) > len(y):
            # Trim x data
            x = x[:len(y)]

        if error is not None:
            if not len(error):
                error = None
            else:
                error = np.asarray(error)
                if error.shape != y.shape:
                    self.logger.warning('Error data does not match shape of Y data')
                    error = None
        if fit is not None:
            if not len(fit):
                fit = None
            else:
                fit = np.asarray(fit)
                if fit_x is None:
                    if fit.shape != y.shape:
                        self.logger.warning('Fit data does not match shape of Y data')
                        fit = None
                    else:
                        fit_x = x
                else:
                    fit_x = np.asarray(fit_x)
                    if len(fit) > len(fit_x):
                        self.logger.warning('Fit data does not match shape of fit X data')
                        fit = None
                        fit_x = None
                    elif len(fit_x) > len(fit):
                        # trim fit x data
                        fit_x = fit_x[:len(fit)]

        # Handle sliding window
        if args.sliding_window > 0:
            # Get window size
            window_size = args.sliding_window

            # Truncate input data based on the window size
            v_lines = [v for v in v_lines if len(y) - window_size <= v < len(y)]
            y = y[-window_size:]
            x = x[-window_size:]
            if error is not None:
                error = error[-window_size:]
            if fit is not None:
                win = (fit_x >= np.min(x)) & (fit_x <= np.max(x))
                fit = fit[win]
                fit_x = fit_x[win]

        if args.last:
            # Extend title with value of the latest data point
            self.extend_title('({:.2f})'.format(y[-1] if args.multiplier is None else y[-1] * args.multiplier))

        if args.subsample > 1:
            # Get subsampling factor
            factor = args.subsample

            # Subsample data
            y = y[::factor]
            x = x[::factor]
            if error is not None:
                error = error[::factor]
            if fit is not None:
                fit = fit[::factor]
                fit_x = fit_x[::factor]

        if args.multiplier is not None:
            # Apply multiplier on data
            y *= args.multiplier

        # Clear plot
        self.plotItem.clear()

        # Plot horizontal and vertical lines
        for h in h_lines:
            self.plotItem.addLine(y=h)
        for v in v_lines:
            self.plotItem.addLine(x=v)

        if error is not None:
            # Plot error bars (note: https://github.com/pyqtgraph/pyqtgraph/issues/211)
            self.plotItem.addItem(pyqtgraph.ErrorBarItem(x=x, y=y, height=error))
        if fit is not None:
            # Sort based on x data
            idx = fit_x.argsort()
            # Plot fit
            self.plotItem.plot(x=fit_x[idx], y=fit[idx])

        # Plot points
        pen = pyqtgraph.mkPen(color= 'cyan' ,width=2)
        self.plotItem.plot(x=x, y=y, pen=pen)

        # Handle moving average
        if args.moving_average > 0:
            # Sort based on x data
            idx = x.argsort()
            # Calculate moving average
            avg = scipy.ndimage.uniform_filter1d(y[idx], args.moving_average, mode='nearest')
            # Plot moving average
            self.plotItem.plot(x=x[idx], y=avg, pen=pyqtgraph.mkPen(width=2, style=Qt.DotLine))

        if self.crosshair:
            # Make data available to mouseMoveEvent
            self.x = x
            self.y = y

    # noinspection PyPep8Naming
    def mouseMoveEvent(self, ev):
        # Call super
        super(XYPlot, self).mouseMoveEvent(ev)

        if self.crosshair and self.x is not None and self.y is not None:
            try:
                pos = self.plotItem.getViewBox().mapSceneToView(ev.pos())
            except np.linalg.LinAlgError:  # Happens when applet is too small
                return

            # Find the nearest point to the cursor's x position and extend title
            idx = np.absolute(self.x - pos.x()).argmin()
            self.extend_title('({:.2f},{:.2f})'.format(self.x[idx], self.y[idx]))

            # Crosshair
            if self.ch_hline:
                self.plotItem.removeItem(self.ch_hline)
            if self.ch_vline:
                self.plotItem.removeItem(self.ch_vline)
            self.ch_hline = self.plotItem.addLine(y=self.y[idx])
            self.ch_vline = self.plotItem.addLine(x=self.x[idx])


def main():
    # Create applet object
    applet = artiq.applets.simple.TitleApplet(XYPlot, default_update_delay=0.1)

    # Add custom arguments
    applet.argparser.add_argument("--x-label", default=None, type=str, help="The X label")
    applet.argparser.add_argument("--y-label", default=None, type=str, help="The Y label")
    applet.argparser.add_argument("--sliding-window", default=0, type=int,
                                  help="Only show the latest data points")
    applet.argparser.add_argument("--subsample", default=0, type=int,
                                  help="Subsample data by the given factor before plotting")
    applet.argparser.add_argument("--multiplier", default=None, type=float,
                                  help="Multiply data before plotting")
    applet.argparser.add_argument("--crosshair", default=False, action='store_true',
                                  help="Enable the crosshair feature")
    applet.argparser.add_argument("--last", default=False, action='store_true',
                                  help="Show the value of the last data point in the title")
    applet.argparser.add_argument("--moving-average", default=0, type=int,
                                  help="Automatic uniform moving average calculation with the given size")

    # Add datasets
    applet.add_dataset("y", "Y values")
    applet.add_dataset("x", "X values", required=False)
    applet.add_dataset("error", "Error bars for Y values", required=False)
    applet.add_dataset("fit", "Fit for Y values", required=False)
    applet.add_dataset("fit-x", "X values for fit data", required=False)
    applet.add_dataset("v-lines", "Vertical lines", required=False)
    applet.add_dataset("h-lines", "Horizontal lines", required=False)
    applet.run()


if __name__ == "__main__":
    main()
