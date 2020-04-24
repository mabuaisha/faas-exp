import os
import sys
import logging
import subprocess

import click

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
FUNCTIONS_DIR = os.path.join(BASE_DIR, 'functions')
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


def _get_experiment_config():
    return config['experiment']


def _get_function_yaml_path(dir_path, name):
    # Get the orchestrator type so that we can tell where is the funciton
    # yaml file need to be loaded
    sub_dir = _get_experiment_config()['orchestrator']
    if sub_dir != 'k8s':
        sub_dir = 'common'

    function_yaml = os.path.join(
        os.path.join(dir_path, sub_dir), '{}.yml'.format(name)
    )
    return function_yaml


def _deploy_function(function_path):
    _execute_command(
        'faas-cli deploy -yaml {0}'.format(function_path),
        cwd=FUNCTIONS_DIR
    )


def _remove_function(name):
    _execute_command('faas-cli remove {0}'.format(name))


def _run_load_test(properties_path, result_path):
    jmx_path = os.path.join(JMETER_DIR, 'jmx/faas.jmx')
    command = 'jmeter -n -t {jmx_path}' \
              ' -p {properties_path}' \
              ' -l {summary_result} -e -o {result_path}' \
              ''.format(jmx_path=jmx_path,
                        properties_path=properties_path,
                        summary_result='',
                        result_path=result_path)
    _execute_command(command)


def _execute_with_auto_scaling(function_dir,
                               function,
                               load_type,
                               number_of_users):
    logger.info(
        'Start running {0} '
        'auto scaling test cases for {1}'
        ''.format(load_type, function['name'])
    )
    load_type_path = os.path.join(function_dir, 'autoscaling')
    _creat_dir(load_type_path)

    experiment = _get_experiment_config()
    number_of_runs = experiment['number_of_runs']
    for user in number_of_users:
        user_path = os.path.join(
            load_type_path, 'user_{}'.format(user)
        )
        _creat_dir(user_path)
        logger.info('Testing with number of users: {}'.format(user))
        for run_number in range(1, number_of_runs + 1):
            logger.info('Testing run # {}'.format(run_number))
            run_path = os.path.join(user_path, str(run_number))
            _creat_dir(run_path)


def _execute_without_auto_scaling(function_dir,
                                  function,
                                  load_type):
    # This is for number of users we should have
    number_of_users = 1
    if load_type == 'parallel':
        number_of_users = 15

    logger.info(
        'Start running {0} '
        ' without auto scaling '
        'test cases for {1}'
        ''.format(load_type, function['name'])
    )
    noautoscaling_path = os.path.join(function_dir, 'noautoscaling')
    _creat_dir(noautoscaling_path)

    experiment = _get_experiment_config()
    number_of_runs = experiment['number_of_runs']
    replicas = experiment['replicas']
    for replica in replicas:
        replica_path = os.path.join(
            noautoscaling_path, 'replica{}'.format(replica)
        )
        _creat_dir(replica_path)
        logger.info('Testing with replica: {}'.format(replica))
        for run_number in range(1, number_of_runs + 1):
            logger.info('Testing run # {}'.format(run_number))
            run_path = os.path.join(replica_path, str(run_number))
            _creat_dir(run_path)


def _execute_sequential(function_dir, function):
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


def _execute_parallel(function_dir, function):
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


def _execute_function(function, result_dir):
    logger.info('Start executing function {}'.format(function['name']))
    function_yaml_path = _get_function_yaml_path(
        function['dir_path'], function['name']
    )
    function['yaml_path'] = function_yaml_path
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