import os
import sys
import time
import logging
import subprocess

import click
import requests
from jinja2 import Environment, FileSystemLoader

from config import Config

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


def _execute_command(command, cwd=None):
    subprocess_args = {
        'args': command.split(),
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'cwd': cwd
    }

    logger.debug('Running command {0}.'.format(command))

    process = subprocess.Popen(**subprocess_args)
    output, error = process.communicate()
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
        uri_path = '{path}?param={param}'.format(
            path=uri_path, param=function['api']['param'])

    endpoint = 'http://{server}:{port}/{uri_path}'.format(
        server=experiment['server'],
        port=experiment['port'],
        uri_path=uri_path
    )
    func['endpoint'] = endpoint
    return func


def _wait_function_to_ready(endpoint, http_method):
    ready = False
    while not ready:
        response = getattr(requests, http_method.lower())(endpoint)
        status_code = response.status_code
        if status_code == 404:
            logger.warning(
                'Function endpoint {0} is not ready'.format(endpoint))
            time.sleep(2)
            continue
        elif status_code == 200:
            ready = True
            logger.info(
                'Function endpoint {0} is ready'.format(endpoint))
            break
        else:
            raise Exception(
                'Function {0} return'
                ' status code {1}'.format(
                    endpoint, status_code)
            )

    return ready


def _generate_jmeter_properties_file(function, number_of_users):
    template_path = os.path.join(
        JMETER_DIR, 'properties/config.properties.j2'
    )
    experiment = _get_experiment_config()
    number_of_requesrs = experiment['number_of_requests']
    context = {
        'number_of_users': number_of_users,
        'loop_count': int(number_of_requesrs/number_of_users),
        'server': experiment['server'],
        'port': experiment['port'],
        'http_method': function['api']['http_method'],
        'path': function['api']['uri']
    }

    if function['api'].get('param'):
        context['path'] = '{path}?param={param}'.format(
            path=context['path'], param=function['api']['param'])

    if function.get('data'):
        context['data'] = function['data']

    template_name = template_path.rsplit('/', 1)[1]
    template_path = template_path.rsplit('/', 1)[0]
    env = Environment(
        autoescape=False,
        trim_blocks=False,
        loader=FileSystemLoader(template_path)
    )
    content = env.get_template(template_name).render(context)
    prop_file = os.path.join(JMETER_DIR, 'properties/config.properties')
    with open(prop_file, 'w') as f:
        f.write(content)

    return prop_file


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
    command = 'echo Remove function {}'.format(name)
    logger.info(command)
    output = _execute_command(command)
    if not output:
        raise Exception(
            'Error when trying to remove function {0}'.format(name)
        )
    logger.info('Remove function {0} successfully'.format(name))


def _run_load_test(properties_path, result_path):
    result_path = os.path.join(result_path, 'results')
    summary_result = os.path.join(os.path.dirname(result_path), 'summary.jtl')
    jmx_path = os.path.join(JMETER_DIR, 'jmx/faas.jmx')
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
    _deploy_function(function['yaml_path'], env=function.get('env'))
    endpoint = _get_function_endpoint(function)
    _wait_function_to_ready(endpoint['endpoint'], endpoint['http_method'])

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
            _run_load_test(prop_file, run_path)

    _remove_function(function_name)
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
            env=function.get('env'))
        endpoint = _get_function_endpoint(function)
        _wait_function_to_ready(endpoint['endpoint'], endpoint['http_method'])
        prop_file = _generate_jmeter_properties_file(function, number_of_users)
        # Wait for replica to init
        time.sleep(10)
        logger.info('Testing with replica: {}'.format(replica))
        for run_number in range(1, number_of_runs + 1):
            logger.info('Testing run # {}'.format(run_number))
            run_path = os.path.join(replica_path, str(run_number))
            _creat_dir(run_path)
            _run_load_test(prop_file, run_path)

        _remove_function(function_name)
        _clean_properties_file()


def _execute_sequential(function_dir, function):
    logger.info('*************** Start sequential test cases ***************')
    sequential_path = os.path.join(function_dir, 'sequential')
    _creat_dir(sequential_path)

    _execute_with_auto_scaling(
        sequential_path,
        function,
        'sequential',
        number_of_users=[1]
    )

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


def _execute_function(function, result_dir):
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
    for func in functions:
        _execute_function(func, result_dir)


@click.group()
def main():
    pass


@click.command()
def validate():
    pass


@click.command()
def clean():
    pass


@click.command()
@click.option('-c', '--config-file', required=True,
              help='This command to start running test cases')
def run(config_file):
    config.load_config(config_file)
    execute_experiment()


main.add_command(run)
main.add_command(clean)
main.add_command(validate)
