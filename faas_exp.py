import os
import sys
import time
import datetime
import csv
import json
import logging
import subprocess
from statistics import median
from pathlib import Path

import click
import requests
import pandas as pd
from jinja2 import Environment, FileSystemLoader

from config import Config
from figures import plot_bar_figure
from functions import (
    SAMPLE,
    FUNCTIONS,
    FRAMEWORKS,
    CASES
)

# Prepare Config
config = Config()

# Prepare logger
logger = logging.getLogger(__name__)

# Set the logger level
logger.setLevel(logging.DEBUG)

# Create handlers
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Set formatter
handler.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(handler)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JMETER_DIR = os.path.join(BASE_DIR, 'jmeter')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')

CASES_DESC = {
    'replica1': '1',
    'replica10': '10',
    'replica20': '20',
    'user_5': '5',
    'user_10': '10',
    'user_20': '20',
    'user_50': '50'
}


def _is_cold_start_enabled(function):
    return True if \
        function.get('inactivity_duration') \
        and function.get('chunks_number') else False


def _execute_command(command, cwd=None, ignore_log=False):
    subprocess_args = {
        'args': command.split(),
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'cwd': cwd
    }

    if not ignore_log:
        logger.debug('Running command {0}.'.format(command))

    process = subprocess.Popen(**subprocess_args)
    output, error = process.communicate()
    if not ignore_log:
        logger.info('command: {0} '.format(repr(command)))
        logger.info('output: {0} '.format(output.decode('utf-8')))
        logger.error('error: {0} '.format(error.decode('utf-8')))
        logger.info('process.returncode: {0} '.format(process.returncode))

    if process.returncode:
        return False

    return output


def _creat_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        logger.info('Directory {} created successfully'.format(dir_path))
    else:
        logger.info('Directory {} is already existed'.format(dir_path))


def _create_nested_dir(dir_path):
    p = Path(dir_path)
    p.mkdir(parents=True, exist_ok=True)
    logger.info('Directory {} created successfully'.format(dir_path))


def _clean_properties_file():
    os.remove(os.path.join(JMETER_DIR, 'properties/config.properties'))


def _get_experiment_config():
    return config['experiment']


def _get_function_endpoint(function):
    experiment = _get_experiment_config()
    func = {
        'http_method': function['api']['http_method']
    }
    uri_path = function['api']['uri']
    if function['api'].get('param'):
        param = function['api']['param'].setdefault('min', '1')
        uri_path = '{path}?param={param}'.format(
            path=uri_path, param=param)

    endpoint = 'http://{server}:{port}/{uri_path}'.format(
        server=experiment['server'],
        port=experiment['port'],
        uri_path=uri_path
    )
    func['endpoint'] = endpoint
    return func


def _get_dependency_function(function_name):
    for function in config['functions']:
        if function['name'] == function_name:
            return function

    return None


def _wait_function_status_code(
        endpoint,
        http_method,
        stop_status,
        check_status,
        data=None):

    ready = False
    while not ready:
        attr = {}
        attr['headers'] = {'content-type': 'text/plain'}
        http_call = getattr(requests, http_method.lower())
        if data:
            attr['data'] = data
        response = http_call(endpoint, **attr)
        status_code = response.status_code
        if status_code in check_status:
            logger.info(
                'Function endpoint'
                ' {0} is on {1}'.format(
                    endpoint, status_code))
            time.sleep(5)
            continue
        elif status_code in stop_status:
            ready = True
            logger.info(
                'Function endpoint {0} is on {1}'
                ''.format(endpoint, status_code))
            break
        elif status_code == 502:
            logger.warning(
                'Bad Gateway, something went wrong try again later')
            time.sleep(10)
        else:
            raise Exception(
                'Function {0} return'
                ' status code {1}'.format(
                    endpoint, status_code)
            )

    return ready


def _generate_file_from_template(context, template_path, generated_path):
    template_name = template_path.rsplit('/', 1)[1]
    template_path = template_path.rsplit('/', 1)[0]
    env = Environment(
        autoescape=False,
        trim_blocks=False,
        loader=FileSystemLoader(template_path)
    )
    content = env.get_template(template_name).render(context)
    with open(generated_path, 'w') as f:
        f.write(content)


