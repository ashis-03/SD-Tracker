document.addEventListener("DOMContentLoaded", function () {

    const dropdown = document.querySelector(".team-dropdown");
    const button = document.getElementById("teamDropdownBtn");
    const dropdownContent = document.getElementById("teamDropdown");
    const selectedText = document.getElementById("selectedTeamsText");

    if (!dropdown || !button || !dropdownContent || !selectedText) {
        console.error("Team dropdown elements not found.");
        return;
    }


    // Open / close dropdown
    button.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        dropdown.classList.toggle("open");

    });


    // Prevent clicks inside dropdown from closing it
    dropdownContent.addEventListener("click", function (event) {

        event.stopPropagation();

    });


    // Close when clicking outside
    document.addEventListener("click", function (event) {

        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove("open");
        }

    });


    // Update selected teams text
    function updateSelectedTeams() {

        const checked = dropdownContent.querySelectorAll(
            'input[type="checkbox"]:checked'
        );

        if (checked.length === 0) {

            selectedText.textContent = "Select Teams";

            return;
        }


        const names = Array.from(checked).map(function (checkbox) {

            const option = checkbox.closest(".team-option");

            if (!option) {
                return "";
            }

            const text = option.querySelector("span");

            return text ? text.textContent.trim() : "";

        }).filter(Boolean);


        selectedText.textContent = names.join(", ");

    }


    // Checkbox change
    dropdownContent
        .querySelectorAll('input[type="checkbox"]')
        .forEach(function (checkbox) {

            checkbox.addEventListener(
                "change",
                updateSelectedTeams
            );

        });


    // Initial state
    updateSelectedTeams();

});