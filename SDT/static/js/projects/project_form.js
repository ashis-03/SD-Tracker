const button = document.getElementById("teamDropdownBtn");
const dropdown = document.getElementById("teamDropdown");

button.addEventListener("click", function () {

    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }

});