def _generate_jmeter_properties_file(function,
                                     number_of_users,
                                     number_of_requests=None):
    template_path = os.path.join(
        JMETER_DIR, 'properties/config.properties.j2'
    )
    experiment = _get_experiment_config()
    if not number_of_requests:
        number_of_requests = experiment['number_of_requests']
    context = {
        'number_of_users': number_of_users,
        'loop_count': int(number_of_requests/number_of_users),
        'server': experiment['server'],
        'port': experiment['port'],
        'http_method': function['api']['http_method'],
        'path': function['api']['uri']
    }

    if function.get('data'):
        context['data'] = function['data']

    prop_file = os.path.join(JMETER_DIR, 'properties/config.properties')
    _generate_file_from_template(context, template_path, prop_file)
    return prop_file


def _generate_jmeter_jmx_file(function):
    # This will passed to the jmx file if no param passed
    template_path = os.path.join(
        JMETER_DIR, 'jmx/faas.jmx.j2'
    )
    path = '${__P(path)}'
    if function['api'].get('param'):
        param = function['api']['param']
        min_param = param.setdefault('min', '1')
        max_param = param.setdefault('max', '3')
        path = '{0}?param=${{__Random({1},{2})}}' \
               ''.format(path,
                         min_param,
                         max_param)

    context = {
        'path': path
    }
    jmx_file = os.path.join(JMETER_DIR, 'jmx/faas.jmx')
    _generate_file_from_template(context, template_path, jmx_file)
    return jmx_file


def _deploy_function(function_path, labels=None, env=None):
    labels_to_add = ''
    envs_to_add = ''
    labels = labels or []
    env = env or {}
    for label in labels:
        labels_to_add += ' --label {0}'.format(label)
    command = 'faas-cli deploy -yaml {0}'.format(function_path)
    if labels_to_add:
        command = '{command}{labels}'.format(
            command=command, labels=labels_to_add
        )

    for key, value in env.items():
        envs_to_add += ' --env {key}={value}'.format(key=key, value=value)

    if envs_to_add:
        command = '{command}{envs}'.format(
            command=command, envs=envs_to_add
        )

    logger.info(command)
    output = _execute_command(command, cwd=BASE_DIR)
    if not output:
        raise Exception(
            'Error when trying to deploy function {0}'.format(function_path)
        )
    logger.info('Deploy function {0} successfully'.format(function_path))


def _remove_function(name):
    command = 'faas-cli remove {}'.format(name)
    logger.info(command)
    output = _execute_command(command)
    if not output:
        raise Exception(
            'Error when trying to remove function {0}'.format(name)
        )
    logger.info('Remove function {0} successfully'.format(name))


def _run_load_test(function, properties_path, result_path):
    result_path = os.path.join(result_path, 'results')
    summary_result = os.path.join(os.path.dirname(result_path), 'summary.jtl')
    jmx_path = _generate_jmeter_jmx_file(function)
    command = 'jmeter -n -t {jmx_path}' \
              ' -p {properties_path}' \
              ' -l {summary_result} -e -o {result_path}' \
              ''.format(jmx_path=jmx_path,
                        properties_path=properties_path,
                        summary_result=summary_result,
                        result_path=result_path)
    logger.info('Running {0}'.format(command))
    output = _execute_command(command)
    if not output:
        raise Exception(
            'Failure while trying to run {}'.format(command)
        )


