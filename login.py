from flask import request, session, redirect, url_for, flash, render_template

from werkzeug.security import check_password_hash


class LogMain:

    def loginwindow(self):

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None
            user = ''

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

            flash(error)

        return render_template('login.html')
