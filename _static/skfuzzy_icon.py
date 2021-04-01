import numpy as np
import skfuzzy as fuzz
import scipy.ndimage as ndi
import skimage.io
from skimage.transform import resize
import matplotlib.pyplot as plt

kwargs = {'lw': 20, 'solid_capstyle': 'round'}


if __name__ == '__main__':

    # Generate membership functions corresponding to S, F, I, and U in logo
    x_sf = np.arange(0, 3.1, 0.1) - 0.1
    x_f2 = np.arange(0, 2.7, 0.1) - 0.1

    s_mf = fuzz.trapmf(x_sf, [1, 2, 3, 3]) * (2. / 3) + 0.4
    f_mf1 = fuzz.trapmf(x_sf, [1, 2, 3, 3]) * (2. / 3)
    f_mf2 = fuzz.trapmf(x_f2, [1, 1.6, 2.6, 2.6]) * 0.4

    bot = 0.4 * 2 / 3

    # Plot various membership functions
    fig, ax = plt.subplots(figsize=(6, 6))

    s = ax.plot(x_sf, s_mf, 'k', **kwargs)
    f1 = ax.plot(x_sf + 0.4, f_mf1, 'k', **kwargs)
    f2 = ax.plot(x_f2 + 0.4, f_mf2, 'k', **kwargs)

    ax.set_ylim(-0.5, 1.2)
    ax.set_xlim(-0.5, 5)
    ax.axis('off')

    # Save the logo text, then reload for modification
    fig.savefig('./temp.png', dpi=300, transparent=True)
    sharp = skimage.io.imread('./temp.png')[138:1348, 168:1378]

    blurred1 = ndi.gaussian_filter(sharp[..., 0], 15)
    blurred2 = ndi.gaussian_filter(sharp[..., 0], 50)

    blue = np.r_[0, 0, 140]
    logo = np.concatenate((np.ones_like(sharp[..., 0])[..., np.newaxis] * blue[0],
                           np.ones_like(sharp[..., 0])[..., np.newaxis] * blue[1],
                           np.ones_like(sharp[..., 0])[..., np.newaxis] * blue[2],
                           255 - np.fmin(blurred1, blurred2)[..., np.newaxis]),
                          axis=-1).round().astype(np.uint8)

    # Reduce scale for web use
    ico16 = resize(logo, (16, 16))
    ico32 = resize(logo, (32, 32))
    ico64 = resize(logo, (64, 64))
    ico128 = resize(logo, (128, 128))
    ico256 = resize(logo, (256, 256))
    ico512 = resize(logo, (512, 512))

    # Save results
    skimage.io.imsave('./icon_16px.png', ico16)
    skimage.io.imsave('./icon_32px.png', ico32)
    skimage.io.imsave('./icon_64px.png', ico64)
    skimage.io.imsave('./icon_128px.png', ico128)
    skimage.io.imsave('./icon_256px.png', ico256)
    skimage.io.imsave('./icon_512px.png', ico512)