def _execute_with_auto_scaling(function_dir,
                               function,
                               load_type,
                               number_of_users):

    function_name = function['name']
    logger.info(
        'Start running {0} '
        'auto scaling test cases for {1}'
        ''.format(load_type, function_name)
    )
    load_type_path = os.path.join(function_dir, 'autoscaling')
    _creat_dir(load_type_path)

    # Deploy function
    _deploy_function(function['yaml_path'], env=function.get('environment'))
    endpoint = _get_function_endpoint(function)
    _wait_function_status_code(
        endpoint['endpoint'],
        endpoint['http_method'],
        stop_status=[200],
        check_status=[404],
        data=function.get('data')
    )

    experiment = _get_experiment_config()
    number_of_runs = experiment['number_of_runs']
    for user in number_of_users:
        user_path = os.path.join(
            load_type_path, 'user_{}'.format(user)
        )
        _creat_dir(user_path)
        # Prepare jmeter configuration
        prop_file = _generate_jmeter_properties_file(function, user)
        logger.info('This is the prop file {}'.format(prop_file))
        logger.info('Testing with number of users: {}'.format(user))
        for run_number in range(1, number_of_runs + 1):
            logger.info('Testing run # {}'.format(run_number))
            run_path = os.path.join(user_path, str(run_number))
            _creat_dir(run_path)
            if _is_cold_start_enabled(function):
                chunks_number = int(function['chunks_number'])
                chunk_requests = int(
                    experiment['number_of_requests'] / chunks_number
                )
                for chunk in range(int(chunks_number / 2)):
                    for index in range(2):
                        chunk_name = "warm_{0}" \
                            if index % 2 == 0 else "cold_{0}"
                        chunk_name = chunk_name.format(chunk)
                        chunk_path = os.path.join(run_path, chunk_name)
                        _creat_dir(chunk_path)
                        # Only wait when the chunk_name is cold
                        if 'cold' in chunk_name:
                            # Wait before sending any requests
                            delay = int(function['inactivity_duration']) + 1
                            logger.info(
                                'Wait Cold start time {0}m'.format(delay)
                            )
                            time.sleep(delay * 60)
                        # Override the prop file
                        prop_file = _generate_jmeter_properties_file(
                            function,
                            user,
                            number_of_requests=chunk_requests
                        )

                        _run_load_test(function, prop_file, chunk_path)
            else:
                _run_load_test(function, prop_file, run_path)
            # Before move to the next run wait a little bit
            delay = experiment['delay_between_runs']
            logger.info(
                'Wait {0} minutes before run next run'.format(delay)
            )
            time.sleep(int(delay) * 60)

    _remove_function(function_name)
    _wait_function_status_code(
        endpoint['endpoint'],
        endpoint['http_method'],
        stop_status=[404],
        check_status=[200, 500, 502],
        data=function.get('data')
    )
    _clean_properties_file()


def _execute_without_auto_scaling(function_dir,
                                  function,
                                  load_type):
    function_name = function['name']
    logger.info(
        'Start running {0} '
        ' without auto scaling '
        'test cases for {1}'
        ''.format(load_type, function_name)
    )
    # This is for number of users we should have
    number_of_users = 1
    if load_type == 'parallel':
        number_of_users = 15
    noautoscaling_path = os.path.join(function_dir, 'noautoscaling')
    _creat_dir(noautoscaling_path)

    experiment = _get_experiment_config()
    number_of_runs = experiment['number_of_runs']
    replicas = experiment['replicas']
    # Prepare jmeter configuration
    for replica in replicas:
        replica_path = os.path.join(
            noautoscaling_path, 'replica{}'.format(replica)
        )
        _creat_dir(replica_path)
        # Deploy function
        _deploy_function(
            function['yaml_path'],
            labels=['com.openfaas.scale.max={}'.format(replica),
                    'com.openfaas.scale.min={}'.format(replica)],
            env=function.get('environment')
        )
        endpoint = _get_function_endpoint(function)
        _wait_function_status_code(
            endpoint['endpoint'],
            endpoint['http_method'],
            stop_status=[200],
            check_status=[404],
            data=function.get('data')
        )
        prop_file = _generate_jmeter_properties_file(function, number_of_users)
        # Wait for replica to init
        time.sleep(5)
        logger.info('Testing with replica: {}'.format(replica))
        for run_number in range(1, number_of_runs + 1):
            logger.info('Testing run # {}'.format(run_number))
            run_path = os.path.join(replica_path, str(run_number))
            _creat_dir(run_path)
            if _is_cold_start_enabled(function):
                chunks_number = int(function['chunks_number'])
                chunk_requests = int(
                    experiment['number_of_requests'] / chunks_number
                )
                for chunk in range(int(chunks_number / 2)):
                    for index in range(2):
                        chunk_name = "warm_{0}" \
                            if index % 2 == 0 else "cold_{0}"
                        chunk_name = chunk_name.format(chunk)
                        chunk_path = os.path.join(run_path, chunk_name)
                        _creat_dir(chunk_path)
                        # Only wait when the chunk_name is cold
                        if 'cold' in chunk_name:
                            # Wait before sending any requests
                            delay = int(function['inactivity_duration']) + 1
                            logger.info(
                                'Wait Cold start time {0}m'.format(delay)
                            )
                            time.sleep(delay * 60)
                        # Override the prop file
                        prop_file = _generate_jmeter_properties_file(
                            function,
                            number_of_users,
                            number_of_requests=chunk_requests
                        )

                        _run_load_test(function, prop_file, chunk_path)
            else:
                _run_load_test(function, prop_file, run_path)

            delay = experiment['delay_between_runs']
            logger.info('Wait {0} minutes before run next run'.format(delay))
            time.sleep(int(delay) * 60)

        _remove_function(function_name)
        # wait before checking if the function removed or not
        # Check if the function already removed or not
        _wait_function_status_code(
            endpoint['endpoint'],
            endpoint['http_method'],
            stop_status=[404],
            check_status=[200, 500, 502],
            data=function.get('data')
        )
        _clean_properties_file()


