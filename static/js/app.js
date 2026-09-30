document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // FILE UPLOAD NAME
    // =========================

    const imageInput = document.getElementById("jewelry-image");
    const fileName = document.getElementById("file-name");

    if (imageInput && fileName) {

        imageInput.addEventListener("change", () => {

            if (imageInput.files.length > 0) {

                const file = imageInput.files[0];

                // Check file size
                if (file.size > 5 * 1024 * 1024) {
                    fileName.textContent = "File is larger than 5 MB.";
                    fileName.style.color = "#c62828";
                    imageInput.value = "";
                    return;
                }

                // Check file type
                const allowedTypes = [
                    "image/jpeg",
                    "image/png",
                    "image/webp"
                ];

                if (!allowedTypes.includes(file.type)) {

                    fileName.textContent =
                        "Invalid file type. Please upload JPG, PNG or WEBP.";

                    fileName.style.color = "#c62828";
                    imageInput.value = "";
                    return;
                }

                fileName.textContent = file.name;
                fileName.style.color = "#20a46b";

            } else {

                fileName.textContent =
                    "JPG, PNG or WEBP · Max 5 MB";

                fileName.style.color = "";
            }
        });
    }


    // =========================
    // COMMON REDIRECT FUNCTION
    // =========================

    function redirectToRecommendation(result) {

        console.log("Generate response:", result);

        // If backend directly provides a redirect URL
        if (result.redirect) {

            window.location.href = result.redirect;
            return;
        }

        // Alternative redirect URL
        if (result.redirect_url) {

            window.location.href = result.redirect_url;
            return;
        }

        // Our backend returns history_id
        if (result.history_id) {

            window.location.href =
                `/recommendations/${result.history_id}`;

            return;
        }

        // If no redirect information is available
        console.log(
            "No redirect information returned:",
            result
        );
    }


    // =========================
    // HOME PLANNER
    // =========================

    const homeForm = document.getElementById("home-form");

    if (homeForm) {

        homeForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const status =
                document.getElementById("home-status");


            const data = {

                budget: Number(
                    document.getElementById("home-budget").value
                ),

                room_type:
                    document.getElementById("room-type").value,

                style:
                    document.getElementById("home-style").value,

                lights: Number(
                    document.getElementById("lights").value
                ),

                fans: Number(
                    document.getElementById("fans").value
                ),

                tables: Number(
                    document.getElementById("tables").value
                ),

                additional_requirements:
                    document.getElementById(
                        "home-requirements"
                    ).value
            };


            status.textContent =
                "Generating your AI plan...";

            status.className = "loading";


            try {

                const response = await fetch(
                    "/generate-home",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify(data)
                    }
                );


                const result =
                    await response.json();


                // Backend returned an error
                if (!response.ok) {

                    throw new Error(
                        result.detail ||
                        result.message ||
                        "Something went wrong while generating the plan."
                    );
                }


                // Successful generation
                status.textContent =
                    "Plan generated successfully! Redirecting...";

                status.className = "success";


                // Redirect using history_id
                redirectToRecommendation(result);

            }

            catch (error) {

                console.error(
                    "Home planner error:",
                    error
                );

                status.textContent =
                    error.message ||
                    "Unable to generate the plan.";

                status.className = "error";
            }

        });
    }


    // =========================
    // PARTY PLANNER
    // =========================

    const partyForm =
        document.getElementById("party-form");

    if (partyForm) {

        partyForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const status =
                document.getElementById("party-status");


            const data = {

                budget: Number(
                    document.getElementById(
                        "party-budget"
                    ).value
                ),

                guests: Number(
                    document.getElementById(
                        "guests"
                    ).value
                ),

                event_type:
                    document.getElementById(
                        "event-type"
                    ).value,

                venue:
                    document.getElementById(
                        "venue"
                    ).value,

                food_preference:
                    document.getElementById(
                        "food-preference"
                    ).value,

                additional_requirements:
                    document.getElementById(
                        "party-requirements"
                    ).value
            };


            status.textContent =
                "Generating your AI party plan...";

            status.className = "loading";


            try {

                const response = await fetch(
                    "/generate-party",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify(data)
                    }
                );


                const result =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        result.detail ||
                        result.message ||
                        "Something went wrong while generating the party plan."
                    );
                }


                status.textContent =
                    "Party plan generated! Redirecting...";

                status.className = "success";


                // Redirect using history_id
                redirectToRecommendation(result);

            }

            catch (error) {

                console.error(
                    "Party planner error:",
                    error
                );

                status.textContent =
                    error.message ||
                    "Unable to generate the party plan.";

                status.className = "error";
            }

        });
    }


    // =========================
    // JEWELRY PLANNER
    // =========================

    const jewelryForm =
        document.getElementById("jewelry-form");


    if (jewelryForm) {

        jewelryForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();


                const status =
                    document.getElementById(
                        "jewelry-status"
                    );


                // Create FormData from the form
                const formData =
                    new FormData(jewelryForm);


                status.textContent =
                    "Analyzing your style and generating recommendations...";

                status.className = "loading";


                try {

                    const response = await fetch(
                        "/generate-jewelry",
                        {
                            method: "POST",

                            body: formData
                        }
                    );


                    const result =
                        await response.json();


                    if (!response.ok) {

                        throw new Error(
                            result.detail ||
                            result.message ||
                            "Something went wrong while generating jewelry recommendations."
                        );
                    }


                    status.textContent =
                        "Jewelry recommendations generated! Redirecting...";

                    status.className = "success";


                    // Redirect using history_id
                    redirectToRecommendation(result);

                }

                catch (error) {

                    console.error(
                        "Jewelry planner error:",
                        error
                    );

                    status.textContent =
                        error.message ||
                        "Unable to generate jewelry recommendations.";

                    status.className = "error";
                }

            }
        );
    }

});