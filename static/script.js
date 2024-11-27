document.getElementById("link-form").addEventListener("submit", async function (e) {
    e.preventDefault();  // Prevent form from submitting the default way

    const url = document.getElementById("link").value;  // Use correct input ID
    const resultElem = document.getElementById("result");

    // Send the data as JSON in the request body
    const response = await fetch("/check-link", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",  // Ensure correct content type
        },
        body: JSON.stringify({ url: url }),  // Send URL as JSON
    })
    
    

    // Handle the response
    const data = await response.json();
    if (data.error) {
        // Display the error message to the user
        alert(data.error);}
        else {
            resultElem.innerText = data.result;
        
            if (data.result.trim() === "Phishing Link" || data.result.trim() === "Suspicious") {
                console.log("Condition met: Showing email form.");
                document.getElementById("emailForm").style.display = "block";
            } else {
                console.log("Condition not met.");
            }
        }
        
    
});
document.getElementById("seeMoreDetails").addEventListener("click", function () {
    window.location.href = "/phishing-details"; // Redirect to the phishing details page
});

document.addEventListener("DOMContentLoaded", function () {
    const emailForm = document.getElementById("phishingEmailForm");
    const emailMessage = document.getElementById("emailMessage");

    emailForm.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent the form from reloading the page

        const emailInput = document.getElementById("email").value.trim();

        // Validate email format (optional since 'required' is in HTML)
        if (!emailInput || !validateEmail(emailInput)) {
            emailMessage.style.color = "red";
            emailMessage.innerText = "Please enter a valid email address.";
            return;
        }

        // Send the email data to the server or perform an action
        fetch('/report-phishing-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: emailInput })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                emailMessage.style.color = "green";
                emailMessage.innerText = "Phishing email reported successfully!";
                emailForm.reset();
            } else {
                emailMessage.style.color = "red";
                emailMessage.innerText = "Failed to report email. Please try again.";
            }
        })
        .catch(error => {
            console.error("Error reporting email:", error);
            emailMessage.style.color = "red";
            emailMessage.innerText = "An error occurred. Please try again.";
        });
    });

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});
