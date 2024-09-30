import logging
import os
from pathlib import Path

import yaml


class YamlConfig:
    def __init__(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        config_path = Path(current_path) / ".." / "resources" / "jira_ticket_prompt.yaml"
        os.path.exists(config_path)
        self._config_path = config_path


    def get_config(self):
        logging.debug(f"read yaml configuration {self._config_path.resolve()}")
        with open(self._config_path) as config:
            return yaml.safe_load(config)
