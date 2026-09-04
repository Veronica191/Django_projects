document.addEventListener("DOMContentLoaded", function () {
    const password = document.querySelector("#password");
    const passwordToggle = document.querySelector(".password-toggle");
    const loginForm = document.querySelector(".login-form");

    if (password && passwordToggle) {
        passwordToggle.addEventListener("click", function () {
            const isVisible = password.type === "text";
            password.type = isVisible ? "password" : "text";
            passwordToggle.textContent = isVisible ? "Show" : "Hide";
            passwordToggle.setAttribute("aria-label", isVisible ? "Show password" : "Hide password");
            passwordToggle.setAttribute("aria-pressed", String(!isVisible));
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", function () {
            const submit = loginForm.querySelector(".login-submit");

            if (submit) {
                submit.classList.add("is-loading");
                submit.textContent = "Signing in...";
                submit.disabled = true;
            }
        });
    }

    document.querySelectorAll(".alert").forEach(function (alert) {
        const dismiss = alert.querySelector(".alert-dismiss");

        if (dismiss) {
            dismiss.addEventListener("click", function () {
                alert.classList.add("is-dismissing");
                setTimeout(function () { alert.remove(); }, 180);
            });
        }

        if (!alert.classList.contains("alert-error")) {
            setTimeout(function () {
                if (alert.isConnected) {
                    alert.classList.add("is-dismissing");
                    setTimeout(function () { alert.remove(); }, 180);
                }
            }, 5000);
        }
    });
});