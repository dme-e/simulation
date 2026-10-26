"""Rain state classification based on the calculated rain index."""


class StateClassifier:
    """Classify a rain index into a human-readable state.

    The thresholds are taken from the practice guide:
        I < 0.40          -> Sin lluvia
        0.40 <= I < 0.60  -> Baja posibilidad
        0.60 <= I < 0.75  -> Lluvia probable
        I >= 0.75         -> Lluvia
    """

    _THRESHOLDS = (
        (0.75, "Lluvia"),
        (0.60, "Lluvia probable"),
        (0.40, "Baja posibilidad"),
    )

    def classify(self, index: float) -> str:
        """Return the rain state for the given index."""
        for threshold, state in self._THRESHOLDS:
            if index >= threshold:
                return state
        return "Sin lluvia"
