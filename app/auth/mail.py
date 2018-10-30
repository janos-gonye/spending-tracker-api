from flask import url_for, current_app as app, request
from flask_mail import Message

from app.mail import mail


def send_reg_confirm_mail(recipient, token):
	"""
	token as string decoded to utf-8
	"""						  # remove the first '/' character
	link = request.url_root + url_for('auth.confirm_registration')[1:] + '?token=%s' % token

	msg = Message(
		subject='Spending Tracker - Activate your registration',
		recipients=[recipient],
		html=(
			"<header>"
			"<h3>Spending Tracker - Activate your registration</h3>"
			"<p>You've received this email because you've signed up for Spending Tracker.</p>"
			"</header>"
			"<main>"
			"<p>Click <em><a href='%s'>this link</a></em> to active your registration.</p>"
			"<p>or copy</p>"
			"<hr>"
			"<em>%s</em>"
			"<hr>"
			"<p>to your URL bar and hit enter.</p>"
			"</main>"
			"<footer>"
			"<p><small>If you haven't registered at Spending Tracker, ignore this email and feel free to remove it. We're sorry to bother you :)</small></p>"
			"</footer>"
		) % (link, link)
	)
	mail.send(msg)


def send_reg_confirmed_mail(recipient):
	pass