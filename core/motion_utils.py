import platform
import time

ON_RPI = platform.system().lower() == "linux"

try:
    if ON_RPI:
        from pidog import Pidog
        _dog = Pidog()
    else:
        _dog = None
except Exception:
    _dog = None
    ON_RPI = False

def _log(action: str):
    print(f"[MOTION] {action}")

def wag_tail(times: int = 2):
    if _dog:
        _dog.tail_move([30, -30], 400, times)
        time.sleep(0.8)
    else:
        _log("Scodinzola")

def sit():
    if _dog:
        _dog.do_action("sit", 1)
    else:
        _log("Siediti")

def lie_down():
    if _dog:
        _dog.do_action("lie", 1)
    else:
        _log("A terra")

def come_here(steps: int = 2):
    if _dog:
        _dog.walk(steps, [0, 0, 0], speed=45)
    else:
        _log("Vieni qui (mock)")

def turn_left():
    if _dog:
        _dog.turn_left(30)
    else:
        _log("Gira a sinistra")

def turn_right():
    if _dog:
        _dog.turn_right(30)
    else:
        _log("Gira a destra")

def stop():
    if _dog:
        _dog.stop()
    else:
        _log("Stop")
