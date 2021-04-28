import cmath


class HarmonicTransformer:
    def __init__(self, signal, initial_frequency):
        self.signal = signal
        self.signal_length = len(signal)
        self.peak_vectors = []

        self.output_t = []
        self.output_real = []
        self.output_imaginary = []
        self.intersection_points_t = []
        self.intersection_points_real = []
        self.intersection_integral = 0
        self.determine_peak_vectors()
        self.calculate(initial_frequency)

    def determine_peak_vectors(self):
        derivatives = []
        previous_sample = 0
        for sample in self.signal:
            derivatives.append(sample - previous_sample)
            previous_sample = sample

        for index in range(len(derivatives)):
            if index > 0 and derivatives[index] <= 0 < derivatives[index - 1]:
                self.peak_vectors.append((index - 2, self.signal[index - 2]))
                self.peak_vectors.append((index - 1, self.signal[index - 1]))
                self.peak_vectors.append((index, self.signal[index]))

    def calculate(self, frequency):
        self.output_t = []
        self.output_real = []
        self.output_imaginary = []
        self.intersection_points_t = []
        self.intersection_points_real = []
        self.intersection_integral = 0

        for t, peak_vector in self.peak_vectors:
            result = cmath.exp((-2j * cmath.pi * t / (self.signal_length - 1)) * (self.signal_length / frequency))
            result *= peak_vector

        # for t in range(self.signal_length):
        #     result = cmath.exp((-2j * cmath.pi * t / (self.signal_length - 1)) * (self.signal_length / frequency))
        #     result *= self.signal[t]

            # if t > 0:
            #     previous_imaginary = self.output_imaginary[-1]
            #     if previous_imaginary > 0 and result.imag == 0:
            #         self.intersection_points_real.append(result.real)
            #         self.intersection_points_t.append(t)
            #
            #     if previous_imaginary > 0 > result.imag:
            #         r_1 = self.output_real[-1]
            #         r_2 = result.real
            #         q_1 = previous_imaginary
            #         q_2 = result.imag
            #         intersection = r_1 - q_1 * (r_2 - r_1) / (q_2 - q_1)
            #         self.intersection_points_real.append(intersection)
            #         self.intersection_points_t.append(t)
            #         self.intersection_integral += intersection

            self.output_t.append(t)
            self.output_real.append(result.real)
            self.output_imaginary.append(result.imag)
