$(document).ready(function () {

    // all custom jQuery will go here
    $("#firstbutton").click(function () {
        $.ajax({
            url: "localhost:32335", success: function (result) {
                $("#firstbutton").toggleClass("btn-primary:focus");
            }
        });
    });
    $("#secondbutton").click(function () {
        $.ajax({
            url: "localhost:31291", success: function (result) {
                $("#secondbutton").toggleClass("btn-primary:focus");
            }
        });
    });
});