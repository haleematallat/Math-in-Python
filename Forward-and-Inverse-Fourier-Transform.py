import numpy as np
from typing import Union, List, Tuple
from dataclasses import dataclass

@dataclass
class TransformParameters:
    """Parameters for Fourier Transform computation"""
    sample_rate: float       # Sampling rate in Hz
    freq_resolution: float   # Frequency resolution in Hz
    n_samples: int          # Number of samples
    n_frequencies: int      # Number of frequency points

@dataclass
class TransformResult:
    """Result of Fourier Transform computation"""
    frequencies: np.ndarray  # Frequency points
    spectrum: np.ndarray    # Complex spectrum
    magnitude: np.ndarray   # Magnitude spectrum
    phase: np.ndarray       # Phase spectrum in radians

class FourierTransform:
    def __init__(self, sample_rate: float):
        """
        Initialize Fourier Transform calculator
        
        Args:
            sample_rate: Sampling rate in Hz
        """
        self.sample_rate = sample_rate
        
    def _calculate_parameters(self, signal: np.ndarray) -> TransformParameters:
        """Calculate transform parameters based on input signal"""
        n_samples = len(signal)
        freq_resolution = self.sample_rate / n_samples
        n_frequencies = n_samples // 2 + 1  # Nyquist limit
        
        return TransformParameters(
            sample_rate=self.sample_rate,
            freq_resolution=freq_resolution,
            n_samples=n_samples,
            n_frequencies=n_frequencies
        )
    
    def forward(self, signal: np.ndarray) -> TransformResult:
        """
        Compute forward Fourier Transform
        
        F(ω) = ∫[−∞ to ∞] f(t) * e^(-j * ω * t) dt
        
        Args:
            signal: Time domain signal
            
        Returns:
            TransformResult containing frequencies and complex spectrum
        """
        params = self._calculate_parameters(signal)
        
        # Compute frequencies array
        frequencies = np.fft.rfftfreq(params.n_samples, 1/self.sample_rate)
        
        # Compute FFT
        # Using rfft for real input signals (more efficient than fft)
        spectrum = np.fft.rfft(signal) / params.n_samples
        
        # Compute magnitude and phase
        magnitude = np.abs(spectrum)
        phase = np.angle(spectrum)
        
        return TransformResult(
            frequencies=frequencies,
            spectrum=spectrum,
            magnitude=magnitude,
            phase=phase
        )
    
    def inverse(self, spectrum: np.ndarray, n_samples: int) -> np.ndarray:
        """
        Compute inverse Fourier Transform
        
        f(t) = 1/(2π) * ∫[−∞ to ∞] F(ω) * e^(j * ω * t) dω
        
        Args:
            spectrum: Frequency domain spectrum
            n_samples: Number of time domain samples to reconstruct
            
        Returns:
            Reconstructed time domain signal
        """
        # Compute inverse FFT and apply proper scaling
        return np.fft.irfft(spectrum * n_samples, n=n_samples)
    
    def analyze_signal(self, signal: np.ndarray) -> dict:
        """
        Perform complete signal analysis
        
        Args:
            signal: Time domain signal
            
        Returns:
            Dictionary containing signal analysis results
        """
        params = self._calculate_parameters(signal)
        transform_result = self.forward(signal)
        
        # Find dominant frequencies (peaks in magnitude spectrum)
        peak_indices = self._find_peaks(transform_result.magnitude)
        dominant_freqs = transform_result.frequencies[peak_indices]
        
        # Calculate power spectral density
        psd = np.abs(transform_result.spectrum) ** 2
        
        # Calculate signal energy in frequency domain
        signal_energy = np.sum(psd)
        
        return {
            'parameters': params,
            'transform': transform_result,
            'dominant_frequencies': dominant_freqs,
            'power_spectral_density': psd,
            'signal_energy': signal_energy
        }
    
    def _find_peaks(self, magnitude: np.ndarray, threshold: float = 0.1) -> List[int]:
        """Find indices of peaks in magnitude spectrum"""
        # Simple peak finding: compare with neighbors
        peaks = []
        for i in range(1, len(magnitude) - 1):
            if (magnitude[i] > magnitude[i-1] and 
                magnitude[i] > magnitude[i+1] and 
                magnitude[i] > threshold * np.max(magnitude)):
                peaks.append(i)
        return peaks

def example_usage():
    """Demonstrate usage with example signals"""
    # Create test signal: sum of two sinusoids
    sample_rate = 1000  # Hz
    duration = 1.0      # seconds
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # 10 Hz and 50 Hz components
    signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
    
    # Initialize transformer
    ft = FourierTransform(sample_rate)
    
    # Analyze signal
    analysis = ft.analyze_signal(signal)
    
    # Forward transform
    result = ft.forward(signal)
    
    # Inverse transform to reconstruct signal
    reconstructed = ft.inverse(result.spectrum, len(signal))
    
    # Verify reconstruction error
    error = np.mean(np.abs(signal - reconstructed))
    print(f"Reconstruction error: {error:.2e}")
    
    return analysis, reconstructed

if __name__ == "__main__":
    analysis, reconstructed = example_usage()





