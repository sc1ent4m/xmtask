import statistics
from typing import Dict
from locust import stats as stats_locust


def add_stdev_and_avg_summary(func):
    """Decorator that adds Standard deviation and Average to final stats"""
    def inner(stats):
        summary = func(stats)
        summary.append(f'Standard deviation is - '
                       f'{int(stats.total.stdev_response_time)}ms')
        summary.append(f'Average order execution is - '
                       f'{int(stats.total.avg_response_time)}ms')
        return summary
    return inner


class ModStatsEntry(stats_locust.StatsEntry):
    @property
    def stdev_response_time(self) -> int:
        if not self.response_times:
            return 0
        stdev = stdev_from_dict(self.response_times) or 0
        return stdev


def stdev_from_dict(count: Dict[int, int]) -> int:
    """
    Standard Deviation calc
    count is a dict {response_time: count}
    """
    listed = []
    for k, v in count.items():
        for i in range(0, v):
            listed.append(k)
    stdev = statistics.stdev(listed)
    return stdev


stats_locust.StatsEntry = ModStatsEntry
stats_locust.get_percentile_stats_summary = add_stdev_and_avg_summary(
    stats_locust.get_percentile_stats_summary)
