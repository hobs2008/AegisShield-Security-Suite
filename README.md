# AegisShield | Zero-Trust Cybersecurity Suite

A lightweight, high-impact cybersecurity web application demonstrating Zero-Trust Multi-Factor Authentication (MFA), symmetric encryption, data integrity hashing, and real-time password entropy analysis.

## 🚀 Key Modules & Features

1. **Zero-Trust MFA Portal:** Dynamic TOTP QR Code challenge-response system synced with Google Authenticator (RFC 6238).
2. **Duress / Panic Override:** Anti-forensics protocol (`999999`) that hides live vault data and triggers a scrubbed interface under coercion.
3. **AES-256 Text Encryptor:** Symmetric encryption module built on cryptographic standards.
4. **SHA-256 Hash Guard:** Data integrity verifier for digital forensics and file hashing.
5. **Password Entropy Analyzer:** Real-time client-side password strength and breach risk evaluator.

## 🛠️ Local Setup

```bash
# Install dependencies
pip install flask pyotp qrcode pillow cryptography

# Launch local server
python app.py

