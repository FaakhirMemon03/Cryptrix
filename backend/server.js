const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');

// Initialize Firebase Admin (requires serviceAccountKey.json)
// admin.initializeApp({
//   credential: admin.credential.cert(require('./serviceAccountKey.json')),
//   databaseURL: "https://cryptrix-backend.firebaseio.com"
// });

const app = express();
app.use(express.json());
app.use(cors());

// Endpoint to send commands to the PC agent
app.post('/send-command', async (req, res) => {
    const { deviceId, action, params } = req.body;

    if (!deviceId || !action) {
        return res.status(400).send({ error: 'Missing deviceId or action' });
    }

    try {
        // In a real scenario, we'd write this to Firestore where the agent is listening
        // await admin.firestore().collection('commands').add({
        //     deviceId,
        //     action,
        //     params: params || {},
        //     timestamp: admin.firestore.FieldValue.serverTimestamp(),
        //     status: 'pending'
        // });

        console.log(`Command ${action} sent to ${deviceId}`);
        res.status(200).send({ message: 'Command sent successfully' });
    } catch (error) {
        console.error('Error sending command:', error);
        res.status(500).send({ error: 'Internal Server Error' });
    }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Cryptrix Backend listening on port ${PORT}`);
});
