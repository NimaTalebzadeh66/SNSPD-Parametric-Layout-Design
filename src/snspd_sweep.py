"""Generate a full 3x3 SNSPD geometry sweep and a pre-screened variant.

Educational example only: generic PDK, arbitrary GDS layer, no fab sign-off.
Requires a compatible installed version of gdsfactory.
"""
from pathlib import Path
import gdsfactory as gf

# All dimensions are micrometres (um).
WIDTHS = (0.08, 0.10, 0.12)
PITCHES = (0.16, 0.20, 0.25)
MIN_WIDTH_NM = 90
MIN_SPACING_NM = 80
LAYER = (2, 0)  # Demo only. NOT a superconducting foundry layer map.
OUT = Path(__file__).resolve().parent.parent / "gds"


def passes_precheck(width_um: float, pitch_um: float) -> bool:
    """Simple parameter precheck; NOT a geometrical DRC replacement."""
    width_nm = round(width_um * 1000, 3)
    spacing_nm = round((pitch_um - width_um) * 1000, 3)
    return width_nm >= MIN_WIDTH_NM and spacing_nm >= MIN_SPACING_NM


def generate(filtered: bool) -> int:
    chip = gf.Component("SNSPD_SWEEP_FILTERED" if filtered else "SNSPD_SWEEP_ALL")
    included = 0
    for row, width in enumerate(WIDTHS):
        for col, pitch in enumerate(PITCHES):
            spacing_nm = round((pitch - width) * 1000, 3)
            if filtered and not passes_precheck(width, pitch):
                print(f"SKIP width={width*1000:.0f} nm, pitch={pitch*1000:.0f} nm, "
                      f"spacing={spacing_nm:g} nm")
                continue

            detector = gf.components.snspd(
                wire_width=width,
                wire_pitch=pitch,
                size=(10, 8),
                turn_ratio=4,
                terminals_same_side=False,
                layer=LAYER,
            )
            ref = chip.add_ref(detector)
            ref.move((col * 20.0, row * 20.0))
            included += 1
            print(f"ADD width={width*1000:.0f} nm, pitch={pitch*1000:.0f} nm, "
                  f"spacing={spacing_nm:g} nm")

    target = OUT / ("snspd_2d_filtered.gds" if filtered else "snspd_2d_full.gds")
    chip.write_gds(str(target))
    print(f"Saved {included} devices to {target}")
    return included


if __name__ == "__main__":
    gf.gpdk.PDK.activate()
    OUT.mkdir(parents=True, exist_ok=True)
    assert generate(filtered=False) == 9
    assert generate(filtered=True) == 4
