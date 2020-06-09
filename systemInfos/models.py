from django.db import models
import socket
import platform
import psutil
import time
import collections
import subprocess
import datetime
# Create your models here.
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


class SystemInfo(models.Model):
    Processor = platform.processor()
    System = platform.system()
    machine_hardware = platform.machine()
    uname = platform.uname()
    boot_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(psutil.boot_time()))

    cpufreq = psutil.cpu_freq()
    def get_hostname(self):
        return socket.gethostname()
    def get_FQDN(self):
        return socket.getfqdn()

    #CPU
    def get_physical_core(self):
        return psutil.cpu_count(logical=False)
    def get_total_core(self):
        return psutil.cpu_count(logical=True)
    def get_cpu_freq(self):
        return self.cpufreq.current
    def get_cpu_usage_per_core(self):
        cpu_usage_per_core ={}
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            cpu_usage_per_core[i]=percentage
        return cpu_usage_per_core
    def get_cpu_usage(self):
        return psutil.cpu_percent()

    #Memory
    def get_total_memory(self):
        return get_size(psutil.virtual_memory().total)
    def get_available_memory(self):
        return get_size(psutil.virtual_memory().available)
    def get_used_memory(self):
        return get_size(psutil.virtual_memory().used)
    def get_percent_memory(self):
        return psutil.virtual_memory().percent

    #partitions and usage
    def get_partitions(self):
        partitions = []
        partition_info = collections.namedtuple('partitioninfo','device mountpoint fstype total used free percent')
        for part in psutil.disk_partitions():
            partition_tuple = partition_info(device=part.device,mountpoint=part.mountpoint,fstype=part.fstype,total=get_size(psutil.disk_usage(part.mountpoint).total),
                                             used=get_size(psutil.disk_usage(part.mountpoint).used),free=get_size(psutil.disk_usage(part.mountpoint).free),percent=psutil.disk_usage(part.mountpoint).percent)
            partitions.append(partition_tuple)
        return partitions

    def get_network(self):
        return psutil.net_if_addrs()

    def get_proc(self):
        processes = []
        for process in psutil.process_iter():
            # get all process info in one shot
            with process.oneshot():
                # get the process id
                pid = process.pid
                if pid == 0:
                    # System Idle Process for Windows NT, useless to see anyways
                    continue
                name = process.name()
                try:
                    create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(process.create_time()))
                except OSError:
                    # system processes, using boot time instead
                    create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(process.boot_time()))
                try:
                    # get the number of CPU cores that can execute this process
                    cores = len(process.cpu_affinity())
                except psutil.AccessDenied:
                    cores = 0
                # get the CPU usage percentage
                cpu_usage = process.cpu_percent()
                status = process.status()
                try:
                    # get the process priority (a lower value means a more prioritized process)
                    nice = int(process.nice())
                except psutil.AccessDenied:
                    nice = 0
                try:
                    # get the memory usage in bytes
                    memory_usage = get_size(process.memory_full_info().uss)
                except psutil.AccessDenied:
                    memory_usage = 0
                # io_counters = process.io_counters()
                # read_bytes = io_counters.read_bytes
                # write_bytes = io_counters.write_bytes
                n_threads = process.num_threads()
                try:
                    username = process.username()
                except psutil.AccessDenied:
                    username = "N/A"
                processes.append({
                    'pid': pid, 'name': name, 'create_time': create_time,
                    'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
                    'memory_usage': memory_usage, #'read_bytes': read_bytes, 'write_bytes': write_bytes,
                    'n_threads': n_threads, 'username': username,
                })
        return processes

    def get_logs(self):
        #use cat /var/log/messages toget the file
        result=subprocess.run(['cat','/var/log/messages'], stdout=subprocess.PIPE)
        #get a list of log messages
        lines=result.stdout.decode('utf-8').split('\n')
        #remove last new line character
        lines.pop()
        logs=[]

        for line in lines:
            log={}
            log['timestamp']=" ".join(line.split()[:3])
            log['hostname']=line.split()[3]
            log['process']=line.split()[4][:-1]
            log['message']=" ".join(line.split()[5:])
            logs.append(log)
        return logs





    # hostname = models.CharField(max_length=200)

