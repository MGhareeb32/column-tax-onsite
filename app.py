from flask import render_template, Flask, request

app = Flask(__name__)

step_id_to_form = {
    '1': 'form_pages/0_marital_status.html',
    '2': 'form_pages/00_number_of_children.html',
    '3': 'form_pages/1_state.html',
    '4': 'form_pages/2_income.html',
    'z': 'results.html',
}


@app.route('/', methods=['GET'])
def index():
    step_id = request.values.get('step_id')
    if step_id not in step_id_to_form:
        return render_template('home.html')
    else:
        return render_template(step_id_to_form[step_id])


if __name__ == '__main__':
    app.run(debug=True)