def _execute_sequential(function_dir, function):
    logger.info('*************** Start sequential test cases ***************')
    sequential_path = os.path.join(function_dir, 'sequential')
    _creat_dir(sequential_path)

    _execute_without_auto_scaling(
        sequential_path,
        function,
        'sequential'
    )
    logger.info(
        '*************** Finished sequential test cases ***************\n'
    )


def _execute_parallel(function_dir, function):
    logger.info('*************** Start parallel test cases ***************')
    parallel_path = os.path.join(function_dir, 'parallel')
    concurrency = _get_experiment_config()['concurrency']
    _creat_dir(parallel_path)

    _execute_with_auto_scaling(
        parallel_path,
        function,
        'parallel',
        number_of_users=concurrency
    )

    _execute_without_auto_scaling(
        parallel_path,
        function,
        'parallel',
    )
    logger.info(
        '*************** Finished parallel test cases ***************\n'
    )


def _execute_function(function, result_dir, func_dep=None):
    if func_dep:
        func_dep = _get_dependency_function(func_dep)
        # Deploy function
        _deploy_function(
            func_dep['yaml_path'],
            env=func_dep.get('environment')
        )
        endpoint = _get_function_endpoint(func_dep)
        _wait_function_status_code(
            endpoint['endpoint'],
            endpoint['http_method'],
            stop_status=[200],
            check_status=[404],
            data=func_dep.get('data')
        )

    logger.info('Start executing function {}'.format(function['name']))
    # This is the result directory where the result will be dumped
    function_result_path = os.path.join(result_dir, function['name'])
    # Create the function res
    _creat_dir(function_result_path)

    _execute_sequential(function_result_path, function)
    _execute_parallel(function_result_path, function)


def execute_experiment():
    result_dir = _get_experiment_config()['result_dir']
    # Create a the main directory which holds all function results
    _creat_dir(result_dir)
    functions = config['functions']
    func_dep = None
    for func in functions:
        if func.get('depends_on'):
            func_dep = func['depends_on']
        _execute_function(func, result_dir, func_dep=func_dep)
        logger.info('Wait 2 minutes before calling next function')
        time.sleep(120)


def _validate_python_version():
    if sys.version[0] != '3':
        raise Exception('Python 3 not installed !!!')


def _validate_command(command):
    try:
        _execute_command(command, ignore_log=True)
    except Exception:
        msg = 'Failed to run {0}, make sure its installed'.format(command)
        logger.error(msg)
        raise Exception(msg)


def _validate_jmeter():
    _validate_command('which jmeter')


def _validate_faas_cli():
    _validate_command('which faas-cli')


def _validate_zip():
    _validate_command('which zip')


def _validate_environment_variables(framework):
    if framework == 'k8s':
        if not os.environ.get('KUBECONFIG'):
            raise Exception('KUBECONFIG variable is not set')

    if not os.environ.get('OPENFAAS_URL'):
        raise Exception('OPENFAAS_URL variable is not set')


def _is_warm_function(function_name):
    return True if function_name == 'warmfunction' else False


