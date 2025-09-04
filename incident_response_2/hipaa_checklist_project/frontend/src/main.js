let complianceScore = 50;
const regulationName = "HIPAA Privacy Rule";
const maxScore = 100;

// Use a logical operator (&&) in the condition
if (complianceScore >= maxScore / 2 && regulationName) {
    console.log(`Checking compliance for: ${regulationName}`);
    document.getElementById("complianceResult").innerText = `Compliance Score: ${complianceScore}%`;
} else {
    console.log(`Compliance check failed for: ${regulationName}`);
    document.getElementById("complianceResult").innerText = `Compliance Score: ${complianceScore}% - Needs Improvement`;
}