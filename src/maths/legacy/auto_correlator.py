import math


class AutoCorrelator:
    def __init__(self, signal, initial_frequency, initial_peak_squish):
        self.signal = signal
        self.frequency = initial_frequency
        self.comparison_signal_peak_squish = initial_peak_squish
        self.comparison_signal_multiplier = 100
        self.max_partials = 5
        self.gaussian_peak_decay = 0.1
        self.signal_derivative = self.calculate_signal_derivative(self.signal)
        self.signal_double_derivative = self.calculate_basic_signal_derivative(self.signal)
        # self.signal_double_derivative.pop(0)
        # self.signal_double_derivative.append(0)
        self.comparison_signal = self.calculate_comparison_signal()
        self.auto_correlated_signal = [0 for i in signal]
        self.auto_correlated_signal_double_derivative = [0 for i in signal]
        self.auto_correlation_integral = 0
        self.auto_correlation_integral_double_derivative = 0
        self.auto_correlation_integral = self.auto_correlate(self.signal_derivative, self.auto_correlated_signal)
        self.auto_correlation_integral_double_derivative = self.auto_correlate(
            self.signal_double_derivative, self.auto_correlated_signal_double_derivative
        )

    @staticmethod
    def calculate_signal_derivative(signal):
        result = []
        for index, sample in enumerate(signal):
            if index == 0 or index == len(signal) - 1:
                derivative = 0
            else:
                derivative = (signal[index + 1] - signal[index - 1]) / 2
            result.append(derivative)
        return result

    @staticmethod
    def calculate_basic_signal_derivative(signal):
        result = []
        for index, sample in enumerate(signal):
            if index == 0:
                derivative = 0
            else:
                derivative = sample - signal[index - 1]
            result.append(derivative)
        return result

    def calculate_comparison_signal(self):
        result = []
        for x, sample in enumerate(self.signal):
            value = 0
            for n in range(1, self.max_partials):
                component = (x - n * self.frequency) / self.comparison_signal_peak_squish
                decay = n ** self.gaussian_peak_decay
                peak = self.signal[n * self.frequency]
                value += -component / decay * math.exp(-(component ** 2)) #  / math.log(peak + 1)
            result.append(self.comparison_signal_multiplier * value)
        return result

    def auto_correlate(self, signal_derivative, output_signal):
        for index, sample in enumerate(signal_derivative):
            output_signal[index] = sample * self.comparison_signal[index]
        integral_result = 0
        for index, sample in enumerate(output_signal):
            value = sample
            # if sample < 0:
            #     value *= 2 / index
            integral_result += value
        integral_result /= len(output_signal)
        return integral_result

    def update_frequency(self, frequency):
        self.frequency = round(frequency)
        self.comparison_signal = self.calculate_comparison_signal()
        self.auto_correlation_integral = self.auto_correlate(self.signal_derivative, self.auto_correlated_signal)
        self.auto_correlation_integral_double_derivative = self.auto_correlate(
            self.signal_double_derivative, self.auto_correlated_signal_double_derivative
        )

    def update_peak_squish(self, peak_squish):
        self.comparison_signal_peak_squish = peak_squish
        self.comparison_signal = self.calculate_comparison_signal()
        self.auto_correlation_integral = self.auto_correlate(self.signal_derivative, self.auto_correlated_signal)
        self.auto_correlation_integral_double_derivative = self.auto_correlate(
            self.signal_double_derivative, self.auto_correlated_signal_double_derivative
        )
