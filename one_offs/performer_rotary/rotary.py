from time import sleep

import zmq
from RPi import GPIO

from conductor_messenger import ConductorMessenger

CLK_PIN = 17
DT_PIN = 18

INITIAL_THRESHOLD = 5
INCREMENT = 0.5
MAX_THRESHOLD = 10
MIN_THRESHOLD = INCREMENT


def main():
    context = zmq.Context()
    conductor_messenger = ConductorMessenger(context, "tcp://*:44440")

    threshold = INITIAL_THRESHOLD
    value_changed = False
    last_clk_state = GPIO.input(CLK_PIN)

    while True:
        sleep(0.01)
        current_clk_state = GPIO.input(CLK_PIN)
        current_dt_state = GPIO.input(DT_PIN)
        if current_clk_state != last_clk_state:
            if current_dt_state != current_clk_state:
                threshold += INCREMENT
                if threshold > MAX_THRESHOLD:
                    threshold = MAX_THRESHOLD
                value_changed = True
            else:
                threshold -= INCREMENT
                if threshold < MIN_THRESHOLD:
                    threshold = MIN_THRESHOLD
                value_changed = True
        last_clk_state = current_clk_state
        if value_changed:
            conductor_messenger.send_threshold(threshold)
            value_changed = False


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    try:
        main()
    finally:
        GPIO.cleanup()
