import numpy as np
import skfuzzy as fuzz
import scipy.ndimage as ndi
import skimage.io
from skimage.transform import rescale
import matplotlib.pyplot as plt

kwargs = {'lw': 20, 'solid_capstyle': 'round'}


if __name__ == '__main__':

    # Generate membership functions corresponding to S, F, I, and U in logo
    x_sf = np.arange(0, 3.1, 0.1) - 0.1
    x_f2 = np.arange(0, 2.7, 0.1) - 0.1
    x_i = np.arange(3.6, 4.05, 0.1)
    x_u1 = np.arange(3.0, 3.45, 0.1)
    x_u2 = np.arange(3.0, 4.05, 0.1)
    x_u3 = np.arange(4.0, 4.45, 0.1)

    s_mf = fuzz.trapmf(x_sf, [1, 2, 3, 3]) * (2. / 3) + 0.4
    f_mf1 = fuzz.trapmf(x_sf, [1, 2, 3, 3]) * (2. / 3)
    f_mf2 = fuzz.trapmf(x_f2, [1, 1.6, 2.6, 2.6]) * 0.4
    i_mf = (x_i - 3.6) * (2. / 3) + 0.4
    u1_mf = (x_u1 - 3) * (2. / 3)
    u2_mf = np.zeros_like(x_u2)
    u3_mf = (x_u3 - 4) * (2. / 3)

    bot = 0.4 * 2 / 3

    # Plot various membership functions
    fig, ax = plt.subplots(figsize=(8, 6))

    s = ax.plot(x_sf, s_mf, 'k', **kwargs)
    f1 = ax.plot(x_sf + 0.4, f_mf1, 'k', **kwargs)
    f2 = ax.plot(x_f2 + 0.4, f_mf2, 'k', **kwargs)
    i = ax.plot(x_i, i_mf, 'k', **kwargs)
    u1 = ax.plot(x_u1, u1_mf, 'k', **kwargs)
    u2 = ax.plot(x_u2, u2_mf, 'k', **kwargs)
    u3 = ax.plot(x_u3, u3_mf, 'k', **kwargs)

    # At this point, for brevity, the rest are generated as lines
    k1 = ax.plot([4.5, 5.3], [0.4, 0.4 + 2. / 3 - 4 / 30.], 'k', **kwargs)
    k2 = plt.plot([4.8, 5.5], [0.525, 0.4], 'k', **kwargs)
    k3 = ax.plot([4.8, 5.9], [0.525, 2. / 3], 'k', **kwargs)
    i2 = ax.plot([6.2, 6.6], [0.4, 2. / 3], 'k', **kwargs)
    t1 = ax.plot([7, 7.8], [0.4, 0.4 + 2. / 3 - 4 / 30.], 'k', **kwargs)
    t2 = ax.plot([7.1, 8.1], [0.8, 0.8], 'k', **kwargs)
    z1a = ax.plot([5.1, 5.5], [bot, bot], 'k', **kwargs)
    z1b = ax.plot([5.5, 5.9], [bot, 0], 'k', **kwargs)
    z1c = ax.plot([5.9, 6.3], [0, 0], 'k', **kwargs)
    z2a = ax.plot([6.1, 6.5], [bot, bot], 'k', **kwargs)
    z2b = ax.plot([6.5, 6.9], [bot, 0], 'k', **kwargs)
    z2c = ax.plot([6.9, 7.3], [0, 0], 'k', **kwargs)
    y1 = ax.plot([8, 8.4], [0, bot], 'k', **kwargs)
    y2 = ax.plot([8, 9], [0, 0], 'k', **kwargs)
    y3 = ax.plot([8.6, 9.4], [-bot, bot], 'k', **kwargs)
    y4 = ax.plot([7.6, 8.6], [-bot, -bot], 'k', **kwargs)

    ax.set_ylim(-0.5, 1.2)
    ax.set_xlim(-0.5, 10.6)
    ax.axis('off')

    # Save the logo text, then reload for modification
    fig.savefig('./temp.png', dpi=300, transparent=True)
    sharp = skimage.io.imread('./temp.png')[138:1572, 219:2112, :]

    blurred1 = ndi.gaussian_filter(sharp[..., 0], 15)
    blurred2 = ndi.gaussian_filter(sharp[..., 0], 50)

    blue = np.r_[0, 0, 140]
    logo = np.concatenate((np.ones_like(sharp[..., 0])[..., np.newaxis] * blue[0],
                           np.ones_like(sharp[..., 0])[..., np.newaxis] * blue[1],
                           np.ones_like(sharp[..., 0])[..., np.newaxis] * blue[2],
                           255 - np.fmin(blurred1, blurred2)[..., np.newaxis]),
                          axis=-1).round().astype(np.uint8)

    # Reduce scale for web use
    downscaled = rescale(logo, 0.25)

    # Save results
    skimage.io.imsave('./logo_full.png', logo)
    skimage.io.imsave('./logo.png', downscaled)
