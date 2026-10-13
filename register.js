
const registerForm = document.getElementById("register-form");
const message = document.getElementById("message");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone_no = document.getElementById("phone_no").value.trim();
    const password = document.getElementById("password").value;

    message.textContent = "Creating your account...";

    try {
        const response = await fetch("http://127.0.0.1:8000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                phone_no: phone_no,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMessage =
                typeof data.detail === "string"
                    ? data.detail
                    : "Registration failed. Please check your details.";

            throw new Error(errorMessage);
        }

        message.textContent = "Account created successfully! Redirecting...";

        setTimeout(() => {
            window.location.href = "login.html";
        }, 1200);

    } catch (error) {
        message.textContent = error.message;
    }
});
