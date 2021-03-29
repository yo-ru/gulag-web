// sticky header
$(window).scroll(() => {
    var header = document.getElementById("navbar");
    var sticky = header.offsetTop;

    if (window.pageYOffset > sticky) {
        header.classList.add("minimized");
    } else {
        header.classList.remove("minimized");
    }
});

//toggle navbar for mobile
function togglenavbar() {
    document.getElementById('navbar').classList.toggle("is-active");
    document.getElementById('navbar-burger').classList.toggle("is-active");
}

var modal = document.getElementById('contentmodal');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (modal.innerHTML.length !== 0) {
        if (event.target.id !== modal) {
            document.getElementById('modaldisplayer').className = "modal"
        }
    }
}