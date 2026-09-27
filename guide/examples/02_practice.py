"""Measure mono PCM16; default data stays in memory and produces no audio file."""
import argparse
import math
import struct
import wave


def pcm16_samples(path):
    with wave.open(str(path), "rb") as wav:
        if (wav.getnchannels() != 1 or wav.getsampwidth() != 2
                or wav.getcomptype() != "NONE"):
            raise ValueError("Only uncompressed mono PCM16 WAV is supported")
        rate = wav.getframerate()
        expected = wav.getnframes()
        count = 0
        while raw := wav.readframes(4096):
            if len(raw) % 2:
                raise ValueError("Truncated PCM16 sample")
            for (value,) in struct.iter_unpack("<h", raw):
                count += 1
                yield value, rate
        if count != expected:
            raise ValueError("Truncated WAV payload")


def measure(samples):
    count, square_sum, peak, clipped = 0, 0.0, 0.0, 0
    rate = None
    for value, sample_rate in samples:
        if not isinstance(sample_rate, int) or sample_rate <= 0:
            raise ValueError("Sample rate must be a positive integer")
        if not isinstance(value, int) or not -32768 <= value <= 32767:
            raise ValueError("Sample is outside signed PCM16")
        if rate is not None and rate != sample_rate:
            raise ValueError("Sample rate changed within recording")
        rate = sample_rate
        norm = value / 32768.0
        count += 1
        square_sum += norm * norm
        peak = max(peak, abs(norm))
        clipped += value in {-32768, 32767}
    if not count:
        raise ValueError("No samples")
    return {
        "duration_seconds": count / rate,
        "peak": peak,
        "rms": math.sqrt(square_sum / count),
        "full_scale_fraction": clipped / count,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wav")
    args = parser.parse_args()
    # Alternating values teach numerical measurement, not speech synthesis.
    samples = pcm16_samples(args.wav) if args.wav else (
        (8192 if i % 2 else -8192, 16000) for i in range(16000)
    )
    try:
        for name, value in measure(samples).items():
            print(f"{name}={value:.4f}")
    except (OSError, ValueError, wave.Error, EOFError) as exc:
        parser.exit(1, f"Measurement failed: {exc}\n")


if __name__ == "__main__":
    main()
