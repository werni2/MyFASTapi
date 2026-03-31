class Client {
    
    constructor() {
        this.watchId = null;
        this.counter = 0;
        this.sessionElm = null;
        this.clientElm = null;
        this.longitudeElm = null;
        this.latitudeElm = null;
        this.speedElm = null;
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

    async joinSession(baseURL, session_id, client_id, longitude_id, latitude_id, speed_id) {

        this.sessionElm = document.getElementById(session_id); 
        this.clientElm = document.getElementById(client_id);
        this.longitudeElm = document.getElementById(longitude_id);
        this.latitudeElm = document.getElementById(latitude_id);
        this.speedElm = document.getElementById(speed_id);

        if (!this.sessionElm || !this.clientElm ||!this.longitudeElm || !this.latitudeElm || !this.speedElm) {
            throw new Error("Ein oder mehrere HTML-Elemente konnten nicht gefunden werden.");
        }

        const response = await fetch(`${baseURL}/timing_sessions/${this.sessionElm.value}/clients`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ client_name: this.clientElm.value })
        });
        
        if (!response.ok) {
            throw new Error("Fehler beim Beitreten der Session.");
        }

        this.startUpdateTimer(baseURL);
    }

    startUpdateTimer(baseURL) {
        // Falls schon ein Timer läuft → stoppen
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        this.updateInterval = setInterval(() => {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    console.log("send update with position:", pos);
                    this.sendUpdate(baseURL, pos);
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

    async sendUpdate(baseURL, position) {
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
                `${baseURL}/timing_sessions/${this.sessionElm.value}/client/${this.clientElm.value}`,
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

            // TimingClientStateModel
            const result = await response.json();

            console.log("Server-Result:", result);

            // Aktualisiere die UI mit den neuen Werten
            if (this.longitudeElm) {
                this.longitudeElm.textContent = result.longitude;
            }
            if (this.latitudeElm) {
                this.latitudeElm.textContent = result.latitude;
            }
            if (this.speedElm) {
                this.speedElm.textContent = result.speed;
            }

            return result;

        } catch (err) {
            console.error("Netzwerkfehler beim Update:", err);
            return null;
        }
    }
}

window.client = new Client();



