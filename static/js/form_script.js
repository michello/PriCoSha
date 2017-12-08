$(document).ready(function(){
    $("input[type='radio']").click(function(){
      if (this.value == 1) {
         $("#groupPost").hide();
      } else {
        $("#groupPost").show();
      }
    });
});
