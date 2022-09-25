from pip._vendor import pkg_resources
import pkg_resources as pk_complete_module
import sys
import json

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

def get_child_dependency_helper(package_name):
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
    return dependency_table_arr


def dfs(curr_package,package_to_check,memo):
    if curr_package == package_to_check:
        return True
    elif curr_package in memo:
        return True
    memo.add(curr_package)
    required_packages = get_child_dependency_helper(curr_package)
    required_packages = [ i['name'] for i in required_packages ]
    for iter_required_package in required_packages:
        ans =  dfs(iter_required_package,package_to_check,memo)
        if ans is True:
            return True
    memo.remove(curr_package)
    return False

def dependency_resolver_main(package_to_check, package_list):
    package_to_check = package_to_check.rstrip().strip().lower()
    memo = set()
    for curr_package in package_list:
        dfs(curr_package,package_to_check,memo)
    return memo

try:
    print(sys.argv)
    package_to_check = sys.argv[1].rstrip().strip().lower()
    package_list = sys.argv[2].rstrip().strip().lower()
    package_list = package_list.replace("[","")
    package_list = package_list.replace("]","")
    package_list = list(package_list.split(','))
    resolved_dependendencies_set = dependency_resolver_main(package_to_check, package_list)
    dependendent_list = [i for i in package_list if i in resolved_dependendencies_set]
    out = []
    try:
        package_to_check_version = pk_complete_module.get_distribution(package_to_check).version
    except:
        package_to_check_version = "Unknown"
    for curr in dependendent_list:
        try:
            curr_version = pk_complete_module.get_distribution(curr).version
        except:
            curr_version = "Unknown"
        out.append({'name': curr, 'version': curr_version})
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'dependendent_list' : out,'package_to_check_version': package_to_check_version,'error': False,'exception' : None}
        json.dump(my_data, f)
except Exception as exe:
    curr_exception = str(exe)
    error_in_execution = True
    with open('python_scripts_output.json', 'w') as f:
        my_data = {'error': error_in_execution,'exception' : curr_exception}
        json.dump(my_data, f)        

"""
print(sys.argv)
print(package_to_check,package_list)
#six
#['django','flask','pandas','altair','celery','numpy','requests']
print(dependency_resolver_main(package_to_check, package_list),'ans')

python dependency_resolver_utility_script.py six "['django','flask','pandas','altair','celery','numpy','requests']"
"""