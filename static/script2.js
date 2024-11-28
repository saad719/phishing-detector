document.getElementById("formemail").addEventListener("submit", async function (e) {
    e.preventDefault();  // Prevent the form from submitting normally
    console.log("hello");
    const email = document.getElementById("email").value;  // Get the email address
    const emailText = document.getElementById("emailText").value;  // Get the email text
    const resultElem = document.getElementById("result");
    console.log("Sending data:", { email: email, emailText: emailText });
    // Send the email address and content as JSON in the request body
    const response = await fetch("/check-email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",  // Ensure the correct content type
        },
        body: JSON.stringify({ email: email, emailText: emailText }),  // Send both email address and content
    });
    

    // Handle the response
    const data = await response.json();
    if (data.error) {
        // Display the error message to the user
        alert(data.error);
    } else {
        resultElem.innerText = data.result;
        
        if (data.result.trim() === "Phishing Link" || data.result.trim() === "Suspicious") {
            console.log("Condition met: Showing email form.");
            
            document.getElementById('block-Email').style.display = 'inline-block';
        } else {
            console.log("Condition not met.");
            document.getElementById('block-Email').style.display = 'none'; // E
        }
    }
   
});
document.getElementById("seeMoreDetails").addEventListener("click", function () {
    window.location.href = "/phishing-details"; // Redirect to the phishing details page
});
