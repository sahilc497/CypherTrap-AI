from fastapi import APIRouter, Request, Depends, Body
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from backend.database.config import get_db
from backend.models.threat import Session as AttackerSession
from backend.services.session_manager import SessionManager
import hashlib

router = APIRouter()

@router.get("/admin-verify", response_class=HTMLResponse)
async def decoy_verify_page():
    """
    Decoy Verification Page designed to capture attacker's face and exact location.
    Looks like a high-security admin login verification.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Identity Verification | Secure Admin</title>
        <style>
            body { background: #0a0a0c; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #111; padding: 2rem; border-radius: 1rem; border: 1px solid #333; text-align: center; max-width: 400px; }
            .btn { background: #00f2ff; color: black; border: none; padding: 1rem 2rem; border-radius: 0.5rem; font-weight: bold; cursor: pointer; margin-top: 1rem; }
            .status { margin-top: 1rem; font-size: 0.8rem; color: #888; }
            video { display: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="color: #00f2ff;">Security Verification</h2>
            <p>To access the sensitive database, you must complete biometric and location verification.</p>
            <button class="btn" onclick="startVerification()">Verify Identity</button>
            <div id="status" class="status">Waiting for user action...</div>
            <video id="video" width="320" height="240" autoplay></video>
            <canvas id="canvas" style="display:none;"></canvas>
        </div>

        <script>
            async function startVerification() {
                const status = document.getElementById('status');
                
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    status.innerHTML = "<span style='color: #ff4444;'>ERROR: Browser restricted camera access. Please use <b>localhost</b> or <b>HTTPS</b>.</span>";
                    return;
                }

                status.innerText = "Requesting biometric access...";
                
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    const video = document.getElementById('video');
                    video.srcObject = stream;
                    
                    status.innerText = "Scanning face... please wait...";
                    await new Promise(r => setTimeout(r, 1500));
                    
                    const canvas = document.getElementById('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    const imageData = canvas.toDataURL('image/jpeg');
                    
                    stream.getTracks().forEach(track => track.stop());

                    status.innerText = "Verifying physical location...";
                    navigator.geolocation.getCurrentPosition(async (pos) => {
                        const intel = {
                            image: imageData,
                            lat: pos.coords.latitude,
                            lon: pos.coords.longitude
                        };
                        
                        status.innerText = "Uploading forensic package to SOC...";
                        const response = await fetch('/api/decoy/capture', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(intel)
                        });
                        
                        if (response.ok) {
                            status.innerHTML = "<span style='color: #00ff00;'>Forensic package uploaded successfully!</span>";
                            setTimeout(() => {
                                window.location.href = "/api/decoy/explorer";
                            }, 2000);
                        } else {
                            status.innerText = "Upload failed. Server unreachable.";
                        }
                        
                    }, (err) => {
                        status.innerHTML = "<span style='color: #ffbb00;'>Location denied. Using IP-based fallback...</span>";
                        setTimeout(async () => {
                            await fetch('/api/decoy/capture', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ image: imageData })
                            });
                            window.location.href = "/api/vuln/db";
                        }, 2000);
                    });

                } catch (err) {
                    status.innerHTML = "<span style='color: #ff4444;'>Camera Error: " + err.message + "</span>";
                }
            }
        </script>
    </body>
    </html>
    """

@router.get("/explorer", response_class=HTMLResponse)
async def decoy_explorer():
    """
    The landing page after verification. Looks like a restricted DB explorer.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Control Panel | Restricted Data</title>
        <style>
            body { background: #070709; color: #aaa; font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
            .header { border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; }
            .sidebar { width: 200px; border-right: 1px solid #333; height: 100vh; position: fixed; }
            .main { margin-left: 220px; }
            .table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            .table th, .table td { border: 1px solid #222; padding: 12px; text-align: left; font-size: 0.8rem; }
            .table th { background: #111; color: #00f2ff; }
            .active { color: #00f2ff; }
            .tag { background: #1a1a1a; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; color: #ff4444; }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h4 class="active">📊 Tables</h4>
            <div style="padding-left: 10px; line-height: 2;">
                <div>- users <span class="tag">SECURED</span></div>
                <div class="active">- transactions</div>
                <div>- logs_legacy</div>
                <div>- sys_config</div>
                <div>- api_keys <span class="tag">ENCRYPTED</span></div>
            </div>
        </div>
        <div class="main">
            <div class="header">
                <span class="active">DB_SESSION: B745-992X-SYSTEM</span>
                <span>Role: DB_ADMIN (Read/Write)</span>
            </div>
            <h3>SELECT * FROM transactions LIMIT 5;</h3>
            <table class="table">
                <thead>
                    <tr><th>id</th><th>user_id</th><th>amount</th><th>status</th><th>hash</th></tr>
                </thead>
                <tbody>
                    <tr><td>1029</td><td>usr_992</td><td>$4,200.00</td><td>COMPLETED</td><td>0x7f88...2a1</td></tr>
                    <tr><td>1030</td><td>usr_114</td><td>$12,50.00</td><td>PENDING</td><td>0x11a2...99b</td></tr>
                    <tr><td>1031</td><td>usr_007</td><td>$99.99</td><td>COMPLETED</td><td>0x88c1...33e</td></tr>
                    <tr><td>1032</td><td>usr_245</td><td>$1,120,000.00</td><td>FLAGGED</td><td>0xbb22...001</td></tr>
                </tbody>
            </table>
            <p style="margin-top: 40px; color: #444;">[SYSTEM] Real-time session monitoring active. Integrity Check: PASSED.</p>
        </div>
    </body>
    </html>
    """

@router.post("/capture")
async def capture_intel(request: Request, intel: dict = Body(...), db: Session = Depends(get_db)):
    """
    Receives captured face and location data from the decoy page.
    """
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")
    session_key = hashlib.md5(f"{ip}:{user_agent}".encode()).hexdigest()
    
    session = db.query(AttackerSession).filter(AttackerSession.session_id == session_key).first()
    
    if session:
        session.captured_face_url = intel.get("image")
        session.latitude = intel.get("lat")
        session.longitude = intel.get("lon")
        session.risk_level = "High" # Automatic High Risk if they fall for the honey-camera
        db.commit()
        
    return {"status": "verified"}
