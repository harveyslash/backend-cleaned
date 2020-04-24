$(document).ready(function () {
    $("#onForget").click(function (event) {
        var data = $("#email").val();
        $.post("http://beatest.in/api/v0.1/user/reset_password?token=test", function (data, status) {
            console.log(data + status)
        });
        event.preventDefault();
    });
});




// $(document).ready(function () {
//     $("#onForget").click(function () {
//         var data = $("#email").val();
//         $.post("http://127.0.0.1:5000/forget-password", function (data, status) {
//             console.log(data + status)
//         });
//     });
// });



// $(document).ready(function () {
//     $("#onForget").click(function () {
//         var data = $("#email").val();
//         $.post("http://127.0.0.1:5000/forget-password", function (data, status) {
//             console.log(data + status)
//         });
//     });
// });



// $(document).ready(function () {
//     $("#onForget").click(function () {
//         var data = $("#email").val();
//         $.post("http://127.0.0.1:5000/forget-password", function (data, status) {
//             console.log(data + status)
//         });
//     });
// });