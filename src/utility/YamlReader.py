"""Wrapper class to help reading YAML files"""

# Usage::
#
#    >>> import YamlReader
#    >>> yaml_reader_object = YamlReader(PATH_TO_YAML_FILE)
#    >>> yaml_data = yaml_reader_object.get_data()
#
# Copyright (c) 2017 Lahiru Pathirage <http://lahiru.site>

import yaml


class YamlReader:

    """Set YAML file.
    
    :param __yaml_file: A string, path to YAML file.
    """
    def __init__(self, yaml_file):
        self.__yaml_data = []
        self.__yaml_file = yaml_file

    def get_data(self):
        # Load yaml data
        self.load()

        # Return YAML data as a list.
        return self.__yaml_data

    def load(self):
        # Open and read YAML file in read only mode
        with open(self.__yaml_file, 'r') as text_stream:
            try:
                self.__yaml_data = yaml.load(text_stream)

            except yaml.YAMLError as ex:
                print(ex.message)
                return None
