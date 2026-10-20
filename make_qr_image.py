import qrcode
import os

# Create a QR code pointing to the local HTML file or a hosted link
# (For remote messaging, host the HTML on GitHub Pages or send the file directly)
qr_data = "https://github.com/lovelaceyrae11/bloom_whitepaper" # Replace with your link or file path if hosted
img = qrcode.make(qr_data)
img.save("earth_proof_qr.png")
print("[✓] QR code image saved as 'earth_proof_qr.png' in your folder!")
