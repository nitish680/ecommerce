
const loginForm = document.getElementById("login-form");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    message.textContent = "Logging in...";

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.message || "Login failed");
        }

        if (!data.token) {
            throw new Error("Login succeeded, but the server returned no token.");
        }

        localStorage.setItem("token", data.token);
        localStorage.setItem("user_name", data.name);
        localStorage.setItem("user_role", data.role);

        message.textContent = "Login successful!";

        window.location.href = "order_history.html";

    } catch (error) {
        message.textContent = error.message;
    }
});
