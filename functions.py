CASES = [
    {
        'type': 'parallel/autoscaling',
        'paths':
            [
                {
                    'statistic':
                        'user_5/{index}/results/statistics.json',
                    'summary': 'user_5/{index}/summary.jtl'
                },
                {
                    'statistic':
                        'user_10/{index}/results/statistics.json',
                    'summary': 'user_10/{index}/summary.jtl'
                },
                {
                    'statistic':
                        'user_20/{index}/results/statistics.json',
                    'summary': 'user_20/{index}/summary.jtl'
                },
                {
                    'statistic':
                        'user_50/{index}/results/statistics.json',
                    'summary': 'user_50/{index}/summary.jtl'
                },
            ],
    },
    {
        'type': 'parallel/noautoscaling',
        'paths':
            [
                {
                    'statistic':
                        'replica1/{index}/results/statistics.json',
                    'summary': 'replica1/{index}/summary.jtl'
                },
                {
                    'statistic':
                        'replica10/{index}/results/statistics.json',
                    'summary': 'replica10/{index}/summary.jtl'
                },
                {
                    'statistic':
                        'replica20/{index}/results/statistics.json',
                    'summary': 'replica20/{index}/summary.jtl'
                },
            ],
    },
    {
        'type': 'sequential/noautoscaling',
        'paths':
            [
                {
                    'statistic':
                        'replica1/{index}/results/statistics.json',
                    'summary': 'replica1/{index}/summary.jtl'
                },
                {
                    'statistic':
                        'replica10/{index}/results/statistics.json',
                    'summary': 'replica10/{index}/summary.jtl'
                },
                {
                    'statistic':
                        'replica20/{index}/results/statistics.json',
                    'summary': 'replica20/{index}/summary.jtl'
                }
            ],
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
    'resTime',
    'throughput',
    'errorPct',
)
