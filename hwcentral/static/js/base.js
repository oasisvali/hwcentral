$(document).ready(function () {
    $("select").addClass("chosen-select");
    $(".chosen-select").chosen()
});

if (screen.width<=760){
    alert ("Sorry ! HWCentral does not support this device. To ensure an optimal experience, try logging in from a non-mobile device")
}