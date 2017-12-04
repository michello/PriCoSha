$(document).ready(function(){
    $(".postComment").click(function(){
      console.log("working");
      let commentName = "#comment"+this.id;
        $(commentName).toggle();
    });
});
