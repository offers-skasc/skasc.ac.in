from flask import Flask, render_template_string
import os
app = Flask(__name__)

@app.route("/")
def google_form():
    center_lat = 10.9393171   # Center latitude
    center_lng = 76.9589776  # Center longitude
    default_radius = 10000    # Default radius in meters

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Hall Attendance Verification</title>
        <style>
            #location-display {{
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(255, 255, 255, 0.9);
                padding: 10px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                font-family: Arial, sans-serif;
                font-size: 14px;
                z-index: 999;
            }}
            #form-container iframe {{
                border: none;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                width: 100%;
                max-width: 700px;
                height: 520px;
            }}
            #form-container h2 {{
                text-align: center;
                font-family: Arial, sans-serif;
                color: #333;
            }}
        </style>
        <script>
            const centerLat = {center_lat};
            const centerLng = {center_lng};
            let maxDistance = {default_radius};

            function toRadians(degrees) {{
                return degrees * (Math.PI / 180);
            }}

            function calculateDistance(lat1, lng1, lat2, lng2) {{
                const R = 6371000; 
                const dLat = toRadians(lat2 - lat1);
                const dLng = toRadians(lng2 - lng1);
                const a = 
                    Math.sin(dLat/2) * Math.sin(dLat/2) +
                    Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
                    Math.sin(dLng/2) * Math.sin(dLng/2);
                const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
                return R * c;
            }}

            function displayLocation(lat, lng) {{
                const locationDisplay = document.getElementById('location-display');
                locationDisplay.textContent = `Your Location: Lat ${{lat.toFixed(6)}}, Lng ${{lng.toFixed(6)}}`;
            }}

            function checkAccess() {{
                const userAgent = navigator.userAgent || navigator.vendor || window.opera;
                console.log("User-Agent:", userAgent);
                if (/iPhone|iPad|iPod/i.test(userAgent)) {{
                    maxDistance = 1000;
                }}

                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(position => {{
                        const userLat = position.coords.latitude;
                        const userLng = position.coords.longitude;

                        displayLocation(userLat, userLng);
                        const distance = calculateDistance(centerLat, centerLng, userLat, userLng);

                        if (distance <= maxDistance) {{
                            document.getElementById('form-container').innerHTML = `
                                <iframe 
                                    src="https://forms.gle/yCEcPvpR66NB6QNK6"
                                    width="640" height="520" frameborder="0">
                                    Loading…
                                </iframe>`;
                        }} else {{
                            document.getElementById('form-container').innerHTML = `
                                <div style='text-align: center;'>
                                    <h2>Access Denied: You are not within the allowed location range.</h2>
                                    <p style="color:red;">If iPhone user: Enable "Precise Location" in Settings or Try Reloading the Page</p>
                                </div>`;
                        }}
                    }}, () => {{
                        document.getElementById('form-container').innerHTML = `
                            <div style='text-align: center;'>
                                <h2>Location access is required to access this form.</h2>
                                <p style="color:red;">If iPhone user: Use Chrome or Google app (avoid Safari)</p>
                            </div>`;
                    }});
                }} else {{
                    document.getElementById('form-container').innerHTML = "<h2>Geolocation is not supported by your browser.</h2>";
                }}
            }}

            document.addEventListener('DOMContentLoaded', checkAccess);
            console.log(maxDistance)
        </script>
    </head>
    <body>
        <div id="location-display">Detecting your location...</div>
        <div id="form-container" style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
            <h2>Loading...</h2>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)





















