from flask_mail import Message

from app.mail import mail


def send_statistics_export_mail(recipient, attachments):
    msg = Message(
        subject="Spending Tracker - Statistics Exported",
        recipients=[recipient],
        html=(
            "<header>"
            "<h3>Spending Tracker - Statistics Exported</h3>"
            "</header>"
            "<main>"
            "<p>Statistics Exported</p>"
            "</main>"
            "<footer>"
            "<small>"
            "<p>If you've received this email and haven't initiated the "
            "exportation of your statistics, "
            "change your Spending Tracker password as soon as possible!</p>"
            "</small>"
            "</footer>"
        )
    )
    for attachment in attachments:
        msg.attach(filename=attachment['filename'],
                   content_type=attachment['content_type'],
                   data=attachment['data'])
    mail.send(msg)
