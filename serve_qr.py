# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import http.server
import socket
import socketserver
import os
import qrcode

PORT = 8080
os.chdir(os.path.expanduser("~/bloom_whitepaper"))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(('10.255.255.255', 1))
    local_ip = s.getsockname()[0]
except Exception:
    local_ip = '127.0.0.1'
finally:
    s.close()

url = f"http://{local_ip}:{PORT}/earth_proof_explainer.html"

print("\n" + "="*50)
print("     CASTLEBERRY BLOOM • LIVE QR PROOF SERVER     ")
print("="*50)
print(f"[*] URL: {url}\n")

qr = qrcode.QRCode(version=1, box_size=1, border=1)
qr.add_data(url)
qr.make(fit=True)
qr.print_ascii(invert=True)

print("\n[✓] Scan the QR code above with any nearby phone camera!")
print("[*] Press Ctrl+C to stop the server when finished.\n")
print("="*50 + "\n")

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")
