from bokeh.models import ColumnDataSource


class DataSourceManger:
    def __init__(self, signal, harmonic_transformer, auto_correlator):
        self.harmonic_transformer = harmonic_transformer
        self.auto_correlator = auto_correlator
        self.harmonic_transform_data = ColumnDataSource()
        self.intersection_integral_data = ColumnDataSource()
        self.intersection_data = ColumnDataSource()
        self.peak_vector_data = ColumnDataSource()
        self.shifted_signals = ColumnDataSource()
        self.auto_correlated_signal = ColumnDataSource()
        self.auto_correlation_integral_data = ColumnDataSource()
        self.signal_data = ColumnDataSource(data={
            "x": [i for i in range(len(signal))],
            "y": signal
        })
        self.signal_peak_data = ColumnDataSource(data={
            "x": [peak_vector[0] for peak_vector in harmonic_transformer.peak_vectors],
            "y": [peak_vector[1] for peak_vector in harmonic_transformer.peak_vectors],
        })
        self.update()

    def update(self):
        self.harmonic_transform_data.data = {
            "x": self.harmonic_transformer.output_real,
            "y": self.harmonic_transformer.output_imaginary,
            "t": self.harmonic_transformer.output_t
        }

        peak_vector_x = []
        peak_vector_y = []
        peak_vector_t = []
        for i in range(len(self.harmonic_transformer.output_real)):
            peak_vector_x.append([0, self.harmonic_transformer.output_real[i]])
            peak_vector_y.append([0, self.harmonic_transformer.output_imaginary[i]])
            peak_vector_t.append(self.harmonic_transformer.output_t[i])

        self.peak_vector_data.data = {
            "xs": peak_vector_x,
            "ys": peak_vector_y,
            "t": peak_vector_t
        }
        self.intersection_integral_data.data = {
            "x": [0],
            "y": [self.harmonic_transformer.intersection_integral]
        }
        self.intersection_data.data = {
            "x": self.harmonic_transformer.intersection_points_t,
            "y": self.harmonic_transformer.intersection_points_real
        }
        self.shifted_signals.data = {
            "xs": self.auto_correlator.shifted_signals_x,
            "ys": self.auto_correlator.shifted_signals_y,
            "iteration": self.auto_correlator.shifted_signal_iteration
        }
        self.auto_correlated_signal.data = {
            "x": [index for index, sample in enumerate(self.auto_correlator.auto_correlated_signal)],
            "y": self.auto_correlator.auto_correlated_signal
        }
        self.auto_correlation_integral_data.data = {
            "x": [0],
            "y": [self.auto_correlator.auto_correlation_integral]
        }
