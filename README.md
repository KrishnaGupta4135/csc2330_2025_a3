
# CSC2330 Assignment 3: Securing Networked Applications

## Overview

This assignment is part of CSC2330 - Securing Networked Applications. It involves developing a secure client-server web application using Python 3, Flask, shell scripting, and HTML5, runnable on the course's Debian virtual machines.

The application includes:
- A Flask-based front-end with login/logout and restricted access functionality.
- A Python-based back-end server that returns aphorisms from *The Zen of Python*.
- TLS encryption and certificate validation for secure communication.
- CSRF protection and secure session handling.
- Logging of security-relevant events.

---

## Repository Information

**Repository Name:** `csc2330_2025_a3`  
**Collaborators Added:** Zhongwei Zhang, James Northway, Ron Addie

---

## 📁 File Structure

```
.
├── backend_server/          # TLS socket server
│   ├── server.py            # Custom TCP server handling secure communication
│   └── ...
├── frontend_flask/          # Flask web frontend
│   ├── app.py               # Main Flask app
│   ├── templates/
│   └── static/
├── certs/                   # SSL/TLS Certificates
│   ├── server.crt
│   ├── server.key
│   ├── frontend.crt
│   ├── frontend.key
│   ├── backend.crt
│   ├── backend.key
│   └── ca.crt
├── logs/                    # Security logs
│   └── server.log
├── scripts/                 # Shell scripts for setup
│   └── run.sh
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
└── part2_essay.docx         # Written response for Part 2
```


---

## Credentials

The application accepts the following credentials for login:

1. **Username:** u1234567  
   **Password:** csc2330a3

2. **Username:** student@usq.edu.au
   **Password:** t12025

---

## Application Features Implemented
- 🔐 Secure login and logout with session management
- 🔁 CSRF token protection on sensitive routes
- 📜 Flask session cookie flags: Secure, HttpOnly, SameSite=Strict
- 🔐 TLS using self-signed certificates and mutual verification
- 🧾 Logging of login attempts and aphorism requests with user/IP info
- ✅ Aphorism retrieval only for authenticated sessions
- 🗂️ Git used consistently with meaningful commit messages

### Front-end Flask Application

- `/login` (GET/POST): Login page and form handling.
- `/logout` (GET): Logs the user out and destroys the session.
- `/restricted` (GET/POST): Displays aphorism request form (GET) and processes CSRF-protected aphorism requests (POST).

### Back-end Server

- Receives requests from the front-end and responds with aphorisms.
- TLS encrypted and validates front-end client certificate signed by CA.

---

## Security Features

- All user input is sanitized and escaped.
- CSRF tokens generated with `secrets.token_hex(16)`.
- Session cookies are:
  - Secure
  - HttpOnly
  - SameSite=Strict
- TLS with:
  - AES-256 encryption
  - RSA 2048/4096-bit keys
  - Mutual certificate validation via CA
- Logging of all auth and aphorism request events to `csc2330a3app.log`.

---

## TLS Certificate Files

Include the following certificates/keys in the root folder:

- `www.crt` — Self-signed for HTTPS front-end
- `ca.crt` — Certificate Authority
- `frontend.crt` — Signed front-end cert
- `backend.crt` — Signed back-end cert
- `frontend.key` — Front-end private key
- `backend.key` — Back-end private key
- `ca.key` — CA private key

---

## Running the Application

From the course Debian VM, execute the following:

### 1. Start the back-end server:
```bash
python3 server.py
```

### 2. Start the front-end Flask app:
```bash
python3 app.py
```

### 3. Use browser or integration script to test:
- Navigate to: `https://localhost:5000/login`

---

## Requirements

- Python 3
- Flask
- `ssl`, `logging`, `secrets`, `socket`
- HTML5 for frontend forms
- Debian 12 environment as provided

---

## Logs

All security events are logged in:
```
csc2330a3app.log
```

Example log line:
```
2025-04-25 12:00:00,001:INFO:SECURITY: IP 127.0.0.1 failed to log in with username u1234567
```

---

## Part 2: Reflective Essay (Brief)

This project deepened my understanding of securing web applications beyond basic authentication. Implementing TLS manually via sockets highlighted real-world challenges in certificate handling. CSRF protection reminded me of how seemingly small vulnerabilities can open doors to attacks. The layered approach—from socket security to Flask form validation—demonstrates how defense in depth plays a critical role in real-world web app development.

---

## 📚 References

- *Foundations of Python Network Programming* – John Goerzen, Brandon Rhodes
- Flask Docs: https://flask.palletsprojects.com/
- Flask-WTF: https://flask-wtf.readthedocs.io/
- OpenSSL: https://www.openssl.org/

See `part2_essay.docx` in this submission for analysis of:
- CSRF
- XSS
- Man-in-the-middle attacks

---

## Git History

- Used UniSQ Gitea server
- Repository: `csc2330_2025_a3`
- > 10 commits with meaningful messages

---

## Author

- Name: [Your Full Name]
- Student ID: u1234567
- Email: [student-email]@usq.edu.au

---

## Submission

Submitted as a `.zip` file via Study Desk, containing:

- Source code for front-end and back-end
- TLS certificates and keys
- `part2_essay.docx`
- This `README.md`

