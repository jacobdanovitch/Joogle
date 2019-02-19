var endpointReg = /\/search\/\w+/g;

var gsearch = function(model) {
    return function(){
      var url = `/search/${model}`
      var endpoint = $("#search-form").attr("action");
      endpoint = endpoint.replace(endpointReg, url);
      console.log(endpoint);
      $("#search-form").attr("action", endpoint);
      $("#search-form").submit();
      return true;
    }
  };

var NUM_VISIBLE = 5;

$(document).ready(function() {
  $("#search-form").attr("action", window.location.pathname);
  
  var active = window.location.pathname.replace(endpointReg, function(m){ return m.replace("search/", "").replace("/", "")});
  $(`#${active}`).attr("id", "active");
  $("#vsm").click(gsearch('vsm'));
  $("#brm").click(gsearch('brm'));

  var showHiddens = function(){
    NUM_VISIBLE += 5;
    console.log(`HERE: ${NUM_VISIBLE}`);
    $(".result").each(function(index, el){
      if(index <= NUM_VISIBLE) $(el).removeClass("hidden").show()
    })
  }

  showHiddens()

  $(window).scroll(function () { 
     if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
        showHiddens()
     }
  });
});