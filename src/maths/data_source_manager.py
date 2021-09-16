from bokeh.models import ColumnDataSource


class DataSourceManger:
    def __init__(self, signal, harmonic_transformer):
        self.harmonic_transformer = harmonic_transformer
        self.signal_data = ColumnDataSource()
        self.signal_derivative_data = ColumnDataSource()
        self.harmonic_signal_data = ColumnDataSource()
        self.result_signal_data = ColumnDataSource()
        self.harmonic_integral_data = ColumnDataSource()
        # self.harmonic_transform = ColumnDataSource()
        self.update_signal(signal)

    def update_signal(self, signal):
        self.signal_data.data = {
            "x": [i for i in range(len(signal))],
            "y": signal
        }
        self.update()

    def update(self):
        self.signal_derivative_data.data = {
            "x": [index for index, sample in enumerate(self.harmonic_transformer.signal_derivative)],
            "y": self.harmonic_transformer.signal_derivative
        }
        self.harmonic_signal_data.data = {
            "x": [index for index, sample in enumerate(self.harmonic_transformer.harmonic_signal)],
            "y": self.harmonic_transformer.harmonic_signal
        }
        self.result_signal_data.data = {
            "x": [index for index, sample in enumerate(self.harmonic_transformer.result_signal)],
            "y": self.harmonic_transformer.result_signal
        }
        self.harmonic_integral_data.data = {
            "x": [0],
            "y": [self.harmonic_transformer.harmonic_integral]
        }
        # self.harmonic_transform.data = {
        #     "x": [index for index, sample in enumerate(self.harmonic_transformer.harmonic_transform)],
        #     "y": self.harmonic_transformer.harmonic_transform
        # }
