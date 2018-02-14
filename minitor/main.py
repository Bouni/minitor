from subprocess import CalledProcessError
from subprocess import check_call

import yamlenv

# TODO: validate on start

def get_config(path):
    """Loads config from a YAML file with env interpolation"""
    with open(path, 'r') as yaml:
        contents = yaml.read()
        return yamlenv.load(contents)


def check_monitor(monitor):
    cmd = monitor.get('command', [])
    if cmd:
        check_call(cmd, shell=isinstance(cmd, str))


def alert_for_monitor(monitor, alerts):
    for alert_name in monitor.get('alerts', []):
        cmd = alerts.get(alert_name, {}).get('command', [])
        if cmd:
           check_call(cmd, shell=isinstance(cmd, str))


def main():
    # TODO: get config file off command line
    config = get_config('./sample-config.yml')
    alerts = config.get('alerts', {})
    for monitor in config.get('monitors', []):
        try:
            check_monitor(monitor)
        except CalledProcessError:
            alert_for_monitor(monitor, alerts)

if __name__ == '__main__':
    main()