def _calculate_throughput(start_date, end_date, status_codes_200):
    # the start & end date passed by are millisecond unix timestamp
    # which need to be converted
    seconds_dt1, millisecond_dt1 = divmod(int(start_date), 1000)
    seconds_dt2, millisecond_dt2 = divmod(int(end_date), 1000)

    start_date = '{0}.{1}'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(seconds_dt1)),
        millisecond_dt1
    )
    end_date = '{0}.{1}'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(seconds_dt2)),
        millisecond_dt2
    )

    start_date = datetime.datetime.strptime(
        start_date, '%Y-%m-%d %H:%M:%S.%f'
    )

    end_date = datetime.datetime.strptime(
        end_date, '%Y-%m-%d %H:%M:%S.%f'
    )
    diff = end_date - start_date
    total_time = diff.seconds + diff.microseconds / 1000000
    throughput = float(int(status_codes_200) / total_time)
    return throughput


def _aggregate_warm_data(
        path,
        dir_case_path,
        warm_cases,
        run_index,
):
    for warm_case, metrics in warm_cases.items():
        _index = '{0}/{1}'.format(run_index, warm_case)
        _item_to_add = warm_case.split('_')[0]

        _aggregate_summaries_and_statistic(
            path,
            dir_case_path,
            metrics,
            _index
        )


def _aggregate_summaries_and_statistic(
        path,
        dir_case_path,
        metrics,
        run_num
):
    # The target file
    path_to_summary = path['summary'].format(index=run_num)
    path_to_statistic = path['statistic'].format(index=run_num)
    target_summary_path = os.path.join(
        dir_case_path, path_to_summary
    )
    target_statistic_path = os.path.join(
        dir_case_path, path_to_statistic
    )

    with open(target_statistic_path) as stat_path:
        result = json.load(stat_path)
        total_result = result['Total']
        metrics['errorPct'].append(total_result['errorPct'])

    status_code_200 = 0
    start_date = ''
    end_date = ''
    if 'resTime' not in metrics:
        metrics['resTime'] = []
    with open(target_summary_path) as csv_file:
        data = pd.read_csv(csv_file)
        last_entry = len(data) - 1
        for index, entry in data.iterrows():
            if index == 0:
                start_date = int(entry['timeStamp'])
            elif index == last_entry:
                end_date = int(entry['timeStamp'])

            num = int(entry['elapsed'])
            response_code = entry['responseCode']
            if not isinstance(response_code, int):
                if response_code.isnumeric():
                    response_code = int(response_code)
            if response_code == 200:
                status_code_200 += 1
                metrics['resTime'].append(num)

    throughput = _calculate_throughput(start_date, end_date, status_code_200)
    logger.info('Number Of Response Code 200 is {0}'.format(status_code_200))
    logger.info('throughput is {0}'.format(throughput))
    logger.info('Test Case path file {0}'.format(target_summary_path))
    metrics['throughput'].append(throughput)


def _parse_test_cases_results(
        function,
        path,
        dir_case_path,
        headers,
):

    warm_cases = {
        'warm_0': {
            'errorPct': [],
            'throughput': []
        },
        'cold_0': {
            'errorPct': [],
            'throughput': []
        },
        'warm_1': {
            'errorPct': [],
            'throughput': []
        },
        'cold_1': {
            'errorPct': [],
            'throughput': []
        },
        'warm_2': {
            'errorPct': [],
            'throughput': []
        },
        'cold_2': {
            'errorPct': [],
            'throughput': []
        },
    }
    headers = headers or []
    metrics = {
        'errorPct': [],
        'throughput': []
    }
    for index in range(6):
        run_num = index + 1
        if _is_warm_function(function):
            _aggregate_warm_data(
                path,
                dir_case_path,
                warm_cases,
                run_num,
            )
        else:
            logger.info('This is the run # {}'.format(run_num))
            # Aggregate summaries and statistic
            _aggregate_summaries_and_statistic(
                path,
                dir_case_path,
                metrics,
                run_num
            )

    # Check if this is a warm function or not
    if _is_warm_function(function):
        for warm_case, warm_metrics in warm_cases.items():
            # Get the median result for response time
            median_result = median(warm_metrics['resTime'])
            # Get the median result for throughput
            logger.info(warm_case, warm_metrics['throughput'])
            throughput_result = median(warm_metrics['throughput'])
            error_pct_result = median(warm_metrics['errorPct'])
            headers.append([
                warm_case,
                median_result,
                throughput_result,
                error_pct_result
            ])
    else:
        logger.info(
            'The values of throughput are {0}'.format(metrics['throughput'])
        )
        # Get the median result for response time
        median_result = median(metrics['resTime'])
        # Get the median result for throughput
        throughput_result = median(metrics['throughput'])
        error_pct_result = median(metrics['errorPct'])

        headers.append([median_result, throughput_result, error_pct_result])


