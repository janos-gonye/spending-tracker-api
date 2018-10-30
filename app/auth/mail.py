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
		# !Don't add href attr to the link, because e.g. gmail redirects to it through www.google.hu?q=<link>
		html=(
			"<header>"
			"<h3>Spending Tracker - Activate your registration</h3>"
			"<p>You've received this email because you've signed up for Spending Tracker.</p>"
			"</header>"
			"<main>"
			"<p>Copy this link</p>"
			"<hr>"
			"<em><a>%s</a></em>"
			"<hr>"
			"<p>to your URL bar and hit enter.</p>"
			"</main>"
			"<footer>"
			"<p><small>If you haven't registered at Spending Tracker, ignore this email and feel free to remove it. We're sorry to bother you :)</small></p>"
			"</footer>"
		) % link
	)
	mail.send(msg)


def send_reg_confirmed_mail(recipient):
	msg = Message(
		subject='Spending Tracker - Registration activated',
		recipients=[recipient],
		html=(
			"<header>"
			"<h3>Spending Tracker - Registration activated</h3>"
			"</header>"
			"<main>"
			"<p>Your registration for Spending Tracker has been activated. Enjoy! ;)</p>"
			"</main>"
			"<footer>"
			"<small>"
			"<p>"
			"If you haven't registered at Spending Tracker, please contact "
			'<a href="mailto:{}?Subject=Unwanted%20Registration&body=Hello%20Johnny!\n\nI%20have%20not%20registered%20at%20Spending%20Tracker.\n\nPlease%20remove%20my%20account!">me</a> and change your password as soon as possible!'
			"</p>"
			"</small>"
			"</footer>"
		).format(app.config['MAIL_DEFAULT_SENDER'])
	)
	mail.send(msg)
