CASES = [
    {
        'type': 'parallel/autoscaling',
        'paths': [
            'user_5/{index}/results/statistics.json',
            'user_10/{index}/results/statistics.json',
            'user_20/{index}/results/statistics.json',
            'user_50/{index}/results/statistics.json',
        ]
    },
    {
        'type': 'parallel/noautoscaling',
        'paths': [
            'replica1/{index}/results/statistics.json',
            'replica10/{index}/results/statistics.json',
            'replica20/{index}/results/statistics.json',
        ]
    },
    {
        'type': 'sequential/noautoscaling',
        'paths': [
            'replica1/{index}/results/statistics.json',
            'replica10/{index}/results/statistics.json',
            'replica20/{index}/results/statistics.json',
        ]
    }
]

FUNCTIONS = (
    'gofunction',
    'javafunction',
    'nodefunction',
    'pythonfunction',
    'iofunction',
    'matrixfunction',
    'consumerfunction',
    'ftpfunction',
    'warmfunction',
)

SAMPLE = (
    'sampleCount',
    'errorCount',
    'errorPct',
    'meanResTime',
    'minResTime',
    'maxResTime',
    'pct1ResTime',
    'pct2ResTime',
    'pct3ResTime',
    'throughput',
    'receivedKBytesPerSec',
    'sentKBytesPerSec'
)
