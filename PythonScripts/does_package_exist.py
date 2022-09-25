import pkg_resources
import json
import sys

def get_all_installed_packages():
    dependency_set = set()
    for curr_dependency in pkg_resources.working_set:
        dependency_set.add(curr_dependency.project_name.strip().rstrip().lower())
    return  dependency_set

curr_exception = None
error_in_execution = False

try:
    all_installed_packages_set = get_all_installed_packages()
    package_exists = False
    package_name = sys.argv[1].strip().rstrip().lower()

    if package_name in all_installed_packages_set:
        package_exists = True
        try:
            package_version = pkg_resources.get_distribution(package_name).version
        except:
            package_version = ""
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'package_exists' : package_exists,'package_version': package_version,'error': False,'exception': None}
        json.dump(my_data, f)
except Exception as exe:
    curr_exception = str(exe)
    error_in_execution = True
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'error': error_in_execution,'exception': curr_exception}
        json.dump(my_data, f)    