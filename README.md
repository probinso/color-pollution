# What is Color?
**PRESENTLY ALL IMAGES ARE PLACE HOLDERS**

When studying color, your goal is to understand:

- a brief knowledge electromagnetic radiation 
- sensor systems
- relationships between electromagnetic radiation and sensor systems
- color coordinate systems and their goals
    - CIE charts
	- Color-maps
	- RGB
- metamerism

# Electromagnetic Radiation
For this course, we will need a basic knowledge of **electromagnetic radiation**. In this section we will introduce this in increasing detail, through Ray Tracing, Waves, and Particles. Finally, we will discuss different bands of measured electromagnetic radiation.

For this color pollution course, most of our data and example material is limited to terrestrial color, however a good understanding of electromagnetic radiation in these forms will allow you to abstract the information of this course environments dissimilar to terrestrial atmospheres.

## Ray Tracing
The simplest, and oldest consistent means of discussing traveling light, is to think of it has a series of rays. We claim that light is emitted from a source, with a color property, and travels in a straight line. These rays then bounce off of impeding objects, until they have either been perceived or absorbed.

This is the model we used to design old *camera obscura* and *pinhole cameras* of the 18th century. Because light is bouncing off in every direction from an impeding object, if you create a dark enough chamber with a pinhole opening then you can view an inverted image of the original object. The walls of the chamber block out light that would white wash the image. In other words, the use of a pinhole limits the **signal to noise ratio.**

![Pinhole Camera](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Pinhole-camera.svg/2000px-Pinhole-camera.svg.png)

## Waves
Although thinking of **electromagnetic radiation** in the form of rays is helpful, it is an incomplete view of the world. We see this when we take a white light and shine it at a prism. If the light was traveling as a ray, then the light that leaves the prism would come out as white as well. This is not the case. We find that, in fact, white light is a composite span of wavelengths which bend at different angles in different mediums. 

![Prism Experiment](http://www-psych.stanford.edu/~lera/psych115s/notes/lecture5/images/floyd.jpg)

## Particles
In order to understand concepts like **quantum efficiency**, we will also need to think of lite as a series of particles (traveling in a wave along a ray). A quantum of **electromagnetic radiation** is called a photon. **Electromagnetic radiation** sources emit with differing densities of photons. Each obstacle in a photon's path has a probability of interrupting the photon's travel before colliding with a recording sensor.

## Bands
We often talk about Bands of the Electromagnetic Spectrum in order to simplify communication. A band is a continuous range of wavelengths that we have assigned a useful label. Human Visible light is a very narrow band...

Additionally, it would be nice to use sensors to exactly determine the wavelength of incident **electromagnetic radiation**, however, existing sensor systems are limited to communicating only a triggered state. It is common practice to reduce a continuous span of wavelengths to well defined bands and measure intensity by counting the triggered sensors per band in unit area. This is inspired by how biological systems reduce colors. This translation is similar to using the Floor function accross the real numberline.

Since astronomers are often concerned with bands beyond human visable light, they use color mapping to make images to improve communication...

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

# Color maps
## Approximation and Smoothing of Data

In physics courses, you are often told to approximate values in your models. In my first life, I thought this was only to accommodate the  the lazy physicist. In my second life, I thought this was a strategy to accommodate the limitations introduced by using computers. Although these are good answers, they do not respect the true value of approximation.

It is often our goal to measure, analyze, and communicate properties of physical systems such that the behavior of similar systems may be predicted. Measuring properties of a physical system is very difficult. Enormous time and cost is put into developing environments and tools to increase the accuracy of these measurements. When we do not have these resources, approximations can be used to smooth out the noise inherent to our instrumentation and environment.



```python
from lamplight import image_info, save_images

ftype, fname, fdata = image_info("misty-street-lights.jpg")
step_gen = step_range_gen(25, 15)

src_points_dict = get_index_of(src_image)

src_cluster_dict = get_cluster_dict(src_points_dict, step_gen)

src_image = f(src_image, src_cluster_dict, 1, next(take(step_gen.range, 1)))
top_image = f(top_image, top_cluster_dict, 1, next(take(step_gen.range, 1)))	
# incomplete
```
## Example of Smoothing

This is a source image of two street lamps at night

![Orig](src/lamplight/images/misty-street-lights.jpg)

It is our goal to atomatically identify clusters of high intensity green light. The images below perform this  clustering task with exactly the same parameters, but the second has a smoothing.

This image highlights all clusters according to specific parameters around green's highest intensity

![Cluster](src/lamplight/images/src_misty-street-lights.jpeg)

This image highlights all clusters according to the same parameters around green's highest intensity with smoothing

![Tops](src/lamplight/images/top_misty-street-lights.jpeg)

---

# For Project

- [markdown guide](https://help.github.com/articles/github-flavored-markdown/)
- [colormaps for oceanography](https://www.youtube.com/watch?v=XjHzLUnHeM0)
- [topographical maps](https://stackoverflow.com/questions/263305/drawing-a-topographical-map)
- [keyhole telescopes](https://en.wikipedia.org/wiki/KH-11_Kennan)
- [clustering techniques](http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#example-cluster-plot-dbscan-py)
- [Data Structures for DDBand](https://en.wikipedia.org/wiki/Quadtree)

# Goals of this repository
We are hoping to gather and develop lecture materials for a course we are designing **sensor systems and color pollution**.

## Outline
- Introduction
    - What is color
        - [Metamerism Wiki] (https://en.wikipedia.org/wiki/Metamerism_(color))
        - What is color history
    - How do sensory systems, capture light and color
        - What types elements produce refraction light
        - Ray tracing with refraction and reflection
    - Human eye
- Filters and content goals
- Types of sensor systems/architecture
    - Keck
    - Eye
    - Camera
- Noise
- **Raw vs processed Images from a camera**
- Signal Noise
    - Scattering (from system)
    - Atmospheric physics (from environment)
- Limiting pollution for your sensor
- Artificial Lighting
- Understanding the human market
    - What do humans want to see?
    - What noise is caused in their environment?
- Understanding the astronomy market
    - What do astronomers want to see?
    - What noise is caused in their environment?
    - Simplest solutions
        - No light
        - Low pressure sodium with filter
        - Other light options

