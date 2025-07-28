let complianceScore = 50;
const regulationName = "HIPAA Privacy Rule";
const maxScore = 100;

if (complianceScore >= maxScore / 2) {
    console.log(`Checking compliance for: ${regulationName}`);
    document.getElementById("complianceResult").innerText = `Compliance Score: ${complianceScore}%`;
} else {
    console.log(`Compliance check failed for: ${regulationName}`);
    document.getElementById("complianceResult").innerText = `Compliance Score: ${complianceScore}% - Needs Improvement`;
}