def _calculate_results(function,
                       case,
                       dir_case_path,
                       dir_to_create):
    for path in case.get('paths'):
        pre_header = ()
        if _is_warm_function(function):
            pre_header += ('startTime',)
        headers = [pre_header + SAMPLE]
        csv.register_dialect('path_dialect',
                             quoting=csv.QUOTE_NONNUMERIC,
                             skipinitialspace=True)

        _parse_test_cases_results(
            function,
            path,
            dir_case_path,
            headers,
        )
        case_id = path['summary'].split('/')[0]
        function_result = os.path.join(dir_to_create, case_id)
        with open('{0}.csv'.format(function_result), 'w') as f:
            writer = csv.writer(f, dialect='path_dialect')
            for row in headers:
                writer.writerow(row)


def _aggregate_result(source_dir,
                      destination_dir,
                      exclude_function=None):
    exclude_function = exclude_function or []
    # Create the destination directory
    _create_nested_dir(destination_dir)

    # Check if the source directory exists or not
    if not os.path.isdir(source_dir):
        raise Exception('The source directory does not exist')

    for function in FUNCTIONS:
        if function in exclude_function:
            continue
        function_dir = os.path.join(destination_dir, function)
        parallel_autoscaling = os.path.join(
            function_dir, 'parallel/autoscaling'
        )
        parallel_nonautoscaling = os.path.join(
            function_dir, 'parallel/noautoscaling'
        )
        sequential_nonautoscaling = os.path.join(
            function_dir, 'sequential/noautoscaling'
        )
        for dir_to_create in [
            parallel_autoscaling,
            parallel_nonautoscaling,
            sequential_nonautoscaling
        ]:

            # Create the directory so that we can dump the result there.
            _create_nested_dir(dir_to_create)

            for case in CASES:
                dir_list = dir_to_create.rsplit('/', 2)
                dir_type = '{0}/{1}'.format(dir_list[1], dir_list[2])
                if case.get('type') == dir_type:
                    function_src_path = os.path.join(source_dir, function)
                    dir_case_path = os.path.join(function_src_path, dir_type)
                    _calculate_results(
                        function,
                        case,
                        dir_case_path,
                        dir_to_create,
                    )


def _plot_metrics(
        k8s,
        nomad,
        swarm,
        cases,
        description,
        figure_base,
        entries_size
):
    # The size of these lists are the same
    # Since we have three metrics we are going to have 3 figures for each case
    # that represent the framework
    cases = [CASES_DESC[item] for item in cases]
    for entry_size in range(entries_size):
        response_time_k8s = []
        response_time_nomad = []
        response_time_swarm = []
        throughput_k8s = []
        throughput_nomad = []
        throughput_swarm = []
        success_pct_k8s = []
        success_pct_nomad = []
        success_pct_swarm = []
        start_time = None
        for index in range(len(k8s)):
            entry_k8s = k8s[index]
            entry_swarm = swarm[index]
            if entry_k8s[entry_size].get('startTime'):
                start_time = entry_k8s[entry_size]['startTime']

            if nomad:
                entry_nomad = nomad[index]
                # Prepare the the data for nomad
                response_time_nomad.append(entry_nomad[entry_size]['resTime'])
                throughput_nomad.append(entry_nomad[entry_size]['throughput'])
                success_pct_nomad.append(
                    100.0 - float(entry_nomad[entry_size]['errorPct'])
                )

            # Prepare the the data for k8s
            response_time_k8s.append(entry_k8s[entry_size]['resTime'])
            throughput_k8s.append(entry_k8s[entry_size]['throughput'])
            success_pct_k8s.append(
                100.0 - float(entry_k8s[entry_size]['errorPct'])
            )

            # Prepare the the data for swarm
            response_time_swarm.append(entry_swarm[entry_size]['resTime'])
            throughput_swarm.append(entry_swarm[entry_size]['throughput'])
            success_pct_swarm.append(
                100.0 - float(entry_swarm[entry_size]['errorPct'])
            )

        # Plot the figures for response time for all selected cases
        figure_path_response = \
            '{0}_{1}_response'.format(figure_base, start_time)\
                if start_time else '{0}_response'.format(figure_base)
        figure_path_throughput = \
            '{0}_{1}_throughput'.format(figure_base, start_time)\
                if start_time else '{0}_throughput'.format(figure_base)
        figure_path_success_rate = \
            '{0}_{1}_success_rate'.format(figure_base, start_time)\
                if start_time else '{0}_success_rate'.format(figure_base)
        plot_bar_figure(
            response_time_k8s,
            response_time_nomad,
            response_time_swarm,
            'Response Time (Median)',
            description,
            cases,
            figure_path_response
        )

        # Plot the figures for throughput for all selected cases
        plot_bar_figure(
            throughput_k8s,
            throughput_nomad,
            throughput_swarm,
            'Throughput (Median)',
            description,
            cases,
            figure_path_throughput
        )

        # Plot the figures for success rate for all selected cases
        plot_bar_figure(
            success_pct_k8s,
            success_pct_nomad,
            success_pct_swarm,
            'Success Rate (Median)',
            description,
            cases,
            figure_path_success_rate
        )


