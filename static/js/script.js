document.addEventListener("DOMContentLoaded", function () {
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