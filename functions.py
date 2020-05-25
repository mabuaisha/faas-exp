COMMON = {
    'parallel': {
        'autoscaling': [
            {
                'user_5': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
            {
                'user_10': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
            {
                'user_20': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
            {
                'user_50': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            }

        ],
        'noautoscaling': [
            {
                'replica1': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
            {
                'replica10': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
            {
                'replica20': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },

        ]
    },
    'sequential': {
        'noautoscaling': [
            {
                'replica1': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
            {
                'replica10': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
            {
                'replica20': [
                    {'1': 'results/statistics.json'},
                    {'2': 'results/statistics.json'},
                    {'3': 'results/statistics.json'},
                    {'4': 'results/statistics.json'},
                    {'5': 'results/statistics.json'},
                    {'6': 'results/statistics.json'},
                ]
            },
        ]
    }
}

COMMON_WARM = [
    {
        '1': [
            {
                'warm_0': 'results/statistics.json',
            },
            {
                'cold_0': 'results/statistics.json',
            },
            {
                'warm_1': 'results/statistics.json',
            },
            {
                'cold_1': 'results/statistics.json',
            },
            {
                'warm_2': 'results/statistics.json',
            },
            {
                'cold_2': 'results/statistics.json',
            },
        ]
    },
    {
        '2': [
            {
                'warm_0': 'results/statistics.json',
            },
            {
                'cold_0': 'results/statistics.json',
            },
            {
                'warm_1': 'results/statistics.json',
            },
            {
                'cold_1': 'results/statistics.json',
            },
            {
                'warm_2': 'results/statistics.json',
            },
            {
                'cold_2': 'results/statistics.json',
            },
        ]
    },
    {
        '3': [
            {
                'warm_0': 'results/statistics.json',
            },
            {
                'cold_0': 'results/statistics.json',
            },
            {
                'warm_1': 'results/statistics.json',
            },
            {
                'cold_1': 'results/statistics.json',
            },
            {
                'warm_2': 'results/statistics.json',
            },
            {
                'cold_2': 'results/statistics.json',
            },
        ]
    },
    {
        '4': [
            {
                'warm_0': 'results/statistics.json',
            },
            {
                'cold_0': 'results/statistics.json',
            },
            {
                'warm_1': 'results/statistics.json',
            },
            {
                'cold_1': 'results/statistics.json',
            },
            {
                'warm_2': 'results/statistics.json',
            },
            {
                'cold_2': 'results/statistics.json',
            },
        ]
    },
    {
        '5': [
            {
                'warm_0': 'results/statistics.json',
            },
            {
                'cold_0': 'results/statistics.json',
            },
            {
                'warm_1': 'results/statistics.json',
            },
            {
                'cold_1': 'results/statistics.json',
            },
            {
                'warm_2': 'results/statistics.json',
            },
            {
                'cold_2': 'results/statistics.json',
            },
        ]
    },
    {
        '6': [
            {
                'warm_0': 'results/statistics.json',
            },
            {
                'cold_0': 'results/statistics.json',
            },
            {
                'warm_1': 'results/statistics.json',
            },
            {
                'cold_1': 'results/statistics.json',
            },
            {
                'warm_2': 'results/statistics.json',
            },
            {
                'cold_2': 'results/statistics.json',
            },
        ]
    },
]

WARM = {
    'parallel': {
        'autoscaling': [
            {
                'user_5': COMMON_WARM
            },
            {
                'user_10': COMMON_WARM
            },
            {
                'user_20': COMMON_WARM
            },
            {
                'user_50': COMMON_WARM
            }

        ],
        'noautoscaling': [
            {
                'replica1': COMMON_WARM
            },
            {
                'replica10': COMMON_WARM
            },
            {
                'replica20': COMMON_WARM
            },

        ]
    },
    'sequential': {
        'noautoscaling': [
            {
                'replica1': COMMON_WARM
            },
            {
                'replica10': COMMON_WARM
            },
            {
                'replica20': COMMON_WARM
            },
        ]
    }
}

FUNCTIONS = \
    {
        'consumerfunction': COMMON,
        'ftpfunction': COMMON,
        'gofunction': COMMON,
        'iofunction': COMMON,
        'javafunction': COMMON,
        'matrixfunction': COMMON,
        'nodefunction': COMMON,
        'pythonfunction': COMMON,
        'warmfunction': WARM
    }
