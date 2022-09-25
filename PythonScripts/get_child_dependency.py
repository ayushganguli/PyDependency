from logging import exception
from struct import pack
from pip._vendor import pkg_resources
import pkg_resources as pk_complete_module
import sys
import json
#sys.argv[1] is package name

def getPackageDependencies(name):
    _package_name = name
    try:
        _package = pkg_resources.working_set.by_key[_package_name]
    except KeyError:
        return []
    return [str(r).strip().rstrip().lower() for r in _package.requires()]  # retrieve deps from setup.py

def split_dependency_string(curr_string):
    comparison_operators = ['>', '>=', '<','<=', '==']
    mini = sys.maxsize
    for curr_operator in comparison_operators:
        if curr_operator in curr_string:
            mini = min(mini, curr_string.index(curr_operator))
    dependency_name = curr_string[:mini].strip().rstrip().lower()
    requirements = curr_string[mini:].strip().rstrip().lower()
    return [dependency_name, requirements]

curr_exception = None
error_in_execution = False

try:
    print(sys.argv)
    print("exec child dpendency")
    package_name = sys.argv[1].strip().rstrip().lower()
    print(package_name)
    all_dependecies_raw = getPackageDependencies(package_name)
    dependency_table_arr = []

    for curr_raw_dependency in all_dependecies_raw:
        curr_dependency_name, curr_dependency_requirements = split_dependency_string(curr_raw_dependency)
        try:
            package_version = pk_complete_module.get_distribution(curr_dependency_name).version
        except:
            package_version = "Unknown"
        curr_dict = {'name' :  curr_dependency_name , 'version': package_version ,'required':curr_dependency_requirements,'resolved': True  }#wtodo: logic to check resolution
        dependency_table_arr.append(curr_dict)
    dependency_table_arr.sort(key = lambda x : x['name'])
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'all_sub_packages' : dependency_table_arr,'package_version': package_version,'error': error_in_execution,'exception' : curr_exception}
        json.dump(my_data, f)
except Exception as exe:
    curr_exception = str(exe)
    error_in_execution = True
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'error': error_in_execution,'exception' : curr_exception}
        json.dump(my_data, f)