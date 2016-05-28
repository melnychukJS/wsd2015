$(document).ready(function(){
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  window.addEventListener("message", function(evt){
    if (evt.data.messageType === 'SETTING'){
      $("iframe").width(evt.data.options.width);
      $("iframe").height(evt.data.options.height);
    }

    if (evt.data.messageType === 'LOAD'){

    }

    if (evt.data.messageType === 'LOAD_REQUEST'){
      var temp = window.location.href.split("/");
      $.ajax({
        url: "/savedState/"+temp[temp.length - 1],
        method: "GET"
      })
      .done(function( data ) {
        if (data === "error"){ //from ajax
          document.querySelector("iframe").contentWindow.postMessage({
            messageType: "ERROR",
            info: "Gamestate could not be loaded"
          }, "*");
        }
        else{
          document.querySelector("iframe").contentWindow.postMessage({
            messageType: "LOAD",
            gameState: JSON.parse(data)
          }, "*");
        }
      });
    }

    if (evt.data.messageType === 'SAVE'){
      var temp = window.location.href.split("/");
      $.ajax({
        url: "/savedState/"+temp[temp.length - 1],
        method: "POST",
        data: {"data":JSON.stringify(evt.data.gameState)}
      })
    }

    if (evt.data.messageType === 'SCORE'){

    }

  });

});
