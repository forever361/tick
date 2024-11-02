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
    job_name = request.form['job_name']
    job_detail = request.form['job_detail']

    if project_name in projects:
        # 如果项目中不存在该任务名称，则添加新任务
        if job_name not in projects[project_name]['jobs']:
            projects[project_name]['jobs'][job_name] = {
                "name": job_name,
                "detail": job_detail
            }
            save_jobs_data(projects)
            return jsonify({'status': 'success', 'jobs': projects[project_name]['jobs']})
        else:
            return jsonify({'status': 'error', 'message': '任务已存在'}), 400
    return jsonify({'status': 'error', 'message': '项目不存在'}), 404

@app.route('/delete_job', methods=['POST'])
def delete_job():
    project_name = request.form['project_name']
    job_name = request.form['job_name']

    if project_name in projects and job_name in projects[project_name]['jobs']:
        # 删除任务
        del projects[project_name]['jobs'][job_name]
        save_jobs_data(projects)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': '任务不存在或项目无效'}), 404


@app.route('/update-job', methods=['POST'])
def update_job():
    project_name = request.form['project_name']
    old_job_name = request.form['date']
    new_job_name = request.form['job_name']
    job_detail = request.form['job_detail']

    if project_name in projects and old_job_name in projects[project_name]['jobs']:
        projects[project_name]['jobs'].pop(old_job_name)
        projects[project_name]['jobs'][new_job_name] = {
            'detail': job_detail
        }
        save_jobs_data(projects)

    return '', 204  # 返回204表示无内容响应



@app.route('/get-job-detail', methods=['GET'])
def get_job_detail():
    project_name = request.args.get('project_name')
    date = request.args.get('date')

    if project_name in projects and date in projects[project_name]['jobs']:
        job = projects[project_name]['jobs'][date]
        return {
            'job_name': date,
            'job_detail': job['detail']
        }
    else:
        return {'error': '任务不存在'}, 404


if __name__ == '__main__':
    app.run(debug=True)
