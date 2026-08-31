from typing import Optional


class NSRIService:

    def calculate_sai(
        self,
        wesad_stress_probability: Optional[float],
        mmash_stress_probability: Optional[float]
    ) -> Optional[float]:
        """
        Stress Accumulation Index (SAI).

        Calculates the average stress probability from
        the available datasets and converts it to a 0-100 scale.
        """

        probabilities = []

        if wesad_stress_probability is not None:
            probabilities.append(wesad_stress_probability)

        if mmash_stress_probability is not None:
            probabilities.append(mmash_stress_probability)

        if not probabilities:
            return None

        return round(sum(probabilities) / len(probabilities) * 100, 2)

    def calculate_pri(
        self,
        hrv_normalized: Optional[float],
        resting_hr_normalized: Optional[float]
    ) -> Optional[float]:
        """
        Physiological Recovery Index (PRI).

        PRI = 0.6 * HRV component
              + 0.4 * Resting HR component

        Higher PRI indicates better physiological recovery.
        """

        if hrv_normalized is None or resting_hr_normalized is None:
            return None

        pri = (
            0.6 * hrv_normalized
            + 0.4 * (1 - resting_hr_normalized)
        )

        return round(pri * 100, 2)


nsri_service = NSRIService()

