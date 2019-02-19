var endpointReg = /\/search\/\w+/g;

var glucky = function() {
    var url = 'https://www.google.com/search?q=' + document.getElementById('searchme').value + '&btnI';
    window.open(url, 'google');
  };

var gsearch = function(model) {
    return function(){
      var url = `/search/${model}`
      var endpoint = $("#search-form").attr("action");
      endpoint = endpoint.replace(endpointReg, url);
      console.log(endpoint);
      $("#search-form").attr("action", endpoint);
      $("#search-form").submit();
    }
  };


$(document).ready(function() {
  console.log("here");
  $("#vsm").click(gsearch('vsm'));
  $("#brm").click(gsearch('brm'));
});