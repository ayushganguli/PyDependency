var expanded = false;
var expanded_atleast_once = false;
function showCheckboxes() {
  var checkboxes = document.getElementById("checkboxes");
  if (!expanded) {
    checkboxes.style.display = "block";
    expanded = true;
    let package_list_div = document.getElementById('checkboxes')
    if('reset_packages_get' in localStorage && JSON.parse(localStorage.getItem('reset_packages_get')) === true){
      package_list_div.innerHTML = ``
    }
    fetch('/get_all_dependency_api/')
      .then((response) => response.json())
      .then((data) => {
        //console.log(data)
        if(data['error'] === true || data['all_packages'].length == 0){
            package_list_div.innerHTML = `
            <label >
              <input type="checkbox" id="checkbox_package==allLibraryCheckBox" value="all#NA" />ALL(No Package Found)
            </label>
              `
            document.getElementById('result_package_list').disabled = true;
        }
        else{
            localStorage.setItem('all_packages', JSON.stringify(data['all_packages']))
            if('reset_packages_get' in localStorage && JSON.parse(localStorage.getItem('reset_packages_get')) === true){
              package_list_div.innerHTML = `
              <label >
              <input type="checkbox" id="checkbox_package==allLibraryCheckBox" onclick="selectAllPackageCheckbox(this)" value="all#NA" />ALL</label>
                ${data['all_packages'].map(
                  (curr_package) =>{
                    return `
                      <label >
                        <input type="checkbox" id="checkbox_package==${curr_package.name}" value="${curr_package.name}#${curr_package.version}" />${curr_package.name}
                      </label>                  
                    `                 
                  }
                ).join('\n')
              }
                `
            localStorage.setItem('reset_packages_get',false)
            }
            document.getElementById('result_package_list').disabled = false;          
        }
      });
    expanded_atleast_once = true;
  } else {
    checkboxes.style.display = "none";
    expanded = false;
  }
}
function selectAllPackageCheckbox(current_checkbox){
    let curr_all_packages_arr = JSON.parse(localStorage.getItem('all_packages'))
    for(var i = 0; i < curr_all_packages_arr.length; i ++){
        let iter_package_checkbox = document.getElementById(`checkbox_package==${curr_all_packages_arr[i].name}`)
        iter_package_checkbox.checked = current_checkbox.checked
    }
    
}