def _generate_figures(source_dir, destination_dir):
    # Create the destination directory
    _create_nested_dir(destination_dir)

    warm_cases = 6
    # Check if the source directory exists or not
    if not os.path.isdir(source_dir):
        raise Exception('The source directory does not exist')

    for function in FUNCTIONS:
        # We need to figure how we should generate figure for metrics
        destination_function_path = os.path.join(destination_dir, function)
        _create_nested_dir(destination_function_path)
        for case in CASES:
            # Main source case directory
            k8s = []
            nomad = []
            swarm = []
            for unit_case in case['cases']:
                for framework in FRAMEWORKS:
                    if framework == 'nomad' and function == 'warmfunction':
                        continue
                    entry_list = []
                    source_framework_dir = os.path.join(source_dir, framework)
                    source_function_dir = os.path.join(
                        source_framework_dir,
                        function
                    )
                    source_case_dir = os.path.join(
                        source_function_dir,
                        case['type']
                    )
                    source_unit_case = os.path.join(
                        source_case_dir,
                        '{0}.csv'.format(unit_case)
                    )
                    with open(source_unit_case) as csv_file:
                        data = pd.read_csv(csv_file)
                        for index, entry in data.iterrows():
                            if index < warm_cases:
                                entry_list.append(entry)
                            else:
                                break

                        if framework == 'k8s':
                            k8s.append(entry_list)
                        elif framework == 'nomad':
                            nomad.append(entry_list)
                        elif framework == 'swarm':
                            swarm.append(entry_list)

            figure_base = os.path.join(
                destination_function_path,
                case['type'].replace('/', '_')
            )
            _plot_metrics(
                k8s,
                nomad,
                swarm,
                case['cases'],
                case['description'],
                figure_base,
                len(entry_list)
            )


@click.group()
def main():
    pass


@click.command()
@click.option('-f',
              '--framework',
              required=True,
              type=click.Choice(['k8s', 'swarm', 'nomad']))
def validate(framework):
    _validate_python_version()
    _validate_jmeter()
    _validate_faas_cli()
    _validate_zip()
    _validate_environment_variables(framework)
    logger.info('Everything is valid !!!!')


@click.command()
@click.option('-s',
              '--source-dir',
              required=True)
@click.option('-d',
              '--destination-dir',
              default=FIGURES_DIR,
              required=False)
def generate_figures(source_dir, destination_dir):
    _generate_figures(source_dir, destination_dir)


@click.command()
@click.option('-s',
              '--source-dir',
              required=True)
@click.option('-d',
              '--destination-dir',
              default=RESULTS_DIR,
              required=False)
@click.option('-e',
              '--exclude-function',
              required=False,
              multiple=True)
def aggregate(source_dir, destination_dir, exclude_function):
    _aggregate_result(
        source_dir,
        destination_dir,
        exclude_function,
    )


@click.command()
@click.option('-c',
              '--config-file',
              required=True,
              help='Path to configuration file for experiment')
def run(config_file):
    config.load_config(config_file)
    execute_experiment()


main.add_command(run)
main.add_command(validate)
main.add_command(aggregate)
main.add_command(generate_figures)
