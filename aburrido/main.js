const WebSocket = require('ws');
const fetch = require('node-fetch'); // Asegúrate de instalar 'node-fetch' con `npm install node-fetch`

const APP_ID = "8S4A1bRFg19ziD6XpXJw08oBjDx7UMZOH68jVj9r"; // Reemplaza con tu APP_ID
const REST_API_KEY = "4jRpVR7TAGD1mD0v3rUmdbFdvzsa2CHtTyWSfVtW"; // Reemplaza con tu REST_API_KEY
const BASE_URL = " https://parseapi.back4app.com";

const server = new WebSocket.Server({ port: 8080 });

server.on('connection', (socket) => {
    console.log('Cliente conectado.');

    socket.on('message', async (message) => {
        console.log('Mensaje recibido:', message);

        // Parsear el mensaje recibido
        let parsedMessage;
        try {
            parsedMessage = JSON.parse(message);
        } catch (error) {
            console.error('Error al parsear el mensaje:', error);
            return;
        }

        // Manejar diferentes tipos de mensajes
        if (parsedMessage.type === 'saveDrawing') {
            // Guardar un dibujo en Back4App
            const drawingData = parsedMessage.data;
            await saveDrawingToBack4App(drawingData);
        }

        // Reenvía el mensaje a todos los clientes conectados
        server.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    });

    socket.on('close', () => {
        console.log('Cliente desconectado.');
    });
});

console.log('Servidor WebSocket ejecutándose en ws://localhost:8080');

// Función para guardar un dibujo en Back4App
async function saveDrawingToBack4App(drawingData) {
    try {
        const response = await fetch(`${BASE_URL}/Drawing`, {
            method: 'POST',
            headers: {
                'X-Parse-Application-Id': APP_ID,
                'X-Parse-REST-API-Key': REST_API_KEY,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(drawingData),
        });

        const result = await response.json();
        console.log('Dibujo guardado en Back4App:', result);
    } catch (error) {
        console.error('Error al guardar el dibujo en Back4App:', error);
    }
}
