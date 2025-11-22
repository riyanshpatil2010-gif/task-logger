from flask import Flask, render_template, request, redirect, send_from_directory, abort
import csv
import os

print("Starting Task Logger Application...")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))

def calculate_total_time():
    total_time = 0
    if os.path.isfile("task_log.csv"):
        with open("task_log.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                total_time += float(row[1])
    return total_time

@app.route('/')
def home():
    total_time = calculate_total_time()
    return render_template('home.html', total_time=total_time)

@app.route('/log', methods=['GET', 'POST'])
def log_task():
    if request.method == 'POST':
        task = request.form['task']
        time_spent = request.form['time_spent']

        file_exists = os.path.isfile("task_log.csv")

        with open("task_log.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Task", "Time Spent (minutes)"])
            writer.writerow([task, time_spent])

        return redirect('/')

    return render_template('log_task.html')

@app.route('/view')
def view_tasks():
    tasks = []
    if os.path.isfile("task_log.csv"):
        with open("task_log.csv", mode="r") as file:
            reader = csv.reader(file)
            tasks = list(reader)

    return render_template('view_tasks.html', tasks=tasks)

@app.route('/files/<path:filename>')
def download_file(filename):
    if filename != "task_log.csv":
        abort(403)  # Forbidden
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    if os.path.isfile("task_log.csv"):
        with open("task_log.csv", mode="r") as file:
            reader = list(csv.reader(file))

        if 0 < task_index < len(reader):
            del reader[task_index]

            with open("task_log.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(reader)

    return redirect('/view')

if __name__ == '__main__':
    app.run(debug=True)