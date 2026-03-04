import numpy as np

clock_speed = 288
buffer_size = 440
ratio_7_11 = 7/11
hades_beat_freq = 0.660688

x_grid = np.linspace(-buffer_size/2, buffer_size/2, clock_speed)
wait_signal = np.sin(2 * np.pi * hades_beat_freq * x_grid)
io_switch = np.array([1 if i % 2 == 0 else 0 for i in range(clock_speed)])

weight_distribution = []
for i, x in enumerate(x_grid):
    diffraction = np.sinc(x * ratio_7_11)
    weight = abs(diffraction * wait_signal[i] * io_switch[i])
    weight_distribution.append(weight)

actual_sum = np.sum(weight_distribution)
print(f"actual_sum: {actual_sum}")

