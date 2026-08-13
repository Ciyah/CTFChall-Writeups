#!/usr/bin/env python3

from collections import Counter

import numpy as np
from scipy.io import wavfile


N = 1_000_000
T = 0.0001


def main() -> None:
    _, waveform = wavfile.read("Noisy/encrypted.wav")

    # A sine with amplitude A has magnitude A after this normalization.
    spectrum = 2 * np.abs(np.fft.rfft(waveform)) / len(waveform)
    peak_bins = np.flatnonzero(spectrum > 0.5)

    # encrypt.py uses amplitude i + 1, which directly reveals each position.
    frequencies_by_position = {
        round(spectrum[bin_index]): bin_index / (N * T)
        for bin_index in peak_bins
    }

    counts: Counter[str] = Counter()
    flag = []

    for position in range(1, max(frequencies_by_position) + 1):
        frequency = frequencies_by_position[position]
        candidates = []

        for codepoint in range(32, 127):
            character = chr(codepoint)
            expected = 0.1 * codepoint * 4 ** counts[character]
            if np.isclose(frequency, expected, atol=1e-8):
                candidates.append(character)

        if len(candidates) != 1:
            raise ValueError(
                f"position {position}: expected one candidate, got {candidates}"
            )

        character = candidates[0]
        flag.append(character)
        counts[character] += 1

    print("".join(flag))


if __name__ == "__main__":
    main()
