CASES = [
    {
        'type': 'parallel/autoscaling',
        'description': 'Parallel Auto Scaling (Users)',
        'cases': [
            'user_5',
            'user_10',
            'user_20',
            'user_50'
        ],
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
        'description': 'Parallel None Auto Scaling (Replicas)',
        'cases': [
            'replica1',
            'replica10',
            'replica20',
        ],
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
        'description': 'Sequential None Auto Scaling (Replicas)',
        'cases': [
            'replica1',
            'replica10',
            'replica20',
        ],
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

FRAMEWORKS = (
    'k8s',
    'nomad',
    'swarm'
)
SUMMARY = (
    'framework',
    'runNumber',
    'factor',
    'factorValue'
)

MEDIAN_ACTION = 'median'
SUMMARY_ACTION = 'summary'

