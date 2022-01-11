import math


class HarmonicTransformer:
    def __init__(self, signal, initial_frequency, initial_peak_squish, max_partials):
        self.signal = signal
        self.current_frequency = initial_frequency
        self.harmonic_signal_peak_squish = initial_peak_squish
        self.harmonic_signal_multiplier = 100
        self.max_partials = max_partials
        self.harmonic_peak_decay = 0.1
        self.signal_derivative = self.calculate_basic_signal_derivative(self.signal)
        self.harmonic_signal = self.calculate_harmonic_signal(initial_frequency)
        self.result_signal = [0 for i in signal]
        self.harmonic_integral = self.calculate_harmonic_integral(
            self.signal_derivative, self.harmonic_signal, self.result_signal
        )

    # @staticmethod
    # def calculate_signal_derivative(signal):
    #     result = []
    #     for index, sample in enumerate(signal):
    #         if index == 0 or index == len(signal) - 1:
    #             derivative = 0
    #         else:
    #             derivative = (signal[index + 1] - signal[index - 1]) / 2
    #         result.append(derivative)
    #     return result

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

    def calculate_harmonic_signal(self, frequency):
        signal_components = []
        for n in range(1, self.max_partials + 1):
            signal_component = []
            shift = n * frequency
            peak_value = self.signal[round(shift)]
            for x, sample in enumerate(self.signal):
                component = (x - shift) / self.harmonic_signal_peak_squish
                decay = n ** self.harmonic_peak_decay
                value = -component / decay * math.exp(-(component ** 2))
                # multiplier = self.harmonic_signal_multiplier / peak_value
                signal_component.append(1000 * value)
            signal_components.append(signal_component)

        result_signal = [0 for i in signal_components[0]]
        for signal in signal_components:
            for index, sample in enumerate(signal):
                result_signal[index] += sample
        return result_signal

    @staticmethod
    def calculate_harmonic_integral(harmonic_signal, signal_derivative, output_signal):
        for index, sample in enumerate(signal_derivative):
            output_signal[index] = sample * harmonic_signal[index]
        integral_result = 0
        for index, sample in enumerate(output_signal):
            value = sample
            if sample < 0:
                value = sample * 4
            integral_result += value
        integral_result /= len(output_signal)
        return integral_result

    def update_frequency(self, frequency):
        self.current_frequency = frequency
        self.harmonic_signal = self.calculate_harmonic_signal(frequency)
        self.harmonic_integral = self.calculate_harmonic_integral(
            self.signal_derivative, self.harmonic_signal, self.result_signal
        )

    def update_peak_squish(self, peak_squish):
        self.harmonic_signal_peak_squish = peak_squish
        self.harmonic_signal = self.calculate_harmonic_signal(self.current_frequency)
        self.harmonic_integral = self.calculate_harmonic_integral(
            self.signal_derivative, self.harmonic_signal, self.result_signal
        )

    def update_signal(self, signal):
        self.signal = signal
        self.signal_derivative = self.calculate_basic_signal_derivative(self.signal)
        self.harmonic_signal = self.calculate_harmonic_signal(self.current_frequency)
        self.result_signal = [0 for i in signal]
        self.harmonic_integral = self.calculate_harmonic_integral(
            self.signal_derivative, self.harmonic_signal, self.result_signal
        )
