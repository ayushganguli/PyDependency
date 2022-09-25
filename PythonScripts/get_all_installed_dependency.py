import pkg_resources
import json

def get_all_installed_packages():
    return  [(d.project_name.rstrip().strip().lower(), d.version.rstrip().strip().lower()) for d in pkg_resources.working_set]

curr_exception = None
error_in_execution = False

try:
    all_installed_packages_arr = get_all_installed_packages()
    dependency_table_arr = []
    for curr_dependency in all_installed_packages_arr:
        dependency_table_arr.append({'name' :  curr_dependency[0] , 'version': curr_dependency[1],'required': "", 'resolved': True  })
    dependency_table_arr.sort(key = lambda x : x['name'])
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'all_packages' : dependency_table_arr,'error': error_in_execution,'exception': curr_exception}
        json.dump(my_data, f)
except Exception as exe:
    curr_exception = str(exe)
    error_in_execution = True
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'error': error_in_execution,'exception': curr_exception}
        json.dump(my_data, f)