"""
CoreInventory — Email Configuration
=====================================
Configure your Gmail SMTP settings here for OTP password reset emails.

HOW TO SET UP:
1. Go to https://myaccount.google.com/apppasswords
2. Generate a 16-character App Password for "Mail"
3. Paste your Gmail address and the 16-char App Password below
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ⬇️  PUT YOUR GMAIL ADDRESS HERE  ⬇️
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAIL_USERNAME = "donotreplycattlesense@gmail.com"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ⬇️  PUT YOUR 16-CHARACTER APP PASSWORD HERE  ⬇️
#  Example: "abcd efgh ijkl mnop" (without quotes, spaces are fine)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAIL_PASSWORD = "pbcswpuexsezphfp"


# ─────────────────────────────────────────────
#  DO NOT CHANGE ANYTHING BELOW THIS LINE
# ─────────────────────────────────────────────
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = MAIL_USERNAME
