
# Math as Code

A collection of mathematical concepts explained through their programming equivalents. This project aims to bridge the gap between mathematical notation and practical implementation.

#### "Mathematics is the art of giving the same name to different things." - Henri Poincaré

## Overview

Mathematical notation can often obscure simple concepts behind complex symbols. This repository demonstrates how common mathematical operations can be expressed as straightforward programming constructs.

## Examples

### Summation (Σ)
The summation symbol represents a loop that accumulates values through addition:
```python
# Mathematical Notation:
# Σ(3n) from n=0 to 4

# Programming Implementation:
sum = 0
for(n=0; n<=4; n++) 
    sum += 3*n
```

### Product (Π)
Similarly, the product symbol represents a loop that accumulates values through multiplication:
```python
# Mathematical Notation:
# Π(2n) from n=1 to 4

# Programming Implementation:
prod = 1
for(n=1; n<=4; n++)
    prod *= 2*n
```

### Fourier Transform
The Fourier Transform integral can be understood as a loop summing wave components:
```python
# Mathematical Notation:
# F(ω) = ∫ f(t) * e^(-jωt) dt

# Programming Implementation:
result = 0
for t in time_points:
    result += signal[t] * complex_wave(w, t) * dt
```


## Contributing

Contributions are welcome. To add a new mathematical concept:

1. Create a clear implementation that parallels the mathematical notation
2. Include both the mathematical form and code implementation
3. Add explanatory comments linking the notation to the code
4. Provide simple examples demonstrating the concept

## Purpose

This project serves as a bridge between mathematical theory and practical implementation, making mathematical concepts more accessible through programming.

