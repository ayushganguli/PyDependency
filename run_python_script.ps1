#args[0] is path of virtualenv
#args[1] is name_of_python_file.py
#args[2] package_name parameter for get_child_dependency, dependency_resolver_utility_script
#args[3] package_list parameter for resolve_dependencies
#changing directory to args[0]
$current_base_location = Get-Location
try{
    deactivate 
    echo "deactivated"
}
catch{
    echo "No virtual environemnt to deactivate"
}
#pip freeze
if($args[0] -ne "global"){
    cd $args[0]
    .\Scripts\activate.ps1
}
$python_scripts_path = "C:\\Users\\ayushganguli\\Desktop\\FinalHackathonProject\\PythonScripts"
cd $python_scripts_path
echo $args.Count
echo $args
if($args.Count -ge 4){
    echo "exec ge 4"
    $file_name = $args[1]
    $package_to_check = $args[2]
    $package_list = ""
    for($i = 3 ; $i -lt $args.Count; $i++){
        $package_list = $package_list +  $args[$i]
    }
    echo $file_name  $package_to_check $package_list
    Invoke-Expression "python $file_name $package_to_check $package_list"
}
elseif($args.Count -eq 3){
    echo "exec eq 3"
    $parent_library = $args[2]
    Invoke-Expression "python get_child_dependency.py $parent_library "
}
else{
    python $args[1]
}
if($args[0] -ne "global"){
    deactivate
}
Set-Location $current_base_location