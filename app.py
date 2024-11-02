from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 模拟数据
projects = {
    '英语': {
        'jobs': ['1', '2', '3', '4', '5','6','7','8','9','10','11','12'],
        'completed_dates': []
    },
    '健身': {
        'jobs': ['1', '2', '3', '4', '5','6','7','8','9','10'],
        'completed_dates': []
    }
}


@app.route('/')
def index():
    return render_template('index.html', projects=projects)


@app.route('/update', methods=['POST'])
def update():
    date = request.form['date']
    project_name = request.form['project_name']

    if date in projects[project_name]['jobs'] and date not in projects[project_name]['completed_dates']:
        projects[project_name]['completed_dates'].append(date)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)