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
  displayType = displayField(fieldType);
  displayRequired = displayBoolean(required)
  displayVisible = displayBoolean(visible)

  let fieldItem = formatFieldDisplayItem(fieldId, fieldLabel, displayType, displayRequired, displayVisible)
  const newElement = document.createElement('div');
  newElement.setAttribute('id', "field_" + fieldId);
  newElement.innerHTML = fieldItem;
  list.appendChild(newElement);

}

function formatFieldDisplayItem(
  fieldId,
  fieldLabel,
  displayType,
  displayRequired,
  displayVisible
) {

  // Adding new html element
  let fieldDisplayItem = '' +
  '<div class="card">' +
    '<div class="card-header">' +
      '<div class="col-12 col-xl-auto mb-3">' +
        fieldLabel +
      '</div>' +
    '</div>' +
    '<div class="card-body">' +
      '<div class="col-12 col-xl-auto mb-3"> ' +
        'Field Type: ' + displayType +
      '</div>' +
      '<div class="col-12 col-xl-auto mb-3"> ' +
        'Required: ' + displayRequired +
      '</div>' +
      '<div class="col-12 col-xl-auto mb-3"> ' +
        'Visible: ' + displayVisible +
      '</div>' +
      '<div class="col-12 col-xl-auto mb-3">' +
        '<a class="btn btn-primary p-2 remove-field" href="" id="remove_' + fieldId + '">Remove</a>' +
      '</div>' +
      '<div class="col-6 col-xl-auto mb-3">' +
        '<a class="btn btn-link move-up" href="" id="up_' + fieldId + '">Up</a>' +
      '</div>' +
      '<div class="col-6 col-xl-auto mb-3">' +
        '<a class="btn btn-link move-down" href="" id="down_' + fieldId + '">Down</a>' +
      '</div>' +
    '</div>' +
  '</div>'

  return fieldDisplayItem

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
