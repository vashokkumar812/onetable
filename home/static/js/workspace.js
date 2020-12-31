/* Not using ajax for now during initial building / testing
Will improve later */

/*
// Activity page
(function($) {
  $('#dashboard').on('click', function(e) {
      e.preventDefault();

      const url = "{% url 'dashboard' organization_pk=organization.pk app_pk=app.pk %}";
      $.ajax({
          type: "GET",
          url: url,
          data: {
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {
              // append html to the posts div
              $('#main-content').html(data['html_from_view']);
          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      }).always(()=> {

        window.history.pushState({}, '', url);
      });
  });
}(jQuery));

// Tasks page
(function($) {
  $('#tasks').on('click', function(e) {
      e.preventDefault();

      const url = "{% url 'tasks' organization_pk=organization.pk app_pk=app.pk %}";
      $.ajax({
        type: "GET",
        url: url,
          data: {
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {
              // append html to the posts div
              $('#main-content').html(data['html_from_view']);
          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      }).always(() => {

        window.history.pushState({}, '', url);
      });
  });
}(jQuery));

// Notes page
(function($) {
  $('#notes').on('click', function(e) {
      e.preventDefault();

      const url = "{% url 'notes' organization_pk=organization.pk app_pk=app.pk %}";
      $.ajax({
        type: "GET",
        url: url,
          data: {
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {
              // append html to the posts div
              $('#main-content').html(data['html_from_view']);
          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      }).always(() => {

        window.history.pushState({}, '', url);
      });
  });
}(jQuery));

// Lists page
(function($) {
  $('#lists').on('click', function(e) {
      e.preventDefault();

      const url = "{% url 'lists' organization_pk=organization.pk app_pk=app.pk %}";
      $.ajax({
        type: "GET",
        url: url,
          data: {
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {
              // append html to the posts div
              $('#main-content').html(data['html_from_view']);
          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      }).always(() => {

        window.history.pushState({}, '', url);
      });
  });
}(jQuery)); */
