// Get dashboard page 1
(function($) {
  $('#activity').on('click', function(e) {
      e.preventDefault();
      $.ajax({
          type: 'post',
          url: '/ajax/activity/',
          data: {
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {
              // append html to the posts div
              $('#page-content').html(data.html);
          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      });
  });
}(jQuery));

// Get dashboard page 2
(function($) {
  $('#tasks').on('click', function(e) {
      e.preventDefault();
      $.ajax({
          type: 'post',
          url: '/ajax/tasks/',
          data: {
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {
              // append html to the posts div
              $('#page-content').html(data.html);
          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      });
  });
}(jQuery));

// Get dashboard page 3
(function($) {
  $('#create_list').on('click', function(e) {
      e.preventDefault();
      $.ajax({
          type: 'post',
          url: '/ajax/create-list/',
          data: {
              'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
          },
          success: function(data) {
              // append html to the posts div
              $('#page-content').html(data.html);
          },
          error: function(xhr, status, error) {
              // shit happens friends!
          }
      });
  });
}(jQuery));
