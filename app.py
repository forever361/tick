from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 模拟数据
projects = {
    '英语': {
        'dates': ['2024-11-01', '2024-11-02', '2024-11-03', '2024-11-04', '2024-11-05'],
        'completed_dates': []
    },
    '健身': {
        'dates': ['2024-11-01', '2024-11-02', '2024-11-03', '2024-11-04', '2024-11-05'],
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

    if date in projects[project_name]['dates'] and date not in projects[project_name]['completed_dates']:
        projects[project_name]['completed_dates'].append(date)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)