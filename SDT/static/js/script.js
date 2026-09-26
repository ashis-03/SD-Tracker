function toggleUserMenu() {

    const userMenu = document.getElementById("userMenu");

    if (userMenu) {
        userMenu.classList.toggle("active");
    }

}


/* Close when clicking outside */

document.addEventListener("click", function(event) {

    const userMenu = document.getElementById("userMenu");

    if (!userMenu) {
        return;
    }

    if (!userMenu.contains(event.target)) {

        userMenu.classList.remove("active");

    }

});


/* Close with Escape */

document.addEventListener("keydown", function(event) {

    if (event.key === "Escape") {

        const userMenu = document.getElementById("userMenu");

        if (userMenu) {
            userMenu.classList.remove("active");
        }

    }

});
