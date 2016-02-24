# Trusting a photograph and Understanding Sensor Systems
For our material, we have claimed that digital photographs are sufficient for reasoning about the spectral profiles of light sources. In this section, we hope to teach you enough about sensor systems, light, and color to make educated assessments of this assertion.

# What is Color?
- still need metamerism

# Absorption, Reflection, Refraction

# Sensor Systems
Traditionally, the term *color* refers to **human visible light**. Although this is a very limited definition, it establishes a good starting point for understanding perception of color. Because of this, the first sensor system we will discuss is the human eye, it's evolution and design. Next we will discuss imitating sensor systems like cameras and telescopes which will lead to a discussion about metamerism and RGB color mapping. Finally, we will discuss ways to express and communicate color like CIE charts and other color mapping options.

## Human Eye
The human eye refracts electromagnetic radiation at the cornea, through a focusing lens, and projects an inverted image of the world onto a the fovia, containing rod cells and cone cells of three types that act as sensors of electromagnetic radiation. L-cone, M-cone, S-cone cells have peak sensor response around wavelengths perceived as red, green, and blue light respectively. The spectra rendered by these cone cells in the human eye span ~400nm-700nm.

![Human Eye](http://cdn.picturecorrect.com/wp-content/uploads/2015/02/image-sensors-11.jpg)

Transduction of light into an electrical signal has four steps

1. light activates rhodopsin
2. activated rhodopsin stimulates a G protine to activate a phosphodiesterase enzyme
3. phosphodiesterase enzyme decreases the concentration of cyclic GMP in the photoreceptor cytoplasm
4. the decrease in cyclic (guanosine monophosphate) GMP closes cyclic nucleotide-gated ion channels similar to the channels in olfactory receptor cells. When the channels close, the Na⁺ influx decreases and the photoreceptor hyperpolarizes rather than depolarizes. 

- Discussion about cones, photopigment molecules and cone type density [...resource](http://hyperphysics.phy-astr.gsu.edu/hbase/vision/rodcone.html#c1)

Terrestrial eyes evolved to discern colors in this limited spectrum as a result of exposure to light least influenced by **atmospheric opacity**; a term we use to describe the spectral range of electromagnetic radiation able to pass through our atmosphere. The graphic below shows that 400-780nm (highlighted by the rainbow) is a consistent range with low *atmospheric distortion*.

![atmospheric opacity](https://upload.wikimedia.org/wikipedia/commons/3/34/Atmospheric_electromagnetic_opacity.svg)

- Due to the valley represented in this graphic... what about 9μm-10μm or 5cm-20m range... ?
- glass absorbs light

## Imitating Sensor Systems
Sensor systems on cameras are designed to mimic the human eye, whereas sensor systems for telescopes are designed to take full advantage of **visible light** spectrum. We will discuss the physics of silicon sensors used in these systems, then the design of cameras and telescopes. Finally, we will use this to establish a clear understanding of metamerism.

Although the design goals of **visible light** sensor systems are very similar, the differences will be paramount in defining and understanding **color pollution** (the topic of this course).

### Silicon Sensors
Silicon sensors are the primary mechanism used in measuring **visible light** spectrum. In this section we will discuss why and how we achieve sensing of color with silicon. This will be our building blocks for designing sensor arrays found in cameras and telescopes.

#### Quantum Efficiency
Sensors hit by photons will either *absorb* and redistribute the energy as heat, or trigger with a measurable chemical reaction. The **quantum efficiency** of a sensor is the probability of triggering an observable chemical reaction as a function of wavelength.

![Quantum Efficiency](https://placehold.it/350x150)

It has been observed that silicon sensors have a fairly high efficiency spanning the **visible light**.

![Silicon Quantum Efficiency](http://www.awaiba.com/v4/wp-content/uploads/2014/03/technology-6.jpg)

#### Color Filters
Although we can observe photo triggered chemical reactions, the only information that we gather is whether a sensor has been triggered **success** or **failure**. Without some way to limit the **transmission band** sent to a sensor, we would only ever render gray-scale information. We use filters to control (or limit) processed photons to those traveling in our desired **transmission band**.

![Filter Behavior](http://www.naoj.org/Observing/Instruments/SCam/jpg/johnson.gif)

### Modern Cameras

### KECK Telescope

# Metamers
