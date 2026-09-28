// user detail pop-up
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

// theme control dark-light 
document.addEventListener("DOMContentLoaded", function () {

    const themeToggle = document.getElementById("themeToggle");

    if (!themeToggle) return;

    const icon = themeToggle.querySelector("i");

    // Load saved theme
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.documentElement.classList.add("dark-theme");

        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
    }

    themeToggle.addEventListener("click", function () {

        document.documentElement.classList.toggle("dark-theme");

        const isDark =
            document.documentElement.classList.contains("dark-theme");

        localStorage.setItem(
            "theme",
            isDark ? "dark" : "light"
        );

        if (isDark) {
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");
        } else {
            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");
        }
    });

});


// =========================================================
// SIDEBAR TOGGLE
// Only the ☰ button can expand/collapse the sidebar
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    const sidebarToggle = document.getElementById("sidebarToggle");

    if (!sidebarToggle) {
        return;
    }

    // Restore previous sidebar state

    const sidebarState = localStorage.getItem("sidebarCollapsed");

    if (sidebarState === "true") {
        document.body.classList.add("sidebar-collapsed");
    }


    // -----------------------------------------------------
    // Toggle ONLY when ☰ button is clicked
    // -----------------------------------------------------

    sidebarToggle.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        document.body.classList.toggle("sidebar-collapsed");

        // Save current state
        const isCollapsed =
            document.body.classList.contains("sidebar-collapsed");

        localStorage.setItem(
            "sidebarCollapsed",
            isCollapsed
        );

    });

});