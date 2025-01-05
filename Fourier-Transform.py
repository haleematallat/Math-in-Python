#Fourier Transform
# F(ω) = ∫[−∞ to ∞] f(t) * e^(-j * ω * t) dt
#   where:
#   - F(ω) is the Fourier Transform (frequency domain representation)
#   - f(t) is the original function (time domain representation)
#   - ω is the angular frequency (ω = 2πf, f in Hz)
#   - e^(-j * ω * t) is the complex exponential
#   - ∫ is the integral over time (t)

def fourier_transform(f_t, t, omega):
    dt = t[1] - t[0]                    # time step
    result = 0                          # initialize integral result
    
    # This loop is the discrete version of the integral ∫
    for i in range(len(t)):
        # f(t) * e^(-j * ω * t) * dt
        result += f_t[i] * (cos(-omega * t[i]) + 1j * sin(-omega * t[i])) * dt
    
    return result

'''
The Fourier Transform integral ∫ is just:

1. A for-loop that goes through time points
2.Multiplies your signal f(t) by e^(-jωt)
3. Adds up all the pieces (dt)

Boils down to:

Loop through time
Multiply stuff
Add it up

The only slightly tricky part is e^(-jωt), which is just:

cos(-ωt) + j*sin(-ωt) [Euler's formula]
'''
