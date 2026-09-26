document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       HELPER
    ========================================================= */

    function getNumber(value) {
        const number = Number(value);

        return Number.isFinite(number)
            ? number
            : 0;
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

    function animateDonut(
        element,
        values,
        colors,
        duration = 1400
    ) {

        if (!element) {
            return;
        }


        const total = values.reduce(
            function (sum, value) {
                return sum + value;
            },
            0
        );


        /* -----------------------------------------------------
           NO DATA
        ----------------------------------------------------- */

        if (total === 0) {

            element.style.background =
                "#e2e8f0";

            return;
        }


        /* -----------------------------------------------------
           TARGET ANGLES
        ----------------------------------------------------- */

        const targetAngles = [];

        let accumulated = 0;


        values.forEach(function (value) {

            accumulated +=
                (value / total) * 360;

            targetAngles.push(accumulated);

        });


        /* -----------------------------------------------------
           ANIMATION
        ----------------------------------------------------- */

        const startTime =
            performance.now();


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
               Current angles
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
       ANIMATED PERCENTAGES
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


        /* Start from zero */

        elements.forEach(function (element) {

            element.textContent = "0%";

        });


        if (total === 0) {
            return;
        }


        const startTime =
            performance.now();


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
       MY TASK OVERVIEW DONUT
       
       To Do
       In Progress
       In Review
       Completed
    ========================================================= */

    const taskChart =
        document.getElementById(
            "taskStatusChart"
        );


    if (taskChart) {

        /* ---------------------------------------------
           Get Django values
        --------------------------------------------- */

        const todo =
            getNumber(
                taskChart.dataset.todo
            );


        const progress =
            getNumber(
                taskChart.dataset.progress
            );


        const review =
            getNumber(
                taskChart.dataset.review
            );


        const completed =
            getNumber(
                taskChart.dataset.completed
            );


        const total =
            todo +
            progress +
            review +
            completed;


        /* ---------------------------------------------
           Donut
        --------------------------------------------- */

        const donut =
            taskChart.querySelector(
                ".donut-chart"
            );


        /* ---------------------------------------------
           Percentages
        --------------------------------------------- */

        const percentages =
            taskChart.querySelectorAll(
                ".legend-percent"
            );


        /* ---------------------------------------------
           Animate donut
        --------------------------------------------- */

        animateDonut(

            donut,

            [
                todo,
                progress,
                review,
                completed
            ],

            [
                "#dce3ec",
                "#4f8df7",
                "#f4b83f",
                "#42c59b"
            ],

            1400

        );


        /* ---------------------------------------------
           Animate percentages
        --------------------------------------------- */

        animatePercentages(

            percentages,

            [
                todo,
                progress,
                review,
                completed
            ],

            total,

            1400

        );

    }


    /* =========================================================
       PROJECT PROGRESS
    ========================================================= */

    const progressBars =
        document.querySelectorAll(
            ".project-progress-item .progress-bar"
        );


    progressBars.forEach(function (bar, index) {

        const targetWidth =
            bar.style.width;


        /* Start from zero */

        bar.style.width =
            "0%";


        requestAnimationFrame(function () {

            requestAnimationFrame(function () {

                bar.style.transition = `
                    width 1200ms
                    cubic-bezier(0.22, 1, 0.36, 1)
                `;


                setTimeout(function () {

                    bar.style.width =
                        targetWidth;

                }, index * 120);

            });

        });

    });


    /* =========================================================
       TABLE PROGRESS BARS
    ========================================================= */

    const tableProgressBars =
        document.querySelectorAll(
            ".table-progress .progress-bar"
        );


    tableProgressBars.forEach(function (bar, index) {

        const targetWidth =
            bar.style.width;


        bar.style.width =
            "0%";


        requestAnimationFrame(function () {

            requestAnimationFrame(function () {

                bar.style.transition = `
                    width 1000ms
                    cubic-bezier(0.22, 1, 0.36, 1)
                `;


                setTimeout(function () {

                    bar.style.width =
                        targetWidth;

                }, 300 + (index * 100));

            });

        });

    });


    /* =========================================================
       STAT CARD ENTRANCE
    ========================================================= */

    const statCards =
        document.querySelectorAll(
            ".stat-card"
        );


    statCards.forEach(function (card, index) {

        card.style.opacity =
            "0";


        card.style.transform =
            "translateY(15px)";


        card.style.transition = `
            opacity 500ms ease,
            transform 500ms ease
        `;


        setTimeout(function () {

            card.style.opacity =
                "1";


            card.style.transform =
                "translateY(0)";

        }, 80 + (index * 80));

    });


    /* =========================================================
       DASHBOARD CARDS
    ========================================================= */

    const dashboardCards =
        document.querySelectorAll(
            ".dashboard-card"
        );


    dashboardCards.forEach(function (card, index) {

        card.style.opacity =
            "0";


        card.style.transform =
            "translateY(12px)";


        card.style.transition = `
            opacity 550ms ease,
            transform 550ms ease
        `;


        setTimeout(function () {

            card.style.opacity =
                "1";


            card.style.transform =
                "translateY(0)";

        }, 250 + (index * 100));

    });


    /* =========================================================
       ASSIGNED PROJECTS
    ========================================================= */

    const assignedProjects =
        document.querySelectorAll(
            ".assigned-project-item"
        );


    assignedProjects.forEach(
        function (project, index) {

            project.style.opacity =
                "0";


            project.style.transform =
                "translateX(10px)";


            project.style.transition = `
                opacity 450ms ease,
                transform 450ms ease
            `;


            setTimeout(function () {

                project.style.opacity =
                    "1";


                project.style.transform =
                    "translateX(0)";

            }, 450 + (index * 100));

        }
    );


    /* =========================================================
       RECENT TASK ROWS
    ========================================================= */

    const taskRows =
        document.querySelectorAll(
            ".dashboard-table tbody tr"
        );


    taskRows.forEach(function (row, index) {

        row.style.opacity =
            "0";


        row.style.transform =
            "translateY(8px)";


        row.style.transition = `
            opacity 400ms ease,
            transform 400ms ease,
            background 200ms ease
        `;


        setTimeout(function () {

            row.style.opacity =
                "1";


            row.style.transform =
                "translateY(0)";

        }, 500 + (index * 80));

    });


    /* =========================================================
       RECENT NOTIFICATIONS
    ========================================================= */

    const notifications =
        document.querySelectorAll(
            ".notification-item"
        );


    notifications.forEach(
        function (notification, index) {

            notification.style.opacity =
                "0";


            notification.style.transform =
                "translateX(10px)";


            notification.style.transition = `
                opacity 400ms ease,
                transform 400ms ease
            `;


            setTimeout(function () {

                notification.style.opacity =
                    "1";


                notification.style.transform =
                    "translateX(0)";

            }, 550 + (index * 90));

        }
    );


    /* =========================================================
       UPCOMING DEADLINES
    ========================================================= */

    const deadlines =
        document.querySelectorAll(
            ".deadline-item"
        );


    deadlines.forEach(
        function (deadline, index) {

            deadline.style.opacity =
                "0";


            deadline.style.transform =
                "translateX(10px)";


            deadline.style.transition = `
                opacity 400ms ease,
                transform 400ms ease
            `;


            setTimeout(function () {

                deadline.style.opacity =
                    "1";


                deadline.style.transform =
                    "translateX(0)";

            }, 550 + (index * 80));

        }
    );


    /* =========================================================
       TABLE HOVER
    ========================================================= */

    const tableRows =
        document.querySelectorAll(
            ".dashboard-table tbody tr"
        );


    tableRows.forEach(function (row) {

        row.addEventListener(
            "mouseenter",
            function () {

                row.style.background =
                    "#f8fafc";

            }
        );


        row.addEventListener(
            "mouseleave",
            function () {

                row.style.background =
                    "";

            }
        );

    });


    /* =========================================================
       STAT CARD HOVER
    ========================================================= */

    statCards.forEach(function (card) {

        card.addEventListener(
            "mouseenter",
            function () {

                card.style.transform =
                    "translateY(-3px)";

            }
        );


        card.addEventListener(
            "mouseleave",
            function () {

                card.style.transform =
                    "translateY(0)";

            }
        );

    });


    /* =========================================================
       DASHBOARD CARD HOVER
    ========================================================= */

    dashboardCards.forEach(function (card) {

        card.addEventListener(
            "mouseenter",
            function () {

                card.style.transform =
                    "translateY(-2px)";

            }
        );


        card.addEventListener(
            "mouseleave",
            function () {

                card.style.transform =
                    "translateY(0)";

            }
        );

    });


    /* =========================================================
       DONUT ENTRANCE
    ========================================================= */

    if (taskChart) {

        const donut =
            taskChart.querySelector(
                ".donut-chart"
            );


        if (donut) {

            donut.animate(
                [
                    {
                        opacity: 0,
                        transform:
                            "scale(0.75) rotate(-90deg)"
                    },
                    {
                        opacity: 1,
                        transform:
                            "scale(1) rotate(0deg)"
                    }
                ],
                {
                    duration: 900,
                    easing:
                        "cubic-bezier(0.22, 1, 0.36, 1)",
                    fill: "forwards"
                }
            );

        }

    }

});