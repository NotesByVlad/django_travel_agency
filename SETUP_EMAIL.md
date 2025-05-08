# 📧 Email Setup (Gmail SMTP) for Django

This project uses Gmail to send emails for password resets and registration verification.

To use it in development:

---

## ✅ Step 1: Enable 2-Step Verification

1. Go to: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Under **"Signing in to Google"**, turn on **2-Step Verification**
3. Complete the setup with your phone number or another method

---

## ✅ Step 2: Generate an App Password

1. Go to: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select **"Mail"** as the app
3. Choose **"Other"**, and type something like: `Django Project`
4. Click **Generate**
5. Copy the 16-character password (no spaces)

> ⚠️ You will only see this password once — copy it immediately.

---

## ✅ Step 3: Create a `.env` File

In the root of the project, create a `.env` file with the following:

```ini
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_char_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
