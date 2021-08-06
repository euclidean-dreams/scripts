import struct

INT_SIZE = 4
FLOAT_SIZE = 4


class SpectrogramManager:
    def __init__(self, data_file_name):
        self.spectrogram = []
        with open(data_file_name, mode='rb') as input_file:
            raw_file_content = input_file.read()
            end_index = 0
            while end_index < len(raw_file_content):
                start_index = end_index
                end_index = end_index + INT_SIZE
                layer_count = struct.unpack("i", raw_file_content[start_index:end_index])[0]
                start_index = end_index
                end_index = end_index + INT_SIZE
                buffer_size = struct.unpack("i", raw_file_content[start_index:end_index])[0]
                for layer in range(layer_count):
                    start_index = end_index
                    end_index = start_index + buffer_size * FLOAT_SIZE
                    if layer == 0:
                        self.spectrogram.append(
                            list(struct.unpack("f" * buffer_size, raw_file_content[start_index:end_index]))
                        )

    def get_max_index(self):
        return len(self.spectrogram) - 1

    def get_signal(self, index):
        return self.spectrogram[index]
