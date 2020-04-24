
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

yaml = YAML()


class Config(CommentedMap):
    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as conf:
                self.update(yaml.load(conf))
        except Exception as error:
            raise Exception(
                'Error {0} while trying'
                ' to load config {1}'.format(error, config_file)
            )
