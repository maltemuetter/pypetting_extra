from pypetting import GridSite,  start_timer, wait_timer


def direct_command(command: str):
    return bytes("B;" + command, "utf-8")


def wait_for_loop_timer(self, timer_id=1):
    T = self.exp.T_all
    i = self.i
    if i+1 < len(T):
        dt = T[i+1] - T[i]
    else:
        dt = 1
    print(dt)
    return wait_timer(timer_id, dt*3600)
