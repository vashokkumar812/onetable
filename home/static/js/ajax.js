<script>

  /*

  $(document).ready(function() {

      // process the form
      $('#add-organization').submit(function(event) {

          // Get form fields
          var name = $('input[name=name]').val();

          // Validate form fields
          if (name != "") {
            // Send in the request
            var formData = {
                'name': name,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            };

            // process the form
            $.ajax({
                type: "POST",
                url: "{% url 'add_organization' %}",
                data: formData,
                dataType: "json",
                encode: true
            }).done(function(data) {

                // On success
                $('#nameMsg').html("Success")

            }).fail(function(xhr, status, error) {
              //Ajax request failed.
              var errorMessage = xhr.status + ': ' + xhr.statusText
              alert('Error - ' + errorMessage);

            });

            return false;

         } else {

           // The user provided an empty value, show form error
          $('#nameMsg').html("Please provide an organization name")

         }

          // stop the form from submitting the normal way and refreshing the page
          event.preventDefault();

      });

  }); */

</script>
