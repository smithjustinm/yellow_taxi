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
