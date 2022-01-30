from math import log10
from scipy.stats import chisquare


# As long as we need only 10 numbers
# calculating them with pure python will not have a noticeable influence on application performance.
def generate_benford_distribution() -> dict:
    return {i: log10((i + 1) / i) for i in range(1, 10)}


# Chi square may be not the best choice for testing Benford distribution.
# https://www.mdpi.com/2571-905X/4/2/27
class DistributionComparator:
    def __init__(self, observedCounts: dict, expected_distribution: dict, significance_level: float = 0.01):

        self.totalObservation = sum(observedCounts.values())
        self.smallestObservation = min([observedCounts[key] for key in expected_distribution])

        self.significance_level = significance_level

        expected_counts = {key: expected_distribution[key] * self.totalObservation for key in expected_distribution}

        self.xValues = list(sorted(expected_distribution.keys()))
        self.yObservedList = [observedCounts[i] for i in self.xValues]
        self.yExpectedList = [expected_counts[i] for i in self.xValues]

    def test_is_valid(self):
        # Thresholds taken directly from scipy documentation
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
        if self.totalObservation < 14:
            return False, f"To little observations {self.totalObservation}"

        if self.smallestObservation < 5:
            return False, f"To little observations for one or more groups: {self.smallestObservation}"

        return True, "tests ok"

    def compare(self):
        chi_square, p = chisquare(f_obs=self.yObservedList, f_exp=self.yExpectedList)

        return chi_square, p, p > self.significance_level
