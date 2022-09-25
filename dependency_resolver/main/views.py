from sys import path_hooks
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,Http404
import json, os
from .powershell_script_utility import PSScriptRunnerUtility
from .models import VirtualEnvironmentPath
from rest_framework.decorators import api_view, permission_classes
import requests

powershell_script_path = "C:\\Users\\ayushganguli\\Desktop\\FinalHackathonProject\\run_python_script.ps1"#this is a default path, don't use always
powershell_script_output_path = "C:\\Users\\ayushganguli\\Desktop\\FinalHackathonProject\\PythonScripts\\python_scripts_output.json"
#python_scripts_path = "C:\\Users\\ayushganguli\\Desktop\\FinalHackathonProject\\PythonScripts"

def home(request):
    return render(request, 'dependency_list.html')

def dependency_resolver_page(request):
    if 'python_scripts_path' in request.session:
        venv_scripts_path = request.session['python_scripts_path']
    else:
        return JsonResponse({'error': True,'exception': "No virtual environemnt path found"})
    print(venv_scripts_path)
    PSScriptRunnerUtility.run_ftp_upload_powershell_script(powershell_script_path,venv_scripts_path,"get_all_installed_dependency.py")
    my_file = open(powershell_script_output_path)
    all_packages_json = json.load(my_file)
    return render(request,'dependency_resolver.html',{'all_packages_json': all_packages_json})

def get_all_dependency_api(request):
    if 'python_scripts_path' in request.session:
        venv_scripts_path = request.session['python_scripts_path']
    else:
        return JsonResponse({'error': True,'exception': "No virtual environemnt path found"})
    print(venv_scripts_path)
    PSScriptRunnerUtility.run_ftp_upload_powershell_script(powershell_script_path,venv_scripts_path,"get_all_installed_dependency.py")
    my_file = open(powershell_script_output_path)
    json_data = json.load(my_file)
    all_venv_path = VirtualEnvironmentPath.objects.all()
    return JsonResponse(json_data)

@api_view(['GET','POST'])
def save_path_api(request):
    print(request.data)
    path_value = request.data['curr_python_script_path'].strip().rstrip()
    if len(path_value) == 0:
        return JsonResponse({'message': "Empty Path Given"})
    elif os.path.exists(path_value) is False and path_value != "global":
        return JsonResponse({'message': "Path does not exist in your system"})
    request.session['python_scripts_path'] = path_value
    if VirtualEnvironmentPath.objects.filter(path_value = path_value).exists() is False:
        new_venv_path_obj = VirtualEnvironmentPath(path_value = path_value)
        new_venv_path_obj.save()
        return JsonResponse({'message': "Path Saved and added to DataBase"})
    return JsonResponse({'message': "Path Saved"})

@api_view(['GET','POST'])
def get_package_requirements_api(request):
    parent_package_name = request.data['parent_package_name']
    if 'python_scripts_path' in request.session:
        venv_scripts_path = request.session['python_scripts_path']
    else:
        return JsonResponse({'error': True,'exception': "No virtual environemnt path found"})
    PSScriptRunnerUtility.run_ftp_upload_powershell_script(powershell_script_path,venv_scripts_path,"get_child_dependency.py" ,parent_package_name)
    my_file = open(powershell_script_output_path)
    json_data = json.load(my_file)
    return JsonResponse(json_data)

@api_view(['GET','POST'])
def resolve_dependencies_api(request):
    print(request.data)
    if 'python_scripts_path' in request.session:
        venv_scripts_path = request.session['python_scripts_path']
    else:
        venv_scripts_path = "global"
        #return JsonResponse({'error': True,'exception': "No virtual environemnt path found"})
    package_to_check = request.data['package_to_check']
    package_list = request.data['package_list']
    PSScriptRunnerUtility.run_ftp_upload_powershell_script(powershell_script_path,venv_scripts_path,"dependency_resolver_utility_script.py" ,str(package_to_check).strip().rstrip().replace(" ",""), str(package_list).strip().rstrip().replace(" ","") )
    my_file = open(powershell_script_output_path)
    json_data = json.load(my_file)
    return JsonResponse(json_data)

# Create your views here.
