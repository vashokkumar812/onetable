const list = document.getElementById('list')
const addField = document.getElementById('addField')

// Clear out local storage
const fields = []
localStorage.setItem('fields', JSON.stringify(fields))

function addFieldElement(field) {

  // Get new item attrs
  fieldId = field['id'];
  fieldLabel = field['fieldLabel'];
  fieldType = field['fieldType'];
  required = field['required'];
  visible = field['visible'];

  let fieldItem = ''
  if (field['editMode']) {
    fieldItem = formatFieldEditItem(fieldId, fieldLabel, fieldType, required, visible)

  } else {
   fieldItem = formatFieldDisplayItem(fieldId, fieldLabel, fieldType, required, visible)
  }

  const newElement = document.createElement('div');
  newElement.setAttribute('id', "field_" + fieldId);
  newElement.innerHTML = fieldItem;
  list.appendChild(newElement);

}

function formatFieldDisplayItem(
  fieldId,
  fieldLabel,
  fieldType,
  required,
  visible,
) {

  displayType = displayField(fieldType);
  displayRequired = displayBoolean(required)
  displayVisible = displayBoolean(visible)

  let fieldDisplayItem = '<div class="card card-icon card card-header-actions lift lift-sm h-100 mb-2">' +
      '<div class="row no-gutters">' +
          '<div class="col-auto card-icon-aside bg-primary"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-layers mr-1 text-white-50"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg></div>' +
          '<div class="col">' +
            '<div class="card-header bg-white">' +
                fieldLabel +
                '<div>' +
                  '<button class="btn btn-link move-up" id="up_' + fieldId + '">Move up</button>' +
                  '<button class="btn btn-link move-down" id="down_' + fieldId + '">Move down</button>' +
                '</div>' +
                '<div class="dropdown no-caret">' +
                    '<button class="btn btn-link" id="dropdownMenuButton" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Settings</button>' +
                    '<div class="dropdown-menu dropdown-menu-right animated--fade-in-up" aria-labelledby="dropdownMenuButton">' +
                        '<a class="dropdown-item edit-field" id="edit_' + fieldId + '" href="#">' +
                          '<div class="dropdown-item-icon"><i class="text-gray-500" data-feather="edit"></i></div>' +
                          'Edit' +
                        '</a>' +
                        '<a class="dropdown-item remove-field" id="remove_' + fieldId + '" href="#">' +
                          '<div class="dropdown-item-icon"><i class="text-gray-500" data-feather="delete"></i></div>' +
                          'Delete' +
                        '</a>' +
                    '</div>' +
                '</div>' +
            '</div>' +
              '<div class="card-body py-2">' +
                  '<p>Field Type: '+ displayType +'</p>' +
                  '<p>Required: '+ displayRequired +'</p>' +
                  '<p>Visible: '+ displayVisible +'</p>' +
              '</div>' +
          '</div>' +
      '</div>' +
    '</div>' +
  '</div>';

  return fieldDisplayItem

}

function formatFieldEditItem(
  fieldId,
  fieldLabel,
  fieldType,
  required,
  visible,
) {

  displayType = displayField(fieldType);
  displayRequired = displayBoolean(required)
  displayVisible = displayBoolean(visible)

  // Building the new HTML element
  let fieldEditItem = '' +
  '<div class="card edit-field">' +
    '<div class="card-body">' +
      '<form>' +
        '<div class="row">' +
          '<div class="col-lg-8">' +
            '<div class="form-group">' +
              '<label for="field-label-' + fieldId + '">Field Label</label>' +
              '<input class="form-control" id="field-label-' + fieldId + '" value="' + fieldLabel + '" type="text" placeholder="Field label">' +
            '</div>' +
          '</div>' +
          '<div class="col-lg-4">' +
            '<div class="form-group">' +
                '<label for="field-type-' + fieldId + '">Field type</label>' +
                '<select class="form-control" id="field-type-' + fieldId + '" placeholder="Select option">' +
                    '<option value="" disabled hidden>Choose here</option>' +
                    '<option value="text">Text</option>' +
                    '<option value="long-text">Long Text</option>' +
                    '<option value="number">Number</option>' +
                    '<option value="decimal">Decimal</option>' +
                    '<option value="select-one-option">Select One Option</option>' +
                    '<option value="select-multiple-option">Select Multiple Options</option>' +
                    '<option value="select-one-list">Select One List</option>' +
                    '<option value="select-multiple-lists">Select Multiple Lists</option>' +
                '</select>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="row">' +
          '<div class="col-lg-12">' +
            '<div class="custom-control custom-checkbox custom-control-solid">' +
              '<input class="custom-control-input" id="required-' + fieldId + '" type="checkbox" name="required-' + fieldId + '">' +
              '<label class="custom-control-label" for="required-' + fieldId + '">Required</label>' +
            '</div>' +
            '<div class="custom-control custom-checkbox custom-control-solid">' +
              '<input class="custom-control-input" id="visible-' + fieldId + '" type="checkbox" name="visible-' + fieldId + '">' +
              '<label class="custom-control-label" for="visible-' + fieldId + '">Visible</label>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</form>' +
    '</div>' +
  '</div>'

  return fieldEditItem

}

