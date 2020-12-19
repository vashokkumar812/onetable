const list = document.getElementById('list')
const addField = document.getElementById('addField')

// Clear out local storage
const fields = []
localStorage.setItem('fields', JSON.stringify(fields))

function addFieldElement(field) {

  // Save item to local storage
  let fields = JSON.parse(localStorage.getItem('fields'))
  fields.push(field)
  fields = setFieldListOrder(fields)
  localStorage.setItem('fields', JSON.stringify(fields))
  console.log(JSON.parse(localStorage.getItem('fields')))

  // Get new item attrs
  fieldId = field['id'];
  fieldLabel = field['fieldLabel'];
  fieldType = field['fieldType'];
  required = field['required'];
  visible = field['visible'];
  displayType = displayField(fieldType);
  displayRequired = displayBoolean(required)
  displayVisible = displayBoolean(visible)

  // Adding new html element
  let fieldItem = '<div class="card"><div class="card-header"><div class="col-12 col-xl-auto mb-3">' + fieldLabel + '</div></div><div class="card-body"><div class="col-12 col-xl-auto mb-3"> Field Type: ' + displayType + '<div class="col-12 col-xl-auto mb-3"> Required: ' + displayRequired + '<div class="col-12 col-xl-auto mb-3"> Visible: ' + displayVisible + '</div><div class="col-12 col-xl-auto mb-3"><a class="btn btn-primary p-2 remove-field" href="" id="remove_' + fieldId + '">Remove</a></div></div></div>'

  const newElement = document.createElement('div');
  newElement.setAttribute('id', "field_" + fieldId);
  newElement.innerHTML = fieldItem;
  list.appendChild(newElement);

  // Clear form so a new field can be added
  $("#field-label").val("")
  $("#field-type").val("")
  $("#required").prop('checked', false)
  $("#visible").prop('checked', false)

}

function removeElement(elementId) {

    fieldId = elementId.replace("field_","")

    // Remove from local storage
    const currentItems = JSON.parse(localStorage.getItem('fields'))
    let afterRemoved = currentItems.filter(field => field.id !== fieldId)
    const fields = setFieldListOrder(afterRemoved)
    localStorage.setItem('fields', JSON.stringify(fields))
    console.log(JSON.parse(localStorage.getItem('fields')))

    // Remove from display
    const element = document.getElementById(elementId);
    element.parentNode.removeChild(element);

}

function makeid(length) {
   var id = '';
   var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      id += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return id;
}

function displayField(fieldType) {
   var displayType = '';
   if (fieldType == "text") {
     displayType = "Text"
   }
   if (fieldType == "long-text") {
     displayType = "Long Text"
   }
   if (fieldType == "number") {
     displayType = "Number"
   }
   if (fieldType == "decimal") {
     displayType = "Decimal"
   }
   if (fieldType == "select-one-option") {
     displayType = "Select One Option"
   }
   if (fieldType == "select-multiple-option") {
     displayType = "Select Multiple Options"
   }
   if (fieldType == "select-one-list") {
     displayType = "Select One from List"
   }
   if (fieldType == "select-multiple-list") {
     displayType = "Select Multiple from List"
   }
   return displayType;
}

function displayBoolean(boolean) {
   var displayBoolean = "No";
   if (boolean) {
     displayBoolean = "Yes"
   }
   return displayBoolean;
}

function setFieldListOrder(fields) {

  for(var i = 0; i < fields.length; i++) {
    let field = fields[i];
    if (i == 0) {
      field['primary'] = true
      field['visible'] = true
    } else {
      field['primary'] = false
    }
    field['order'] = i + 1;
  }
  localStorage.setItem('fields', JSON.stringify(fields))

  return fields

}


$(document).on('click','#add-field', function(e){

  e.preventDefault();

  var fieldLabel = $("#field-label").val()
  var fieldType = $("#field-type").val()
  var required = $("#required").prop('checked')
  var visible = $("#visible").prop('checked')

  // Check to make sure required values are set
  if(fieldLabel && fieldType){

    var fieldId = makeid(10);

    field = {}
    field['id'] = fieldId;
    field['fieldLabel'] = fieldLabel;
    field['fieldType'] = fieldType;
    field['required'] = required;
    field['visible'] = visible;
    field['order'] = null;

    addFieldElement(field)

  } else{
    alert("Please fill in all required fields")
  }

});

$(document).on('click','.remove-field', function(e){

  e.preventDefault();

  fieldId = "field_" + $(this).attr('id').replace("remove_","")
  removeElement(fieldId)

});
