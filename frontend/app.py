from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
import logging
import ssl
import socket

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configure session cookie
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict'
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s',
    filename='../logs/csc2330a3app.log',
    encoding='utf-8',
    level=logging.DEBUG
)

# User credentials
users = {
    'u1234567': 'csc2330a3',
    'student@usq.edu.au': 't12025'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        csrf_token = request.form.get('csrf_token', '')

        if csrf_token != session.get('csrf_token'):
            flash('Invalid CSRF token.')
            logging.info(f"SECURITY: CSRF token mismatch for username={username}")
            return redirect(url_for('login'))

        if users.get(username) == password:
            session['username'] = username
            session['csrf_token'] = secrets.token_hex(16)
            logging.info(f"SECURITY: Successful login: IP={request.remote_addr}, username={username}")
            return render_template('logged_in.html')
        else:
            flash('Invalid credentials.')
            logging.info(f"SECURITY: Unsuccessful login attempt: IP={request.remote_addr}, username={username}")
            return redirect(url_for('login'))
    else:
        session['csrf_token'] = secrets.token_hex(16)
        return render_template('login.html', csrf_token=session['csrf_token'])

@app.route('/logout')
def logout():
    username = session.get('username', 'Unknown')
    session.clear()
    logging.info(f"SECURITY: Logout: IP={request.remote_addr}, username={username}")
    return render_template('logged_out.html')



@app.route('/restricted', methods=['GET', 'POST'])
def restricted():
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token', '')
        if csrf_token != session.get('csrf_token'):
            flash('Invalid CSRF token.')
            logging.info(f"SECURITY: CSRF token mismatch on aphorism request: IP={request.remote_addr}, username={session['username']}")
            return redirect(url_for('login'))

        aphorism = get_aphorism()
        logging.info(f"SECURITY: Aphorism requested: IP={request.remote_addr}, username={session['username']}")
        return render_template('aphorisms.html', aphorism=aphorism)
    else:
        return render_template('restricted.html', csrf_token=session['csrf_token'])


def get_aphorism():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(r'C:\Users\welcome\Downloads\csc2330_2025_a3\csc2330_2025_a3\backend\certs\ca.crt')  # Trust the backend CA
    context.load_cert_chain(
        certfile=r'C:\Users\welcome\Downloads\csc2330_2025_a3\csc2330_2025_a3\backend\certs\backend.crt',
        keyfile=r'C:\Users\welcome\Downloads\csc2330_2025_a3\csc2330_2025_a3\backend\certs\backend.key'
    )
    context.check_hostname = False  # Disable if cert is for localhost

    with socket.create_connection(('localhost', 8443)) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            ssock.sendall(b"GET /aphorism")
            return ssock.recv(1024).decode()


if __name__ == '__main__':
    app.run(ssl_context=('certs/www.crt', 'certs/www.key'), host='127.0.0.1', port=5000, debug=True)
