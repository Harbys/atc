import daemonize
import time
import sys
import os
import signal
import Config
import KeepassManager


def main():
    config = Config.Config()
    arguments = {
        'dbpath': config.getpath(),
        'password': config.get_password()
    }

    manager = KeepassManager.KeepassManager(**arguments)
    services = config.get_active()
    active_services = []
    if services['FaceBook']['active']:
        manager.init_fb()
        active_services.append('FaceBook')
    if services['GitHub']['active']:
        manager.init_gh()
        active_services.append('GitHub')
    if services['Reddit']['active']:
        manager.init_reddit()
        active_services.append('Reddit')
    if services['SSH']['active']:
        manager.init_ssh()
        active_services.append('SSH')

    service_names = {
        'FaceBook': 'change_fb_password',
        'GitHub': 'change_gh_password',
        'Reddit': 'change_reddit_password',
        'SSH': 'change_password_over_ssh'
    }
    while True:
        for service in active_services:
            if config.check_for_update(service):
                print(f'changing {service}')
                if manager.__getattribute__(service_names[service])():
                    config.update_time(service)
        print('giong to sleep')
        time.sleep(500)


def start():
    pid = '/tmp/atc.pid'
    app = daemonize.Daemonize(app='atc', pid=pid, action=main)
    app.start()


def stop():
    pid_file = '/tmp/atc.pid'
    pid = open(pid_file).read()
    os.kill(int(pid), signal.SIGTERM)
    os.remove(pid_file)


def run():
    main()


options = ['start', 'stop', 'run']
if len(sys.argv) > 1 and sys.argv[1].lower() in options:
    globals()[sys.argv[1].lower()]()
else:
    print('Options are start stop or run')
