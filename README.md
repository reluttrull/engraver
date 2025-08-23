Still in active development!

Current package at: https://test.pypi.org/project/engraver/

![engraver](https://github.com/user-attachments/assets/53b32a26-97e0-4b5e-bfea-aa7dae733cf7)
```
engraver: the basic CL sheet music engraving tool nobody asked for

Usage:
    engraver new (treble|bass) (4/4|3/4|2/4|12/8|9/8|6/8|3/8) (C|F|Bb|Eb|Ab|Db|Gb|Cb|G|D|A|E|B|F#|C#) <number_of_bars>
    engraver new
    engraver -h | --help
    engraver --version

Options:
    -h --help      Show this screen.
    --version      Show version.

Adding objects:
    Notes:
        <pitch> <duration> [.]
    Rests:
        r <duration> [.]
    Accidentals:
        (f|s|n) <pitch>

Treble clef pitches: d4|e4|f4|g4|a4|b4|c5|d5|e5|f5|g5
Bass clef pitches: f2|g2|a2|b2|c3|d3|e3|f3|g3|a3|b3
Durations: 1n|2n|4n|8n
```
