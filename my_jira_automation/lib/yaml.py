import os
from pathlib import Path

import yaml

from lib import log

logger = log.get_logger(__name__)
class YamlConfig:
    def __init__(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        config_path = Path(current_path) / ".." / "resources" / "jira_ticket_prompt.yaml"
        os.path.exists(config_path)
        self._config_path = config_path


    def get_config(self):
        """
        Read the YAML configuration from the file specified by the config path.

        :return: The loaded YAML configuration as a dictionary.
        """
        logger.debug(f"read yaml configuration {self._config_path.resolve()}")
        with open(self._config_path) as config:
            return yaml.safe_load(config)
