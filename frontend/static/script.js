async function predictTransaction() {
    const amount = parseFloat(document.getElementById("amount").value);
    const velocity = parseFloat(document.getElementById("velocity").value);
    const avgAmount = parseFloat(document.getElementById("avg_amount").value);
    const merchantDiversity = parseFloat(document.getElementById("merchant_diversity").value);

    if (isNaN(amount) || isNaN(velocity) || isNaN(avgAmount) || isNaN(merchantDiversity)) {
        alert("Please fill all fields correctly.");
        return;
    }

    if (amount < 0 || velocity < 0 || avgAmount < 0 || merchantDiversity < 0) {
        alert("Negative values are not allowed.");
        return;
    }

    const btn = document.querySelector(".predict-btn");
    btn.textContent = "Analyzing...";
    btn.disabled = true;

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                amount: amount,
                velocity_1m: velocity,
                avg_amount_1m: avgAmount,
                merchant_diversity_1m: merchantDiversity,
            }),
        });

        const data = await response.json();
        const resultDiv = document.getElementById("prediction-result");

        const modelExplanation = data.prediction === "anomaly"
            ? "This transaction appears unusual compared to learned transaction behavior patterns."
            : "This transaction matches normal behavioral transaction patterns.";

        resultDiv.innerHTML = `
            <div class="result-item">
                <div class="result-label">Prediction</div>
                <div class="result-value ${data.prediction === "anomaly" ? "anomaly" : "normal"}">
                    ${data.prediction.toUpperCase()}
                </div>
            </div>

            <div class="result-item">
                <div class="result-label">Anomaly Score</div>
                <div class="result-value">
                    ${data.anomaly_score !== null ? data.anomaly_score.toFixed(4) : "N/A"}
                </div>
            </div>

            <div class="result-item">
                <div class="result-label">Explainability Signals</div>
                <ul class="reason-list">
                    ${data.reasons.length > 0
                        ? data.reasons.map(r => `<li>${r}</li>`).join("")
                        : "<li>No major anomaly indicators detected</li>"
                    }
                </ul>
            </div>

            <div class="model-note">
                <h4>Model Behavior</h4>
                <p>${modelExplanation}</p>
            </div>
        `;

    } catch (error) {
        console.error("Prediction request failed:", error);
        alert("Prediction failed. Please try again.");
    } finally {
        btn.textContent = "Analyze Transaction";
        btn.disabled = false;
    }
}