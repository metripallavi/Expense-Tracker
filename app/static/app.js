function generateIdempotencyKey() {
    if (window.crypto && crypto.randomUUID) {
        return crypto.randomUUID();
    }
    return "idemp-" + Date.now() + "-" + Math.random().toString(16).slice(2);
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("expense-form");
    if (!form) return;

    const submitButton = document.getElementById("submit-button");
    const statusElement = document.getElementById("form-status");

    let currentIdempotencyKey = generateIdempotencyKey();

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        submitButton.disabled = true;
        statusElement.textContent = "Submitting...";
        statusElement.className = "form-status";

        const formData = new FormData(form);
        const payload = {
            amount: formData.get("amount"),
            category: formData.get("category"),
            description: formData.get("description"),
            date: formData.get("date"),
        };

        try {
            const response = await fetch("/expenses", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Idempotency-Key": currentIdempotencyKey,
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Failed to create expense.");
            }

            statusElement.textContent = "Expense added successfully.";
            statusElement.className = "form-status success";
            form.reset();
            currentIdempotencyKey = generateIdempotencyKey();

            window.location.reload();
        } catch (error) {
            statusElement.textContent = error.message || "Something went wrong.";
            statusElement.className = "form-status error";
        } finally {
            submitButton.disabled = false;
        }
    });
});