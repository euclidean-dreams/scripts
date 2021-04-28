class AutoCorrelator:
    def __init__(self, signal, initial_iterations, initial_frequency):
        self.signal = signal
        self.signal_derivative = self.calculate_signal_derivative()
        self.iterations = initial_iterations
        self.frequency = initial_frequency
        self.shifted_signals_x = None
        self.shifted_signals_y = None
        self.shifted_signal_iteration = None
        self.auto_correlated_signal = [0 for i in signal]
        self.auto_correlation_integral = 0
        self.rebuild_iterations()
        self.auto_correlate()

    def calculate_signal_derivative(self):
        result = []
        for index, sample in enumerate(self.signal):
            if index == 0:
                derivative = 0
            else:
                derivative = sample - self.signal[index - 1]
            result.append(derivative)
        return result

    def auto_correlate(self):
        for iteration, shifted_signal in enumerate(self.shifted_signals_y):
            for index, sample in enumerate(shifted_signal):
                if iteration == 0:
                    self.auto_correlated_signal[index] = shifted_signal[index] ** 1 / 3
                else:
                    self.auto_correlated_signal[index] *= shifted_signal[index] ** 1 / 3
        self.auto_correlation_integral = 0
        for sample in self.auto_correlated_signal:
            self.auto_correlation_integral += sample
        self.auto_correlation_integral /= len(self.auto_correlated_signal)

    def update_frequency(self, frequency):
        self.frequency = round(frequency)
        self.auto_correlate()

    def update_iterations(self, iterations):
        self.iterations = round(iterations)
        self.rebuild_iterations()
        self.auto_correlate()

    def rebuild_iterations(self):
        self.shifted_signals_x = [[index for index, sample in enumerate(self.signal)] for i in range(self.iterations)]
        self.shifted_signals_y = [[1 for j in self.signal] for i in range(self.iterations)]
        self.shifted_signal_iteration = [i for i in range(self.iterations)]
