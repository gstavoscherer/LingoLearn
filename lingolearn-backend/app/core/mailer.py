import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to: str, subject: str, body: str, html_body: str | None = None):
    """
    Sends an email using SMTP with TLS encryption.
    Supports both plain text and HTML bodies.
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to

    text_part = MIMEText(body, "plain")
    msg.attach(text_part)

    if html_body:
        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            print(f"✅ Email sent successfully to {to}")

    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")
        raise


def build_reset_password_email(username: str, reset_link: str, expire_minutes: int) -> tuple[str, str]:
    subject = "Password Reset Request"
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 8px; padding: 20px;">
          <h2 style="color: #333;">Password Reset</h2>
          <p>Hello <strong>{username}</strong>,</p>
          <p>You requested to reset your password. Click the button below to set a new one.</p>
          <p style="text-align: center; margin: 30px 0;">
            <a href="{reset_link}" style="
              background-color: #007bff;
              color: white;
              padding: 12px 20px;
              text-decoration: none;
              border-radius: 6px;
              font-weight: bold;
            ">Reset Password</a>
          </p>
          <p>This link will expire in <strong>{expire_minutes} minutes</strong>.</p>
          <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
          <p style="font-size: 12px; color: #777;">If you did not request this, just ignore this email.</p>
        </div>
      </body>
    </html>
    """
    plain_body = f"""
    Hi {username},

    You requested to reset your password.
    Use the following link (valid for {expire_minutes} minutes):

    {reset_link}

    If you did not request this, please ignore this email.
    """

    return subject, plain_body if not html_body else html_body
