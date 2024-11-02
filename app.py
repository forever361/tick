import json
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# 读取 JSON 文件
def load_jobs_data():
    if os.path.exists('jobs.json'):
        with open('jobs.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 保存 JSON 文件
def save_jobs_data(data):
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 加载项目数据
projects = load_jobs_data()



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

    # 保存更新后的数据
    save_jobs_data(projects)

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
