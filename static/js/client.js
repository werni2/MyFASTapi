class Client {
    constructor() {
        this.watchId = null;
        this.counter = 0;
    }

    async GetGPSPosition() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error("Geolocation wird nicht unterstützt."));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({
                    lat: pos.coords.latitude,
                    lng: pos.coords.longitude
                }),
                (err) => reject(err)
            );
        });
    }

    StartAutoUpdate(latId, lngId, errorId, cntId) {
        const latElem = document.getElementById(latId);
        const lngElem = document.getElementById(lngId);
        const errElem = document.getElementById(errorId);
        const cntElem = document.getElementById(cntId);

        if (this.watchId !== null) {
            navigator.geolocation.clearWatch(this.watchId);
        }

        this.watchId = navigator.geolocation.watchPosition(
            (pos) => {
                this.counter++;

                latElem.textContent = pos.coords.latitude;
                lngElem.textContent = pos.coords.longitude;
                cntElem.textContent = this.counter;
            },
            (err) => {
                errElem.textContent = "Fehler: " + err.message;
            },
            {
                enableHighAccuracy: true,
                maximumAge: 0,
                timeout: 5000
            }
        );
    }

    StopAutoUpdate() {
        if (this.watchId !== null) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
    }

    async joinSession(baseURL, session_id, client_id) {
        const response = await fetch(`${baseURL}/timing_sessions/${session_id}/clients`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ client_name: client_id })
        });
        
        if (!response.ok) {
            throw new Error("Fehler beim Beitreten der Session.");
        }

        this.startUpdateTimer(baseURL, session_id, client_id);
    }

    startUpdateTimer(baseURL, session_id, client_id) {
        // Falls schon ein Timer läuft → stoppen
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        this.updateInterval = setInterval(() => {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    this.sendUpdate(baseURL, session_id, client_id, pos);
                },
                (err) => {
                    console.error("Geolocation-Fehler:", err);
                },
                {
                    enableHighAccuracy: true,
                    maximumAge: 0,
                    timeout: 5000
                }
            );
        }, 2000);
    }

    async sendUpdate(baseURL, session_id, client_id, position) {
        try {
            const body = {
                coords: {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy,
                    altitude: position.coords.altitude ?? null,
                    altitudeAccuracy: position.coords.altitudeAccuracy ?? null,
                    heading: position.coords.heading ?? null,
                    speed: position.coords.speed ?? null
                },
                timestamp: position.timestamp
            };

            const response = await fetch(
                `${baseURL}/timing_sessions/${session_id}/clients/${client_id}`,
                {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(body)
                }
            );

            if (!response.ok) {
                console.error("Update fehlgeschlagen:", response.status);
                return null;
            }

            // 🔥 Hier kommt dein UpdateClientResultModel an
            const result = await response.json();

            console.log("Server-Result:", result);

            // Beispiel-Auswertung:
            console.log("Neue Position:", result.latitude, result.longitude);
            console.log("Geschwindigkeit:", result.speed);

            return result;

        } catch (err) {
            console.error("Netzwerkfehler beim Update:", err);
            return null;
        }
    }
}

window.client = new Client();



