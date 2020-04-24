import os
import logging
import subprocess

import click

from config import Config

# Prepare Config
config = Config()
# Prepare logger
logger = logging.getLogger(__name__)
# Create handlers
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
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


def _execute_sequential_with_auto_scaling(function_dir, function):
    sequential_path = os.path.join(function_dir, 'sequential')
    if not os.path.isdir(sequential_path):
        os.mkdir(sequential_path)
    number_of_runs = _get_experiment_config()['number_of_runs']
    for run_number in range(1, number_of_runs + 1):
        run_path = os.path.join(sequential_path, str(run_number))
        if not os.path.isdir(run_path):
            os.mkdir(run_path)

        #
        result_path = os.path.join(run_path, 'results')
        logger.info('The result path for run')


def _execute_sequential_without_auto_scaling(function_dir, function):
    pass


def _execute_parallel_with_auto_scaling(function_dir, function):
    pass


def _execute_parallel_without_auto_scaling(function_dir, function):
    pass


def _execute_function(function):
    function_yaml_path = _get_function_yaml_path(
        function['dir_path'], function['name']
    )
    function['yaml_path'] = function_yaml_path
    result_dir = _get_experiment_config()['result_dir']
    # This is the result directory where the result will be dumped
    function_result_path = os.path.join(result_dir, function['name'])
    # Create a directory for the result if does not exist
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)
    # Create the function if
    if not os.path.isdir(function_result_path):
        os.mkdir(function_result_path)

    # Run sequential requests with auto scaling
    _execute_sequential_with_auto_scaling(
        function_result_path, function
    )

    # Run sequential requests without auto scaling
    _execute_sequential_without_auto_scaling(
        function_result_path, function
    )

    # Run parallel requests with auto scaling
    _execute_parallel_with_auto_scaling(
        function_result_path, function
    )

    # Run parallel requests without auto scaling
    _execute_parallel_without_auto_scaling(
        function_result_path, function
    )


def execute_experiment():
    functions = config['functions']
    for func in functions:
        _execute_function(func)


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