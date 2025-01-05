# Forward Fourier Transform: Signal -> Frequencies
def time_to_frequency(signal, times):
    frequencies = []
    
    # For each desired frequency we want to find
    for freq in range(100):  # Check first 100 frequencies
        wave_strength = 0
        
        # Compare signal against this frequency
        for t in times:
            wave = complex_wave(frequency=freq, time=t)
            wave_strength += signal[t] * wave
            
        frequencies.append(wave_strength)
    
    return frequencies

# Inverse Fourier Transform: Frequencies -> Signal
def frequency_to_time(frequencies, desired_times):
    reconstructed_signal = []
    
    # For each time point we want to reconstruct
    for t in desired_times:
        signal_value = 0
        
        # Add up contribution from each frequency
        for freq, strength in enumerate(frequencies):
            wave = complex_wave(frequency=freq, time=t)
            signal_value += strength * wave
            
        # Scale result
        signal_value = signal_value / (2 * pi)
        reconstructed_signal.append(signal_value)
    
    return reconstructed_signal

# Helper function to create a wave of given frequency
def complex_wave(frequency, time):
    # e^(jwt) = cos(wt) + j*sin(wt)
    return cos(frequency * time) + 1j * sin(frequency * time)

# Example usage:
times = [0, 0.1, 0.2, 0.3, 0.4, 0.5]  # Sample times
signal = [cos(2*t) for t in times]     # Original signal

# Transform signal to frequencies and back
frequencies = time_to_frequency(signal, times)
reconstructed = frequency_to_time(frequencies, times)
'''
Forward transform (time_to_frequency):

1. Takes a signal in time
2. For each frequency: checks how much of that frequency exists in the signal
3. Returns list of frequency strengths


Inverse transform (frequency_to_time):

1. Takes frequency strengths
2. For each time: adds up all frequencies with their strengths
3. Returns reconstructed signal



It's like:

Forward: "How much of each frequency is in my signal?"
Inverse: "Add up all frequencies to get back my signal"
'''
