const express = require('express');
const fetch = require('node-fetch');
const app = express();
const PORT = 3000;

app.use(express.json());

// Endpoint to handle symptom submission
app.post('/submit-symptoms', async (req, res) => {
    const { age, temp } = req.body;

    // Initialize session
    let sessionResponse = await fetch('https://api.endlessmedical.com/v1/dx/InitSession');
    let sessionData = await sessionResponse.json();
    let sessionID = sessionData.SessionID;

    // Accept Terms of Use
    await fetch(`https://api.endlessmedical.com/v1/dx/AcceptTermsOfUse?SessionID=${sessionID}&passphrase=I%20have%20read%2C%20understood%20and%20I%20accept%20and%20agree%20to%20comply%20with%20the%20Terms%20of%20Use%20of%20EndlessMedicalAPI%20and%20Endless%20Medical%20services.%20The%20Terms%20of%20Use%20are%20available%20on%20endlessmedical.com`);

    // Add symptoms
    await fetch(`https://api.endlessmedical.com/v1/dx/UpdateFeature?SessionID=${sessionID}&name=Age&value=${age}`);
    await fetch(`https://api.endlessmedical.com/v1/dx/UpdateFeature?SessionID=${sessionID}&name=BodyTemperature&value=${temp}`);

    // Analyze symptoms
    let analyzeResponse = await fetch(`https://api.endlessmedical.com/v1/dx/Analyze?SessionID=${sessionID}`);
    let analyzeData = await analyzeResponse.json();

    res.json(analyzeData);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
