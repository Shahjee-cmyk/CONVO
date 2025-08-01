from flask import Flask, request, render_template_string, redirect
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'Referer': 'https://www.google.com/'
}

stop_events = {}
threads = {}
task_logs = {}
task_statuses = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                try:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = f"{mn} {message1}"
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)

                    success = response.status_code == 200
                    log_msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {'✅' if success else '❌'} Token ****: {message}"
                    task_logs[task_id].append(log_msg)

                    if success:
                        task_statuses[task_id]['valid'] += 1
                    else:
                        task_statuses[task_id]['invalid'] += 1
                        task_logs[task_id].append(f"Response: {response.status_code} - {response.text}")

                    time.sleep(time_interval)
                except Exception as e:
                    task_logs[task_id].append(f"[CRITICAL_ERROR] {str(e)}")
                    task_statuses[task_id]['status'] = 'ERROR'
                    stop_event.set()
                    break

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId').strip()
        if 'facebook.com' in thread_id:
            thread_id = thread_id.split('/')[-1].split('?')[0]

        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        if time_interval <= 0:
            return "⛔ Delay must be greater than 0", 400

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        stop_events[task_id] = Event()
        task_logs[task_id] = []
        task_statuses[task_id] = {
            'valid': 0,
            'invalid': 0,
            'start': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'ONLINE',
            'token_count': len(access_tokens)
        }

        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return redirect('/dashboard')

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>L3G3ND R9MBO</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    html, body {
      height: 100%;
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      background: url('https://i.ibb.co/wZc5CYmz/e681d54bce0782dcce41547236b0d19a.jpg') no-repeat center center fixed;
      background-size: cover;
      font-family: 'Segoe UI', sans-serif;
    }
    .form-container {
      background: rgba(173, 216, 230, 0.2);
      backdrop-filter: blur(15px);
      padding: 25px;
      border-radius: 15px;
      width: 100%;
      max-width: 500px;
      margin: 20px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
    }
    .form-control {
      background-color: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: #fff;
      border-radius: 8px;
      margin-bottom: 15px;
      padding: 10px;
    }
    h2 {
      text-shadow: 2px 2px 4px #000;
      color: white;
    }
    .fancy-button {
      position: relative;
      background: linear-gradient(135deg, #7f3eff, #4e6eff);
      color: white;
      border: none;
      padding: 14px 28px;
      font-size: 18px;
      font-weight: 600;
      border-radius: 20px;
      box-shadow: 0 5px 15px rgba(0, 0, 255, 0.4);
      cursor: pointer;
      overflow: hidden;
      transition: all 0.3s ease;
      width: 100%;
    }
    .fancy-button:hover {
      box-shadow: 0 0 25px rgba(0, 123, 255, 0.7);
      transform: scale(1.03);
    }
    .fancy-button .corner {
      position: absolute;
      top: 0;
      right: 0;
      width: 28px;
      height: 28px;
      background: linear-gradient(135deg, #fff, #4e6eff);
      border-top-right-radius: 20px;
      clip-path: polygon(100% 0, 0 0, 100% 100%);
      box-shadow: -3px 3px 5px rgba(0,0,0,0.2);
    }
    .btn-glow:hover {
      box-shadow: 0 0 12px 2px rgba(255, 255, 255, 0.8);
      transform: scale(1.02);
    }
  </style>
</head>
<body>
  <div class="form-container text-center">
    <h2 class="mb-4">♛𝕲𝐀𝐌𝐁𝐋𝐄𝐑 𝐑𝐔𝐋𝐋𝐄𝐗♛</h2>
    <form method="post" enctype="multipart/form-data">
      <select class="form-control" name="tokenOption" onchange="toggleTokenInput()" required>
        <option value="single">Single Token</option>
        <option value="multiple">Multiple Tokens</option>
      </select>
      <input type="text" class="form-control" id="singleToken" name="singleToken" placeholder="Enter Single Token">
      <input type="file" class="form-control" id="tokenFile" name="tokenFile" style="display:none;">
      <input type="text" class="form-control" name="threadId" placeholder="Group/Inbox Link" required>
      <input type="text" class="form-control" name="kidx" placeholder="Hater Name" required>
      <input type="number" class="form-control" name="time" placeholder="Delay in Sec (e.g. 3)" required>
      <input type="file" class="form-control" name="txtFile" required>
      <button type="submit" class="fancy-button mt-2">
        ⚡ Start Task
        <span class="corner"></span>
      </button>
    </form>
    <a href="/dashboard" class="btn btn-light mt-4 btn-glow">♻️ View All Tasks</a>
  </div>
  <script>
    function toggleTokenInput() {
      var tokenOption = document.querySelector('select[name="tokenOption"]').value;
      document.getElementById('singleToken').style.display = tokenOption === 'single' ? 'block' : 'none';
      document.getElementById('tokenFile').style.display = tokenOption === 'multiple' ? 'block' : 'none';
    }
    toggleTokenInput();
  </script>
</body>
</html>
''')

@app.route('/dashboard')
def dashboard():
    dashboard_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Task Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: url('https://i.ibb.co/wZc5CYmz/e681d54bce0782dcce41547236b0d19a.jpg') no-repeat center center fixed;
                background-size: cover;
                color: #fff;
                font-family: 'Segoe UI', sans-serif;
                padding: 20px;
            }
            .task-container {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                margin-bottom: 20px;
                padding: 20px;
                box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
            }
            .task-logs {
                background: rgba(0, 0, 0, 0.4);
                padding: 12px;
                border-radius: 10px;
                max-height: 200px;
                overflow-y: auto;
                font-size: 14px;
                color: #00ff9c;
                margin-top: 12px;
                font-family: monospace;
            }
            .btn-stop {
                background-color: #ff4444;
                border: none;
                padding: 10px 18px;
                color: white;
                border-radius: 6px;
                font-weight: 600;
                margin-top: 10px;
                box-shadow: 0 0 8px rgba(255, 0, 0, 0.4);
                transition: 0.3s ease;
            }
            .btn-stop:hover {
                background-color: #cc0000;
                box-shadow: 0 0 12px rgba(255, 0, 0, 0.6);
            }
            .status-online { color: #00ff9c; font-weight: bold; }
            .status-error { color: #ff4f4f; font-weight: bold; }
            .status-stopped { color: #cccccc; font-weight: bold; }
        </style>
    </head>
    <body>
        <h2 class="text-center mb-4">📊 𝕷𝐢𝐯𝐞 𝕯𝖆𝐬𝐡𝖇𝐨𝐚𝐫𝐝</h2>
        {% if statuses %}
            {% for tid, status in statuses.items() %}
                <div class="task-container">
                    <div class="row g-2">
                        <div class="col-12 col-md-6"><strong>🆔 Task ID:</strong> {{ tid }}</div>
                        <div class="col-12 col-md-6"><strong>Status:</strong> <span class="status-{{ status.status|lower }}">{{ status.status }}</span></div>
                        <div class="col-6 col-md-4"><strong>Tokens:</strong> {{ status.token_count }}</div>
                        <div class="col-6 col-md-4"><strong>✅ Valid:</strong> {{ status.valid }}</div>
                        <div class="col-6 col-md-4"><strong>❌ Invalid:</strong> {{ status.invalid }}</div>
                        <div class="col-12 col-md-6"><strong>🕒 Start:</strong> {{ status.start }}</div>
                        {% if status.get('end') %}
                            <div class="col-12 col-md-6"><strong>🔚 End:</strong> {{ status.end }}</div>
                        {% endif %}
                    </div>
                    {% if status.status != 'STOPPED' %}
                        <form method="POST" action="/stop">
                            <input type="hidden" name="taskId" value="{{ tid }}">
                            <button type="submit" class="btn-stop">🛑 Stop Task</button>
                        </form>
                    {% endif %}
                    <div class="task-logs mt-2">
                        {% for log in logs[tid][-10:] %}
                            {{ log }}<br>
                        {% endfor %}
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <p class="text-center">No running tasks found.</p>
        {% endif %}
        <div class="text-center">
            <a href="/" class="btn btn-light mt-3">💠 Back to Form</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(dashboard_html, statuses=task_statuses, logs=task_logs)

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        threads[task_id].join(timeout=1)
        task_statuses[task_id]['status'] = 'STOPPED'
        task_statuses[task_id]['end'] = time.strftime('%Y-%m-%d %H:%M:%S')
        del stop_events[task_id]
        del threads[task_id]
        return redirect('/dashboard')
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
