document.getElementById("block-Email").addEventListener("click", async function () {
    const email = document.getElementById('email').value;

    const response = await fetch("/block-sender", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email }),  // Send the email address to block
    });

    const data = await response.json();
    alert(data.message);  // Notify the user that the sender has been blocked
});
