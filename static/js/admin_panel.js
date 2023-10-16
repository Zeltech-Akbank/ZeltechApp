$(document).ready(function(){
    $("#menu1").click(function(event){
        event.preventDefault();
        $.ajax({
            url: 'logistic',
            type: 'GET',
            success: function(response) {
                $("#content").html(response);
            },
            error: function() {
                $("#content").html('<p>Hata oluştu.</p>');
            }
        });
    });

    $("#menu2").click(function(event){
        event.preventDefault();
        $("#content").html("<h3>Menu 2 İçeriği</h3>");
    });

    $("#menu3").click(function(event){
        event.preventDefault();
        $("#content").html("<h3>Menu 3 İçeriği</h3>");
    });
});
console.log("JS dosyası yüklendi!");
