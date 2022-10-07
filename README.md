# Pyrometry image processing

## Temperature maps

**Grayscale pyrometry:** currently basic; uses grayscale opencv import, then just applies a jet filter. Doesn't yet copy the full impl in the paper.

**Ratio pyrometry:** pretty damn close to what's in the paper but it's very broken atm

**Test image:**

![](01-0001.png)

**Grayscale pyrometry result:**

![](01-0001-transformed-grayscale.png)

**Ratio pyrometry result (with 2x2 convolutional smoothing):**

According to general researcher consensus, ratio pyrometry is supposed to be more accurate.

![](01-0001-transformed-ratio.png)
