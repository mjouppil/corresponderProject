$(document).ready(function(){
    $("#toastDismiss").click(function(){
        $("#myToast").hide()
    });
});


const modalThread = document.getElementById("modalNewThread")
if (modalThread) {
    modalThread.addEventListener('show.bs.modal', event => {
    })
}

const modalToken = document.getElementById("modalToken")
if (modalToken) {
    modalToken.addEventListener('show.bs.modal', event => {
    })
}
