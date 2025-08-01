from flask import Flask
from routes import setup_routes
from engine import run_lockdown_cycle
from zip_guardian_daemon import watch_loop as zip_loop
from rico_trigger_engine import watch_loop as rico_loop
import threading, schedule, time, os

app = Flask(__name__)
setup_routes(app)

def launch_thread(fn):
    t = threading.Thread(target=fn)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    run_lockdown_cycle()
    launch_thread(zip_loop)
    launch_thread(rico_loop)
    port = int(os.environ.get("PORT", 10000))
    launch_thread(lambda: app.run(host='0.0.0.0', port=port))
    while True:
        schedule.run_pending()
        time.sleep(60)
