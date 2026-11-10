"""
Versioned Instrument Capability Map Lookup

For each genuine disagreement, checks whether the disagreement
is testable with instruments that exist today.

Three possible verdicts:
  - testable_now: instrument named, observable named
  - testable_under_assumption: assumption named
  - not_testable: structural reason named

The map is versioned. Old verdicts stay valid under their version.
"""


def check_testability(
    disagreement: dict,
    capability_map: list,
    map_version: str
) -> dict:
    """
    Check whether a disagreement is testable against the
    instrument capability map.

    Args:
        disagreement: dict with physical_scale and observable
        capability_map: list of instrument entries
        map_version: version string for the map

    Returns:
        dict with verdict, instrument (if testable), and reason
    """
    target_scale = disagreement.get("physical_scale")
    target_observable = disagreement.get("observable")

    # Find instruments that reach this scale and measure this observable
    matching_instruments = [
        entry for entry in capability_map
        if (
            entry.get("physical_scale") == target_scale
            and target_observable.lower() in entry.get("observable", "").lower()
        )
    ]

    if matching_instruments:
        best = matching_instruments[0]
        return {
            "verdict": "testable_now",
            "instrument": best["instrument_class"],
            "observable": best["observable"],
            "resolution": best.get("resolution"),
            "map_version": map_version
        }

    # Check for instruments at this scale with different observables
    scale_instruments = [
        entry for entry in capability_map
        if entry.get("physical_scale") == target_scale
    ]

    if scale_instruments:
        return {
            "verdict": "testable_under_assumption",
            "assumption": f"Assumes {target_observable} is measurable via proxy observable at {target_scale} scale",
            "available_instruments": [e["instrument_class"] for e in scale_instruments],
            "map_version": map_version
        }

    return {
        "verdict": "not_testable",
        "reason": f"No instrument in capability map (version {map_version}) reaches {target_scale} scale to measure {target_observable}",
        "map_version": map_version
    }
