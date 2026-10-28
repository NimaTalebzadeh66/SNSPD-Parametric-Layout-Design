"""Generate a reference meander and a deliberately invalid spacing test.

Use with drc/snspd_spacing_diagnostic.lydrc in KLayout.
"""
from pathlib import Path
import gdsfactory as gf

OUT = Path(__file__).resolve().parent.parent / "gds"


def make_detector(pitch_um: float, filename: str) -> None:
    detector = gf.components.snspd(
        wire_width=0.10,
        wire_pitch=pitch_um,
        size=(10, 8),
        turn_ratio=4,
        terminals_same_side=False,
        layer=(2, 0),
    )
    detector.write_gds(str(OUT / filename))
    print(f"Saved {filename}: straight-section gap = {(pitch_um-0.10)*1000:.0f} nm")


if __name__ == "__main__":
    gf.gpdk.PDK.activate()
    OUT.mkdir(parents=True, exist_ok=True)
    make_detector(0.25, "snspd_reference_250nm_pitch.gds")  # 150 nm gap
    make_detector(0.16, "snspd_spacing_test_160nm_pitch.gds")  # 60 nm gap
