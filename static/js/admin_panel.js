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
        $.ajax({
            url: 'logistic-review',
            type: 'GET',
            success: function(response) {
                $("#content").html(response);
            },
            error: function() {
                $("#content").html('<p>Hata oluştu.</p>');
            }
        });
    });

    $("#menu3").click(function(event){
    event.preventDefault();
    $.ajax({
        url: 'maps',
        type: 'GET',
        success: function(response) {
            $("#content").html(response);
        },
        error: function() {
            $("#content").html('<p>Hata oluştu.</p>');
            }
        });
    });

});


document.getElementById("sidebarToggle").addEventListener("click", function() {
    var sidebar = document.getElementById("sidebar");

    if (sidebar.style.display === "none" || sidebar.style.width === "0px") {
        sidebar.style.display = "block";
        sidebar.style.width = "250px";
    } else {
        sidebar.style.width = "0px";
        setTimeout(function(){ sidebar.style.display = "none"; }, 300);
    }
});

console.log("JS dosyası yüklendi!");
