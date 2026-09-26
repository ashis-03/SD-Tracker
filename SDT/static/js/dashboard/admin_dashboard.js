document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       HELPER
    ========================================================= */

    function getNumber(value) {
        const number = Number(value);
        return Number.isFinite(number) ? number : 0;
    }


    /* =========================================================
       ANIMATED DONUT FUNCTION
    ========================================================= */

    function animateDonut(element, values, colors, duration = 1200) {

        if (!element) return;

        const total = values.reduce(
            (sum, value) => sum + value,
            0
        );

        if (total === 0) {
            element.style.background = "#e2e8f0";
            return;
        }

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
                Math.min(elapsed / duration, 1);


            /*
             * Ease-out animation
             * Starts fast and slows down smoothly.
             */
            const eased =
                1 - Math.pow(1 - progress, 3);


            const currentAngles =
                targetAngles.map(function (angle) {
                    return angle * eased;
                });


            let gradientParts = [];

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


            if (progress < 1) {
                requestAnimationFrame(draw);
            }
        }


        requestAnimationFrame(draw);
    }


    /* =========================================================
       TASK STATUS DONUT
    ========================================================= */

    const taskChart =
        document.getElementById("taskStatusChart");

    if (taskChart) {

        const todo =
            getNumber(taskChart.dataset.todo);

        const progress =
            getNumber(taskChart.dataset.progress);

        const review =
            getNumber(taskChart.dataset.review);

        const completed =
            getNumber(taskChart.dataset.completed);


        const total =
            todo +
            progress +
            review +
            completed;


        const donut =
            taskChart.querySelector(".donut-chart");


        const percentages =
            taskChart.querySelectorAll(
                ".legend-percent"
            );


        /* -----------------------------------------------------
           Animate donut
        ----------------------------------------------------- */

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


        /* -----------------------------------------------------
           Animate percentages
        ----------------------------------------------------- */

        if (percentages.length >= 4) {

            percentages.forEach(function (item) {
                item.textContent = "0%";
            });


            if (total > 0) {

                const finalValues = [
                    todo,
                    progress,
                    review,
                    completed
                ];


                const startTime =
                    performance.now();

                const duration = 1400;


                function animateTaskPercentages(
                    currentTime
                ) {

                    const elapsed =
                        currentTime - startTime;

                    const progressValue =
                        Math.min(
                            elapsed / duration,
                            1
                        );


                    const eased =
                        1 -
                        Math.pow(
                            1 - progressValue,
                            3
                        );


                    finalValues.forEach(
                        function (value, index) {

                            const percentage =
                                Math.round(
                                    (value / total) *
                                    100 *
                                    eased
                                );

                            percentages[index]
                                .textContent =
                                percentage + "%";
                        }
                    );


                    if (progressValue < 1) {

                        requestAnimationFrame(
                            animateTaskPercentages
                        );
                    }
                }


                requestAnimationFrame(
                    animateTaskPercentages
                );
            }
        }
    }


    /* =========================================================
       SDLC PHASE DONUT
    ========================================================= */

    const phaseChart =
        document.getElementById("phaseStatusChart");


    if (phaseChart) {

        const planning =
            getNumber(
                phaseChart.dataset.planning
            );

        const progress =
            getNumber(
                phaseChart.dataset.progress
            );

        const hold =
            getNumber(
                phaseChart.dataset.hold
            );

        const completed =
            getNumber(
                phaseChart.dataset.completed
            );


        const total =
            planning +
            progress +
            hold +
            completed;


        const donut =
            phaseChart.querySelector(
                ".phase-chart"
            );


        const percentages =
            phaseChart.querySelectorAll(
                ".legend-percent"
            );


        /* -----------------------------------------------------
           Animate donut
        ----------------------------------------------------- */

        animateDonut(
            donut,
            [
                planning,
                progress,
                hold,
                completed
            ],
            [
                "#a9cffb",
                "#4f8df7",
                "#f4b83f",
                "#42c59b"
            ],
            1400
        );


        /* -----------------------------------------------------
           Animate percentages
        ----------------------------------------------------- */

        if (percentages.length >= 4) {

            percentages.forEach(function (item) {
                item.textContent = "0%";
            });


            if (total > 0) {

                const finalValues = [
                    planning,
                    progress,
                    hold,
                    completed
                ];


                const startTime =
                    performance.now();

                const duration = 1400;


                function animatePhasePercentages(
                    currentTime
                ) {

                    const elapsed =
                        currentTime - startTime;

                    const progressValue =
                        Math.min(
                            elapsed / duration,
                            1
                        );


                    const eased =
                        1 -
                        Math.pow(
                            1 - progressValue,
                            3
                        );


                    finalValues.forEach(
                        function (value, index) {

                            const percentage =
                                Math.round(
                                    (value / total) *
                                    100 *
                                    eased
                                );


                            percentages[index]
                                .textContent =
                                percentage + "%";
                        }
                    );


                    if (progressValue < 1) {

                        requestAnimationFrame(
                            animatePhasePercentages
                        );
                    }
                }


                requestAnimationFrame(
                    animatePhasePercentages
                );
            }
        }
    }

});