# display adjustment

2026-09-05

## background

One thing that Windows has that Ubuntu doesn't is display adjustment.
So I created an app.
This time, I created it using Qt (C++) and making full use of AI.

![UI](essays/2026-09-05-display-ajast.png)

## Main features

### Multi-display detection & screen identification

- Detects all connected displays (resolution, refresh rate, DPI, color depth, etc.)
- "Screen Identification" function displays a large identification banner on the target monitor

### Test pattern drawing engine

- **Brightness**: 0%~5% Adjust the dark gradation standard with low brightness step and flashing test block
- **Contrast**: 95% to 100% Highlight gradation and each color highlight bar prevents overexposure
- **Gamma 2.2**: Tone curve adjustment using 1px black and white equal width raster stripes and standard tone patch
- **Grayscale & Color Balance**: 32-level step bar, smooth continuous gradation, RGB primary color gradation
- **Sharpness & Focus**: Optimized edge contour (halo/ringing) with 1px vertical and horizontal lines and checkerboard
- **Color uniformity & missing dot inspection**: Single color (white, gray, black, red, green, blue, cyan, magenta, yellow) full screen display
- **Screen ratio & overscan**: 1:1 pixel mapping, dot-by-dot, inspection for 1px missing outer frame

### step-by-step wizard

- Just follow the guide to complete optimal monitor settings (with OSD operation instructions)

### DDC/CI & XRandR hardware/software collaboration

- `ddcutil` In supported environments, the monitor's internal brightness and contrast can be controlled directly from the sliders.
- Software correction and automatic fallback to manual OSD guidance mode in X11/XRandR environments

## sauce

- [AdjustDisplay](https://github.com/amekusa03/AdjustDisplay)
