import numpy as np
clock_speed = 288
buffer_size = 440
ratio_7_11 = 7/11
hades_beat_freq = 0.660688

x_grid = np.linspace(0, buffer_size, clock_speed)
wait_signal = np.sin(2 * np.pi * hades_beat_freq * x_grid)
io_switch = np.array([1 if i % 2 == 0 else 0 for i in range(clock_speed)])

w = np.abs(np.sinc(x_grid * ratio_7_11) * wait_signal * io_switch)
actual = np.sum(w)
print(actual)
