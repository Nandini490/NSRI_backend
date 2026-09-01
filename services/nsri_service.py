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

    def calculate_rdt(
        self,
        hrv_normalized: Optional[float],
        resting_hr_normalized: Optional[float],
        external_stress_score: Optional[float] = None
    ) -> Optional[float]:
        """
        Recovery Debt Index (RDT).

        RDT = [0.3 * (1 - HRV component)
               + 0.2 * Resting HR component
               + 0.5 * External stress component] * 100

        Components:
        - HRV (0-1): Heart rate variability normalized. Low HRV = high recovery debt.
        - Resting HR (0-1): Resting heart rate normalized. High resting HR = high recovery debt.
        - External stress (0-100): Environmental stressors (weather, AQI, alerts, etc).
          If not provided, defaults to 0 (no external stress).

        Higher RDT indicates greater recovery debt/need for recovery.
        """

        if hrv_normalized is None or resting_hr_normalized is None:
            return None

        # Default external stress to 0 if not provided
        ext_stress = external_stress_score if external_stress_score is not None else 0.0

        rdt = (
            0.3 * (1 - hrv_normalized)
            + 0.2 * resting_hr_normalized
            + 0.5 * (ext_stress / 100)
        ) * 100

        return round(rdt, 2)

    def calculate_nsri(
        self,
        sai: Optional[float],
        pri: Optional[float],
        rdt: Optional[float]
    ) -> Optional[float]:
        """
        Nervous System Response Index (NSRI) - Final Score.

        NSRI = 0.4 * SAI + 0.3 * (100 - PRI) + 0.3 * RDT

        All inputs should be on 0-100 scale.
        - SAI: Higher = more stress
        - PRI: Higher = better recovery
        - RDT: Higher = greater recovery debt

        NSRI represents overall nervous-system strain/risk.
        Higher NSRI indicates greater overall stress burden and recovery needs.
        """

        # All three components are required for final NSRI
        if sai is None or pri is None or rdt is None:
            return None

        nsri = (
            0.4 * sai
            + 0.3 * (100 - pri)
            + 0.3 * rdt
        )

        # Enforce strict 0-100 scale
        nsri = max(0.0, min(100.0, nsri))

        return round(nsri, 2)


nsri_service = NSRIService()

