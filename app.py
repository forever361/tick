from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# 模拟数据
projects = {
    '英语': {
        'jobs': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        'completed_dates': []
    },
    '健身': {
        'jobs': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
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

    # 检查日期是否在已完成的列表中
    if date in projects[project_name]['completed_dates']:
        projects[project_name]['completed_dates'].remove(date)  # 取消勾选
    else:
        projects[project_name]['completed_dates'].append(date)  # 勾选

    return redirect(url_for('index'))


@app.route('/add_job', methods=['POST'])
def add_job():
    project_name = request.form['project_name']
    job = request.form['job']
    if project_name in projects and job not in projects[project_name]['jobs']:
        projects[project_name]['jobs'].append(job)
    return jsonify({'status': 'success', 'jobs': projects[project_name]['jobs']})


@app.route('/delete_job', methods=['POST'])
def delete_job():
    project_name = request.form['project_name']
    job = request.form['job']
    if project_name in projects and job in projects[project_name]['jobs']:
        projects[project_name]['jobs'].remove(job)
    return jsonify({'status': 'success', 'jobs': projects[project_name]['jobs']})


if __name__ == '__main__':
    app.run(debug=True)