function clearInputs() {
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

function moveElementUp(elementId) {

    // Get current fields and field length
    let fields = JSON.parse(localStorage.getItem('fields'))
    fieldsLength = fields.length

    // Find element in field list
    let fieldToMoveUp = getById(fields, elementId);
    const fieldToMoveUpOrder = fieldToMoveUp['order']

    if(fieldToMoveUpOrder > 1) {
      let fieldToMoveDown = fields[fieldToMoveUpOrder - 2]
      fieldToMoveUp['order'] = fieldToMoveUpOrder - 1
      fieldToMoveDown['order'] = fieldToMoveUpOrder
      fields = orderFields(fields)
      localStorage.setItem('fields', JSON.stringify(fields))
      console.log(JSON.parse(localStorage.getItem('fields')))
      refreshFieldDisplay()
    }

}

function moveElementDown(elementId) {

  // Get current fields and field length
  let fields = JSON.parse(localStorage.getItem('fields'))
  fieldsLength = fields.length

  // Find element in field list
  let fieldToMoveDown = getById(fields, elementId);
  const fieldToMoveDownOrder = fieldToMoveDown['order']

  if(fieldToMoveDownOrder < fieldsLength) {
    let fieldToMoveUp = fields[fieldToMoveDownOrder]
    fieldToMoveDown['order'] = fieldToMoveDownOrder + 1
    fieldToMoveUp['order'] = fieldToMoveDownOrder
    fields = orderFields(fields)
    localStorage.setItem('fields', JSON.stringify(fields))
    console.log(JSON.parse(localStorage.getItem('fields')))
    refreshFieldDisplay()
  }

}

function setFieldEditMode(elementId) {

  // Get current fields and field length
  let fields = JSON.parse(localStorage.getItem('fields'))

  // Find element in field list
  let fieldToEdit = getById(fields, elementId);
  fieldToEdit['editMode'] = true;

  localStorage.setItem('fields', JSON.stringify(fields))
  console.log(JSON.parse(localStorage.getItem('fields')))
  refreshFieldDisplay()

}

function refreshFieldDisplay(){

  // Clear the 'list' div
  $( "#list" ).empty();

  let fields = JSON.parse(localStorage.getItem('fields'))

  fields.forEach(function(field){
    addFieldElement(field)
  });

}

function getById(jsonObject, id) {
  return jsonObject.filter(
    function(jsonObject) {
      return (jsonObject['id'] == id);
    }
  )[0];
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
      field['required'] = true
    } else {
      field['primary'] = false
    }
    field['order'] = i + 1;
  }
  localStorage.setItem('fields', JSON.stringify(fields))

  return fields

}

function orderFields(fields) {

  sorted = fields.sort(function(a, b) {
    return a.order - b.order
  });

  return sorted

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
    field['editMode'] = false;

    // Add field to the local storage
    let fields = JSON.parse(localStorage.getItem('fields'))
    fields.push(field)
    fields = setFieldListOrder(fields)
    localStorage.setItem('fields', JSON.stringify(fields))
    console.log(JSON.parse(localStorage.getItem('fields')))

    // Add field to the display
    addFieldElement(field)

    clearInputs()

  } else{
    alert("Please fill in all required fields")
  }

});

$(document).on('click','.remove-field', function(e){

  e.preventDefault();

  fieldId = "field_" + $(this).attr('id').replace("remove_","")
  removeElement(fieldId)

});

$(document).on('click','.move-up', function(e){

  e.preventDefault();

  fieldId = $(this).attr('id').replace("up_","")
  moveElementUp(fieldId)

});

$(document).on('click','.move-down', function(e){

  e.preventDefault();

  fieldId = $(this).attr('id').replace("down_","")
  moveElementDown(fieldId)

});

$(document).on('click','.edit-field', function(e){

  e.preventDefault();

  fieldId = $(this).attr('id').replace("edit_","")
  setFieldEditMode(fieldId)

});
