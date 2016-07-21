# Introduction
- I am Philip
- Python 4+ Years
  - Academic
    - Computer Graphics
    - Cryptography
  - Industry
    - Integration Tests - EMC
	- Process Management/Visualization - Galois Inc./Melinae
	- Education - PDXCodeGuild/Melinae/C&W Energy USA
	- Scientific/Data Analytic/Engineering/Visualisation - C&W Energy USA

# Project What/Why
- Develop low cost tools to quantitatively study light pollution
- Describe human eye response to light
- Describe how light pollution effects terrestrial telescopes

# Problem Statement
Current measures for 'lighting needs' disregard metrics like 'blue light content'. Since 'blue light content' critically impacts many industries and habitats we hope to motivate a change in industry measurement standards. From nighttime photographs of lit street lamps, can we classify the type of bulb by approximating spectral profile?

# Strategy for Analytics
- Standardize/Sanatize input image
- Identify light sources
- Extract RGB features from each lamp
  - Area of red green blue content
  - PDF fitting
- Classify lamps

# Tools used so far
- GitHub
  - Version Control
  - ZenHub
  - Jupyter and Markdown Rendering
- Amazon Web Services (AWS)
- ~1200 lines Python
  - argparse
  - imread, imhdr, Pillow
  - sklearn, scipy, numpy, matplotlib
  - PonyORM
- Jupyter
- Google Hangouts

# Technical Goals
- Work must be reproducible
- Don't waste compute time
- Simple install
- Yield usable visualisations
- Easily swap feature extraction
