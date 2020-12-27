// Save record
{% if record_id and type == 'edit-record' %}
/*
// Update a legacy record
(function($) {
  $('#add-record').on('click', function(e) {
      e.preventDefault();

      // Get the values from the form
      var field_values = [];
      $(".record-field").each(function(){
       var key = $(this).attr('id').replace("field_","");
       var val = $(this).val();
       item = {}
       item [key] = val;
       field_values.push(item);
      });

      $.ajax({
        type: "POST",
        dataType: 'json',
        url: "{% url 'update_record' organization_pk=organization.pk app_pk=app.pk list_pk=list.pk record_pk=record_id %}",
          data: {
              'field_values': JSON.stringify(field_values),
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {

              console.log(data)

          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      });
  });
}(jQuery)); */

{% else %}

// This is a new record
/*
(function($) {
  $('#add-record').on('click', function(e) {
      e.preventDefault();

      // Get the values from the form
      var field_values = [];
      $(".record-field").each(function(){
       var key = $(this).attr('id').replace("field_","");
       var val = $(this).val();
       item = {}
       item [key] = val;
       field_values.push(item);
      });

      $.ajax({
        type: "POST",
        dataType: 'json',
        url: "{% url 'save_record' organization_pk=organization.pk app_pk=app.pk list_pk=list.pk %}",
          data: {
              'field_values': JSON.stringify(field_values),
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {

              console.log(data)

          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      });
  });
}(jQuery)); */
{% endif %}
