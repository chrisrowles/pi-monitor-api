import psutil

from app.main.service.wifi_service import *


def get_network_status():
    return {
        'status': 'connected'
    }


def get_network_info():
    return {
        'interfaces': get_interface_stats(),
        'connections': get_connections()
    }


def get_wifi_info():
    return parse_wifi_info()


def get_wifi_speed():
    return run_wifi_speedtest()


def get_interfaces():
    interfaces = psutil.net_if_addrs()

    return [*interfaces.keys()]


def get_interface_stats():
    interfaces = dict()
    for addr, stat in psutil.net_io_counters(pernic=True).items():
        interfaces[addr] = {
            'mb_sent': stat.bytes_sent / (1024.0 * 1024.0),
            'mb_received': stat.bytes_recv / (1024.0 * 1024.0),
            'pk_sent': stat.packets_sent,
            'pk_received': stat.packets_recv,
            'error_in': stat.errin,
            'error_out': stat.errout,
            'dropout': stat.dropout,
        }

    return interfaces


def get_connections():
    connections = dict()
    connections['ssh'] = []
    for sconn in psutil.net_connections(kind='inet'):
        if sconn.laddr.port == 22 and sconn.status == 'ESTABLISHED':
            connections['ssh'].append({
                'local_port': sconn.laddr.port,
                'remote_ip': sconn.raddr.ip,
            })

    return connections
