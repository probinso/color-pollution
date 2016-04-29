# Introduction
Our project will grow your understanding of light and sensor systems. Although there are many topics in this space, we will primarily focus on how industries communicate their lighting needs. Our motivating example is a study of light pollution and impact to astronomy.

For each section below we will link to material, either provided by others, or generated ourselves. For any section, this may include:
- References to relative articles
- Physical systems video lectures
- Programming video lectures

## Table of Contents


# Project: Dark Sky Objectives for Terestrial Astronomy
In this project we discuss light polution's effect on terrestrial astronomy. Although we go into greater detail in other sections, we summarize this below.

## Background Information
The below image shows measurements of our atmosphere's natural light [emissions](YO DOG NEED WORKSHEET), (also known as night glow). We can observe that the Blue 400~550nm band (also known as g-prime band) has little natural emissions; where as the remaining terrestrial visible light spectrum has intense emissions.

![Night Glow](./images/index.png)

```python
import numpy as np
import matplotlib.pyplot as plt

datafile = lambda filename: transpose(array(read_csv(filename)))
night_glow = datafile('./src/notebooks/datasets/Night_glow.csv')

plt.xlabel('Wavelength (nm)', fontsize = 12)
plt.ylabel('F($\lambda$) [10$^{-17}$ erg s$^{-1}$ cm$^{-2}$ $\AA$ arcsec$^{-2}$]', fontsize = 12)
plt.tick_params(axis='x', labelsize=10)
plt.tick_params(axis='y', labelsize=10)
plt.plot(night_glow[0], night_glow[1], '-', color = 'b', linewidth = 1)
plt.grid(True)
plt.annotate('[O1]', (520, 6),   color ='r')
plt.annotate( 'Na' , (580, 4.2), color ='r')
plt.annotate('[O1]', (635, 4.2), color ='r')
plt.xlim(400, 1000)
plt.show()
```

Although blue has low natural emissions, it scatters very easily in our atmosphere due to [rayleigh scattering](http://spaceplace.nasa.gov/blue-sky/en/) resulting in greater signal-noise in these bands. In order for telescopes to capture useful images, they filter out bands that have high signal-noise in the atmosphere. This results in less informative images, yielding lower return on investment.

It is exceptionally expensive to setup telescopes, and relocation is often not an option. In order to preserve their ability to contribute, astronomers join organizations like [International Dark Sky Association](http://darksky.org/) that lobby to influence public artificial lighting policies.

## Historical Consiquence of Language


