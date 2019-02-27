from abc import ABCMeta
from core.config import Settings
from core.terraform.resources import BaseTerraformResource
from core import constants as K
import inspect
import importlib


class BaseCommand(metaclass=ABCMeta):
    """
    Base command class for all core and user based commands. One should inherit from this class to treat that as a comamnd

    Attributes:
        terraform_with_targets (boolean): Identify whether complete installation or partial installation is required
        OPTIONAL_ARGS (dict): Optional arguments
        MANDATORY_ARGS (dict): Mandatory arguments
        category_field_name (str): category field name which used used to identify the resources to be installed/destroyed
            Ex: --tags=deploy, tags is the category field name
        dry_run (boolean): This argument controls whether actual process is to be run or not
    """
    OPTIONAL_ARGS = {}
    MANDATORY_ARGS = {}
    category_field_name = K.CATEGORY_FIELD_NAME
    terraform_with_targets = False
    dry_run = False

    def __init__(self, args):
        """
        Constructor method for install

        Args:
            args (List): List of key- value pair of args supplied to the command
        """
        self.args = args
        self.resource_tags_list = [v for (k, v) in args if k == self.category_field_name]

        if self.resource_tags_list:
            self.terraform_with_targets = True

        self.dry_run = True if any([x[1] for x in args if x[0] == "dry-run"]) else self.dry_run

    def get_complete_resources(self, input_instance, need_instance=True):
        """
        This returns all the resources present in the common configurations

        Returns:
            resources_to_process (list): List of all resources
        """
        resource_keys_to_process = self.get_resource_keys_to_process(None, None)
        resources_to_process = self.get_resources_from_the_keys(resource_keys_to_process, input_instance, need_instance)

        return resources_to_process

    def get_resources_to_process(self, input_instance, need_instance=True):
        """
        This returns the resources to be processed currently. This can either be full resources or part of resources

        Returns:
            resources_to_process (list): List of resources
        """
        resource_keys_to_process = self.get_resource_keys_to_process(self.resource_tags_list, self.category_field_name)
        resources_to_process = self.get_resources_from_the_keys(resource_keys_to_process, input_instance, need_instance)

        return resources_to_process

    def get_resources_from_the_keys(self, resource_keys_to_process, input_instance, need_instance):
        """
        This returns the resources to be processed based on the key which is the filename

        Returns:
            resources_to_process (list): List of resources
        """
        resources_to_process = []
        for resource in resource_keys_to_process:
            try:
                resource = Settings.RESOURCES_FOLDER + '.' + resource
                resource_module = importlib.import_module(resource)
            except ImportError:
                print("Resource classes could not be found for module: %s" % str(resource))
                raise Exception("Resource classes could not be found for module, %s", str(resource))
            except Exception as e:
                print("Error: %s" % str(e))
                raise Exception("Error: %s" % str(e))

            for name, obj_class in inspect.getmembers(resource_module, inspect.isclass):
                if obj_class.__module__ == resource:  # To collect Resource Classes defined only in the resource file
                    if BaseTerraformResource in inspect.getmro(obj_class):
                        if need_instance:
                            resources_to_process.append(obj_class(input_instance))  # Create instance of that class
                        else:
                            resources_to_process.append(obj_class)

        return resources_to_process

    def get_resource_keys_to_process(self, resource_tags_list, category_field_name):
        """
        This returns the keys for the resources from the resource list supplied in PROCESS_RESOURCES

        Returns:
            resource_keys_to_process (list): List of resource's keys
        """
        resource_keys_to_process = []
        if resource_tags_list:
            for resource, attrs in Settings.PROCESS_RESOURCES.items():
                for attr, val in attrs.items():
                    if attr == category_field_name:
                        if any(x in val for x in resource_tags_list):
                            resource_keys_to_process.append(resource)
        else:
            resource_keys_to_process = Settings.PROCESS_RESOURCES.keys()

        return resource_keys_to_process

    def initialize_and_validate(self):
        return self.validation_class().validate()

    def check_pre_requisites(self):
        pass

    def read_input(self):
        """
        This returns the input read from the provider input class instance

        Returns:
            input_instancce (object): Provider Input instance
        """
        input_instancce = self.input_class()
        input_instancce.read_input()

        return input_instancce
