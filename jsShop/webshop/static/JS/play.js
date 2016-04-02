$(document).ready(function(){
  window.addEventListener("message", function(evt){
    if (evt.data.messageType === 'SETTING'){
      $("iframe").width(evt.data.options.width);
      $("iframe").height(evt.data.options.height);
    }
  });
});
