"""Gunicorn configuration file."""
from prometheus_client import multiprocess


def child_exit(server, worker):
    """Remove leftover pid files from `prometheus_multiprocess_dir`.

    On green unicorn worker exit. These files are used to share metrics between
    processes. If they aren't cleaned on exit, they will cause issues on restart
    if pids are reused.

    Args:
        server: gunicorn server object
        worker: gunicorn worker object
    """
    multiprocess.mark_process_dead(worker.pid)


errorlog = "-"  # https://docs.gunicorn.org/en/latest/settings.html#errorlog
bind = "0.0.0.0:9000"  # https://docs.gunicorn.org/en/latest/settings.html#bind
# https://docs.gunicorn.org/en/latest/settings.html#worker-class
worker_class = "uvicorn.workers.UvicornWorker"
worker_tmp_dir = (
    "/dev/shm"  # nosec https://docs.gunicorn.org/en/latest/settings.html#worker-tmp-dir
)
workers = "2"  # https://docs.gunicorn.org/en/latest/settings.html#workers
