function createChildCollapse(event, parent_package_name,parent_child_body_group_id ){
  let parent_child_body_group_element = document.getElementsByClassName(parent_child_body_group_id)[0]
  json_input_data ={
    'method' : "POST",
    headers: {
    'Content-Type': 'application/json'
    // 'Content-Type': 'application/x-www-form-urlencoded',
  },
    'body' : JSON.stringify({"parent_package_name" : parent_package_name} )
  } 
  fetch('/get_package_requirements_api/',json_input_data)
    .then((response) => response.json())
    .then((data) => {
        console.log(data,'requirements')
        let display_value = ``
        bool_condition = (data['error'] === true || 'all_sub_packages' in data === false || data['all_sub_packages'].length === true )
        if(bool_condition === true){
          display_value = "<h5 class='text-center' style='color:white;'>No more dependencies required</h5>"
        }
        else{
        display_value = `
          ${data['all_sub_packages'].map(
                (curr_package) =>{
                  return `
                  <package-card
                  package-name="${curr_package.name}"
                  package-version="${curr_package.version}"
                  level-node =0>
                  </package-card>                   
                  `                 
                }
              ).join('\n')
            }           
        `
        }
      parent_child_body_group_element.innerHTML = display_value;

    });  
    
}   

function toggleIcon(e) {//toggle collapse + icon
  //console.log(e)
  $(e.target)
      .prev('.accordion-heading')
      .find(".more-less")
      .toggleClass('glyphicon-plus glyphicon-minus');
}
$('.accordion-group').on('hidden.bs.collapse', toggleIcon);
$('.accordion-group').on('shown.bs.collapse', toggleIcon);

function removeWhiteSpaces(string){
  return string.replaceAll(' ','').replaceAll(';','').replaceAll('>','').replaceAll('<','').replaceAll('=','').replaceAll('!','')

}

function createRandomString(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
  charactersLength));
  }
  return result;
}
class PackageCard extends HTMLElement {
    constructor() {
      super();
  
      this.package_name = "";
      this.package_version = "";
      this.element_id = ""
      this.collapse_id = ""
      this.level_node = 0
      this.child_body_group_id = ""
      this.required = ""
    }
  
    connectedCallback() {
      this.package_name = this.getAttribute("package-name");
      this.package_version = this.getAttribute("package-version");
      this.element_id = this.getAttribute('element-id');
      this.level_node = this.getAttribute('level-node');
      this.required = this.getAttribute('required')
      this.collapse_id = removeWhiteSpaces( (this.package_name) + "level" + String(this.level_node) + "id" + createRandomString(5) )
      this.child_body_group_id = removeWhiteSpaces( (this.package_name) + "level" + String(this.level_node) + "id" + createRandomString(5) + "child_body" )
      this.render();
    }
  
    render() {
      this.innerHTML = `
        <div class="accordion accordion-default">
          <div class="accordion-heading" role="tab" id="headingOne">
            <h4 class="accordion-title">
                <a role="button" data-toggle="collapse" data-parent="#accordion"  aria-expanded="true"  data-bs-toggle="collapse" data-bs-target="#${this.collapse_id}"  onclick="createChildCollapse(event, '${this.package_name}' ,'${this.child_body_group_id}' ) " >
                <i class="more-less glyphicon glyphicon-plus"></i>
                <div class="row">
                    <div class="col-3">
                        ${this.package_name}
                    </div>
                    <div class="col-2">
                        ${this.package_version}
                    </div>
                </div>
                </a>
            </h4>
          </div>
          <div id="${this.collapse_id}" class="accordion-collapse collapse" role="tabpanel" aria-labelledby="headingOne"  >
            <div class="accordion-body">
                <div class="accordion-group ${this.child_body_group_id}" id="accordion" role="tablist" aria-multiselectable="true" >

                </div>
            </div>
            <hr style="height:2px; width:50%; border-width:0; "><!--don't remove-->
          </div>
      </div>
        `;
    }
  }
  
  customElements.define("package-card", PackageCard);