from flask import Flask, render_template, request, flash, redirect, url_for
import os
import smtplib
from email.message import EmailMessage


# --------------------------------------------------
# Debug: Check Flask's current folder and static files
# --------------------------------------------------
print("Current folder:", os.getcwd())
print("Static folder:", os.path.abspath("static"))

if os.path.exists("static"):
    print("Static files:", os.listdir("static"))
    print("Profile image exists:", os.path.exists("static/profile.jpeg"))
else:
    print("ERROR: static folder does not exist!")


# --------------------------------------------------
# Flask application
# --------------------------------------------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Used for Flask flash messages
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)


# --------------------------------------------------
# Home page
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Contact form
# --------------------------------------------------
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in all fields.", "error")
        return redirect(url_for("home") + "#contact")

    # Email configuration comes from environment variables.
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    contact_email = os.environ.get("CONTACT_EMAIL")

    # If email settings aren't configured yet,
    # save the message locally.
    if not all([
        smtp_host,
        smtp_user,
        smtp_password,
        contact_email
    ]):
        with open("messages.txt", "a", encoding="utf-8") as file:
            file.write(
                f"\n--- New Message ---\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Message: {message}\n"
            )

        flash(
            "Thank you! Your message has been received.",
            "success"
        )

        return redirect(url_for("home") + "#contact")

    # Send email
    try:
        msg = EmailMessage()

        msg["Subject"] = f"Portfolio Contact: {name}"
        msg["From"] = smtp_user
        msg["To"] = contact_email
        msg["Reply-To"] = email

        msg.set_content(
            f"""
You received a new portfolio message.

Name: {name}
Email: {email}

Message:
{message}
"""
        )

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        flash("Message sent successfully!", "success")

    except Exception:
        flash(
            "Sorry, something went wrong while sending your message.",
            "error"
        )

    return redirect(url_for("home") + "#contact")


# --------------------------------------------------
# Run Flask
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )