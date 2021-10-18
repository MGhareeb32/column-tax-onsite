from flask import render_template, Flask, request, url_for
from werkzeug.utils import redirect

import forms
from db import init_db

app = Flask(__name__)
init_db(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.values)
    user_id = request.values.get('user_id')
    step_id = request.values.get('step_id')
    if step_id not in forms.step_id_to_form:
        if request.method == 'POST':
            next_step_id = forms.find_next_step_for_user(user_id, None)
            next_url = url_for('.index', step_id=next_step_id, user_id=user_id)
            return redirect(next_url)
        else:
            return render_template('home.html')
    else:
        response = {
            'error_messages': [],
            'tax': forms.get_taxes(user_id)
        }
        if request.method == 'POST':
            forms.process_form_submission(
                user_id,
                step_id,
                request.values.get('user_selection'),
                response)
            if len(response['error_messages']) == 0:
                next_step_id = forms.find_next_step_for_user(user_id, step_id)
                next_url = url_for('.index', step_id=next_step_id, user_id=user_id)
                return redirect(next_url)
            else:
                return render_template(
                    forms.step_id_to_form[step_id],
                    response=response)
        elif request.method == 'GET':
            forms.build_form_payload(user_id, step_id, response)
            return render_template(
                forms.step_id_to_form[step_id],
                response=response)


if __name__ == '__main__':
    app.run(debug=True)
