document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       HELPER
    ========================================================= */

    function getNumber(value) {
        const number = Number(value);
        return Number.isFinite(number) ? number : 0;
    }


    /* =========================================================
       EASING
    ========================================================= */

    function easeOutCubic(progress) {
        return 1 - Math.pow(1 - progress, 3);
    }


    /* =========================================================
       ANIMATED DONUT
    ========================================================= */

    function animateDonut(element, values, colors, duration = 1400) {

        if (!element) {
            return;
        }

        const total = values.reduce(function (sum, value) {
            return sum + value;
        }, 0);


        /* -----------------------------------------------------
           No data
        ----------------------------------------------------- */

        if (total === 0) {

            element.style.background = "#e2e8f0";

            return;
        }


        /* -----------------------------------------------------
           Calculate target angles
        ----------------------------------------------------- */

        const targetAngles = [];

        let accumulated = 0;

        values.forEach(function (value) {

            accumulated +=
                (value / total) * 360;

            targetAngles.push(accumulated);
        });


        /* -----------------------------------------------------
           Animation
        ----------------------------------------------------- */

        const startTime = performance.now();


        function draw(currentTime) {

            const elapsed =
                currentTime - startTime;

            const progress =
                Math.min(
                    elapsed / duration,
                    1
                );

            const eased =
                easeOutCubic(progress);


            /* ---------------------------------------------
               Calculate current angles
            --------------------------------------------- */

            const currentAngles =
                targetAngles.map(function (angle) {

                    return angle * eased;

                });


            /* ---------------------------------------------
               Build gradient
            --------------------------------------------- */

            const gradientParts = [];

            let previousAngle = 0;


            currentAngles.forEach(
                function (angle, index) {

                    gradientParts.push(
                        `${colors[index]} ${previousAngle}deg ${angle}deg`
                    );

                    previousAngle = angle;

                }
            );


            element.style.background = `
                conic-gradient(
                    ${gradientParts.join(", ")}
                )
            `;


            /* ---------------------------------------------
               Continue animation
            --------------------------------------------- */

            if (progress < 1) {

                requestAnimationFrame(draw);

            }

        }


        requestAnimationFrame(draw);

    }


    /* =========================================================
       ANIMATE NUMBERS / PERCENTAGES
    ========================================================= */

    function animatePercentages(
        elements,
        values,
        total,
        duration = 1400
    ) {

        if (!elements || elements.length === 0) {
            return;
        }


        /* Start from 0% */

        elements.forEach(function (element) {

            element.textContent = "0%";

        });


        if (total === 0) {
            return;
        }


        const startTime = performance.now();


        function update(currentTime) {

            const elapsed =
                currentTime - startTime;

            const progress =
                Math.min(
                    elapsed / duration,
                    1
                );

            const eased =
                easeOutCubic(progress);


            values.forEach(
                function (value, index) {

                    if (!elements[index]) {
                        return;
                    }


                    const percentage =
                        Math.round(
                            (value / total) *
                            100 *
                            eased
                        );


                    elements[index].textContent =
                        percentage + "%";

                }
            );


            if (progress < 1) {

                requestAnimationFrame(update);

            }

        }


        requestAnimationFrame(update);

    }


    /* =========================================================
       MANAGER PROJECT STATUS DONUT
    ========================================================= */

    const projectChart =
        document.getElementById(
            "managerProjectStatusChart"
        );


    if (projectChart) {

        /* ---------------------------------------------
           Get project statistics
        --------------------------------------------- */

        const active =
            getNumber(
                projectChart.dataset.active
            );

        const planning =
            getNumber(
                projectChart.dataset.planning
            );

        const hold =
            getNumber(
                projectChart.dataset.hold
            );

        const completed =
            getNumber(
                projectChart.dataset.completed
            );


        /* ---------------------------------------------
           Total projects
        --------------------------------------------- */

        const total =
            active +
            planning +
            hold +
            completed;


        /* ---------------------------------------------
           Find donut
        --------------------------------------------- */

        const donut =
            projectChart.querySelector(
                ".manager-project-chart"
            );


        /* ---------------------------------------------
           Find percentages
        --------------------------------------------- */

        const percentages =
            projectChart.querySelectorAll(
                ".legend-percent"
            );


        /* ---------------------------------------------
           Animate donut
           
           Green  = Active
           Blue   = Planning
           Orange = On Hold
           Purple = Completed
        --------------------------------------------- */

        animateDonut(

            donut,

            [
                active,
                planning,
                hold,
                completed
            ],

            [
                "#42c59b",
                "#4f8df7",
                "#f4b83f",
                "#7748d8"
            ],

            1400

        );


        /* ---------------------------------------------
           Animate percentages
        --------------------------------------------- */

        animatePercentages(

            percentages,

            [
                active,
                planning,
                hold,
                completed
            ],

            total,

            1400

        );

    }


    /* =========================================================
       PROJECT PROGRESS BAR ANIMATION
    ========================================================= */

    const progressBars =
        document.querySelectorAll(
            ".project-progress-item .progress-bar"
        );


    progressBars.forEach(function (bar) {

        const targetWidth =
            bar.style.width;


        /* Start at zero */

        bar.style.width = "0%";


        /* Allow browser to render zero first */

        requestAnimationFrame(function () {

            requestAnimationFrame(function () {

                bar.style.transition =
                    "width 1200ms cubic-bezier(0.22, 1, 0.36, 1)";

                bar.style.width =
                    targetWidth;

            });

        });

    });


    /* =========================================================
       TABLE PROGRESS BAR ANIMATION
    ========================================================= */

    const tableProgressBars =
        document.querySelectorAll(
            ".table-progress .progress-bar"
        );


    tableProgressBars.forEach(function (bar) {

        const targetWidth =
            bar.style.width;


        bar.style.width = "0%";


        requestAnimationFrame(function () {

            requestAnimationFrame(function () {

                bar.style.transition =
                    "width 1200ms cubic-bezier(0.22, 1, 0.36, 1)";

                bar.style.width =
                    targetWidth;

            });

        });

    });


    /* =========================================================
       STAT CARD ENTRANCE ANIMATION
    ========================================================= */

    const statCards =
        document.querySelectorAll(
            ".stat-card"
        );


    statCards.forEach(function (card, index) {

        card.style.opacity = "0";

        card.style.transform =
            "translateY(15px)";


        card.style.transition = `
            opacity 500ms ease,
            transform 500ms ease
        `;


        setTimeout(function () {

            card.style.opacity = "1";

            card.style.transform =
                "translateY(0)";

        }, 80 + (index * 80));

    });


    /* =========================================================
       DASHBOARD CARD ENTRANCE ANIMATION
    ========================================================= */

    const dashboardCards =
        document.querySelectorAll(
            ".dashboard-card"
        );


    dashboardCards.forEach(function (card, index) {

        card.style.opacity = "0";

        card.style.transform =
            "translateY(12px)";


        card.style.transition = `
            opacity 550ms ease,
            transform 550ms ease
        `;


        setTimeout(function () {

            card.style.opacity = "1";

            card.style.transform =
                "translateY(0)";

        }, 250 + (index * 100));

    });


    /* =========================================================
       TEAM MEMBER ANIMATION
    ========================================================= */

    const teamMembers =
        document.querySelectorAll(
            ".team-member-item"
        );


    teamMembers.forEach(function (member, index) {

        member.style.opacity = "0";

        member.style.transform =
            "translateX(10px)";


        member.style.transition = `
            opacity 400ms ease,
            transform 400ms ease
        `;


        setTimeout(function () {

            member.style.opacity = "1";

            member.style.transform =
                "translateX(0)";

        }, 500 + (index * 80));

    });


    /* =========================================================
       DEADLINE ANIMATION
    ========================================================= */

    const deadlines =
        document.querySelectorAll(
            ".deadline-item"
        );


    deadlines.forEach(function (deadline, index) {

        deadline.style.opacity = "0";

        deadline.style.transform =
            "translateX(10px)";


        deadline.style.transition = `
            opacity 400ms ease,
            transform 400ms ease
        `;


        setTimeout(function () {

            deadline.style.opacity = "1";

            deadline.style.transform =
                "translateX(0)";

        }, 600 + (index * 80));

    });


    /* =========================================================
       TABLE ROW HOVER EFFECT
    ========================================================= */

    const tableRows =
        document.querySelectorAll(
            ".dashboard-table tbody tr"
        );


    tableRows.forEach(function (row) {

        row.addEventListener(
            "mouseenter",
            function () {

                row.style.transition =
                    "background 0.2s ease";

            }
        );

    });


});