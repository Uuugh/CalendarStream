"""Start-up check for the test servers (0.2.8-beta.34, review #8 finding 2).

A suite starts its server in a thread and used to sleep a second, so a port already held by a leftover
process went unnoticed and the suite talked to the wrong server. wait_up() waits until THIS server is
serving, and stops the suite with a FAIL line (which run.sh counts) when it isn't.
"""
import sys, time


def wait_up(srv, port, seconds=20):
    end = time.time() + seconds
    while time.time() < end:
        if srv.started:
            return
        time.sleep(0.05)
    print(f"FAIL test server did not start on port {port} (in use by a leftover process? see `ss -ltnp | grep {port}`)")
    sys.exit(1)
