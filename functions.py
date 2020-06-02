CASES = [
    {
        'type': 'parallel/autoscaling',
        'statistics': [
            'user_5/{index}/results/statistics_stdev.json',
            'user_10/{index}/results/statistics_stdev.json',
            'user_20/{index}/results/statistics_stdev.json',
            'user_50/{index}/results/statistics_stdev.json',
        ],
        'summaries': [
            'user_5/{index}/summary.jtl',
            'user_10/{index}/summary.jtl',
            'user_20/{index}/summary.jtl',
            'user_50/{index}/summary.jtl',
        ]
    },
    {
        'type': 'parallel/noautoscaling',
        'statistics': [
            'replica1/{index}/results/statistics_stdev.json',
            'replica10/{index}/results/statistics_stdev.json',
            'replica20/{index}/results/statistics_stdev.json',
        ],
        'summaries': [
            'replica1/{index}/summary.jtl',
            'replica10/{index}/summary.jtl',
            'replica20/{index}/summary.jtl',
        ]
    },
    {
        'type': 'sequential/noautoscaling',
        'statistics': [
            'replica1/{index}/results/statistics_stdev.json',
            'replica10/{index}/results/statistics_stdev.json',
            'replica20/{index}/results/statistics_stdev.json',
        ],
        'summaries': [
            'replica1/{index}/summary.jtl',
            'replica10/{index}/summary.jtl',
            'replica20/{index}/summary.jtl',
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
    'StdDev',
    'receivedKBytesPerSec',
    'sentKBytesPerSec'
)
