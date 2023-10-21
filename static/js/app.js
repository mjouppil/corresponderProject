const buttonToast = document.getElementById("toast1");

function handleToast(event) {
    // console.log(event.target.value)
    $("#myToast").show();
    document.getElementById("toast-text").innerHTML = event.target.getAttribute('value');
}

buttonToast.addEventListener("click", handleToast, false);

$(document).ready(function(){
    $("#toastDismiss").click(function(){
        $("#myToast").hide()
    });
});
