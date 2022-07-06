import PWM_Stepper_Motor_01 as stp
import RPi.GPIO as GPIO
import datetime
# -----import pr6100Rs485 as PR
import logging
import argparse
import signal
import os
import sys
import multiprocessing
import time

# from filehelper import FileHelper

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# class Handler:
#     def onDestroy(self, *args):
#         Gtk.main_quit()

#     def onButtonPressed(self, button):
#         print("Hello World!")




def add_command_option():
    parser = argparse.ArgumentParser(description='Application')
    parser.add_argument('--loglevel', '-l',
                        type=str,
                        default='NOTSET',
                        help='Log levels: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL, DISABLE')
    parser.add_argument('--logdir', '-d',
                        type=str,
                        default='./logs/',
                        help='Log directory relative path example (1 level up): "../logs/"')
    parser.add_argument('--logname', '-n',
                        type=str,
                        default='Provoda.log',
                        help='Log file name')
    parser.add_argument('--configpath', '-c',
                        type=str,
                        default='config.json',
                        help='Config file path')
    return parser.parse_args()


def init_logger(file_dir='./logs/',
                file_name='main.log',
                log_level='DEBUG',
                log_name='main',
                log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    try:
        logger = logging.getLogger(log_name)
        logger.disabled = True
        if log_level in logging._nameToLevel:
            logging.basicConfig(format=log_format, level=log_level)
            logger.setLevel(log_level)
            logger.disabled = False
            os.makedirs(file_dir, exist_ok=True)
            fh = logging.FileHandler(file_dir + "/" + file_name)
            fh.setLevel(log_level)
            fh.setFormatter(logging.Formatter(log_format))
            logger.addHandler(fh)
        return logger
    except Exception as error:
        raise Exception("Unable to initialize logger: %s" % error)

# Const
SHAG_STEP = 1
SHAG_SPEED = 1

STEP_MAX = 50
STEP_MIN = 10
SPEED_MAX = 8
SPEED_MIN = SHAG_SPEED
COEFF = 1
# TestMode1 = True ## True - Not sending in rs485, False - all system active

# Strings Const
STEP_S = "Шаг свивки\n(мм) "
RPM_SET_S = "Скорость приёмного барабана\n(об/мин)"
RPM_UP_S = "Скорость\nприёмного барабана\n(об/мин)"
RPM_DOWN_S = "Скорость\nпланшайбы\n(об/мин)"
TIME_S = "Время\nc момента\n начала свивки"
CONNECT_ON_S = "Соединение: ON"
CONNECT_OFF_S = "Соединение: OFF"
DOOR_OPEN_S = "Кожух: Открыт"
DOOR_CLOSED_S = "Кожух: Закрыт"

FONT_STYLE_1 = "<span font_desc='Tahoma 16'>%s</span>"
FONT_STYLE_2 = "<span font_desc='Tahoma 45'>%s</span>"
FONT_STYLE_3 = "<span font_desc='Tahoma 20'>%s</span>"
FONT_STYLE_4 = "<span font_desc='Tahoma 20' foreground='red'>%s</span>"


class Parametrs():
    def __init__(self, step=STEP_MIN, speed=SPEED_MIN, time=0, ActiveMotors=False, FWD=True, time_=0, connect=False):
        self.step = step
        self.speed = speed  # RPM VALUE
        self.time = time
        self.ActiveMotors = ActiveMotors
        self.FWD = FWD
        self.time_ = time_
        self.connect = connect
        self.buttonStartDeb = 0
        self.buttonStopDeb = 0
        self.HollDeb = 0
        self.NumberStep = 0
        self.REP = 0
        self.LEP = 0
        self.CurrP = 0
        self.Stop = False




def worker(num,arr):
    while True:
        if Param.CurrP == Param.LEP:
            s_motor.goto_r(Param.NumberStep , num)
            Param.CurrP = Param.REP
        else:
            s_motor.goto_l(Param.NumberStep, num)
            Param.CurrP = Param.LEP


class Handler:
    global log
    def __init__(self) -> None:
        self.process = multiprocessing.Process(target=worker, name="Pr1")
        self.num = multiprocessing.Value('i', 0)

        pass

    def EventToLeft(self, *args):
        s_motor.forward()
        print("To Left")

    def EventToRight(self, *args):
        s_motor.reverse()
        Param.NumberStep = Param.NumberStep + 4000
        print("To Right")

    def EventLeftEndPoint(self, *args):
        Param.NumberStep = 0
        Param.LEP = 0
        Param.CurrP= Param.LEP
        LabelLP.set_markup("0")
        pass

    def EventRightEndPoint(self, *args):
        Param.REP = Param.NumberStep
        Param.CurrP = Param.NumberStep
        LabelRP.set_markup(str(Param.REP))
        pass

    def onDestroy(self, *args):
        Gtk.main_quit()

    def EventMStep(self, *args):
        pass

    def EventPSpeed(self, *args):
        pass

    def EventMSpeed(self, *args):
        pass

    def EventStart(self, *args):
        #--- PR.Start_(100, 1, 0)
        self.num.value = Param.CurrP
        arr = multiprocessing.Array('i', range(10))
        self.process.close()
        self.process = multiprocessing.Process(target=worker, name="Pr1", args=(self.num,arr))
        self.process.start()
        log.info("Process started %i",self.process.pid)
        log.info('Process WorkItem %s',self.process.name)
        log.info('CPU num {}'.format(multiprocessing.cpu_count()))

    def EventStop(self, *args):
        #--- PR.Stop_(1)
        Param.Stop = True
        if self.process.is_alive():
            self.process.terminate()
        Param.CurrP = self.num.value
        LabelCurPosition.set_markup(str(Param.CurrP))
        log.info("currp= {}".format(self.num.value))
        log.info("Kill process")
        pass

    def EventPStep(self, *args):
        pass





# GLib.timeout_add(100,buttonIterupt)



def receive_signal(signum, stack):
    quit_app('Received system signal: %s' % signal.Signals(signum).name)


def quit_app(error=None):
    global log
    if 'log' not in globals():
        log = logging.getLogger("main")
        log.warning("Logger not found. Enabling standard logger")
    if error:
        log.critical(error)
    try:
        os.remove(lock_file)
    except Exception as exc:
        log.error("Unable to remove lock file: %s" % exc)
    log.info('Application stopped')
    sys.exit()



if __name__ == "__main__":

    Param = Parametrs()  # Global parametrs of all system
    builder = Gtk.Builder()
    builder.add_from_file("gui4.glade")
    builder.connect_signals(Handler())

    LabelStep = builder.get_object("LabelStep")
    LabelSpeed = builder.get_object("LabelSpeed")
    LabelTime = builder.get_object("LabelTime")
    LabelRPM_UP = builder.get_object("LabelRPM_UP")
    LabelRPM_Down = builder.get_object("LabelRPM_Down")
    Switch1 = builder.get_object("Switch1")
    LabelConnect = builder.get_object("LabelConnect")
    ButtonStart = builder.get_object("ButtonStart")
    ButtonStop = builder.get_object("ButtonStop")
    LabelTimeBIG = builder.get_object("LabelTimeBIG")
    LabelRPM_UP_BIG = builder.get_object("LabelRPM_UP_BIG")
    LabelRPM_DOWN_BIG = builder.get_object("LabelRPM_DOWN_BIG")
    LabelStep_ = builder.get_object("LabelStep_")
    LabelSpeed_ = builder.get_object("LabelSpeed_")
    LabelDoor = builder.get_object("LabelDoor")

    ButtonToLeft = builder.get_object("toLeft")
    ButtonToRight = builder.get_object("toRight")
    ButtonLKT = builder.get_object("leftEndPoint")
    ButtonRKT = builder.get_object("rightEndPoint")

    LabelLP = builder.get_object("LabelLP")
    LabelRP = builder.get_object("LabelRP")
    LabelCurPosition = builder.get_object("LabelCurPosition")

    s_motor = stp.STMotor()
    num = multiprocessing.Value('d', 0.0)
    lock_file = "/tmp/app_lock.lock"
    # Change working directory to project directory
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(os.path.abspath(sys.executable + "/")))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Get start arguments
    args = add_command_option()

    # Init logger
    try:
        log = init_logger(file_dir=args.logdir,
                          file_name=args.logname,
                          log_level=args.loglevel)
    except Exception as e:
        quit_app(e)
    else:
        log.info('Application started')

        # This is to check if there is already a lock file existing
        try:
            if os.access(lock_file, os.F_OK):
                # If the lockfile is already there then check the PID number in the lock file
                pid_file = open(lock_file, "r")
                pid_file.seek(0)
                old_pid = pid_file.readline()
                # Now we check the PID from lock file matches to the current process PID
                if os.path.exists("/proc/%s" % old_pid):
                    quit_app("Application already running. PID: %s" % old_pid)
                else:
                    log.debug(
                        "Lock file exists but application is not running. Removing lock file")
                    os.remove(lock_file)

            # This is part of code where we put a PID file in the lock file
            pid_file = open(lock_file, "w")
            pid_file.write("%s" % os.getpid())
            pid_file.close()
            log.debug("Lock file with current pid (%s) created: %s" %
                      (os.getpid(), lock_file))
        except Exception as e:
            quit_app("Unable get access to lock file: %s" % e)

        # Subscribing to system exit signals
        signal.signal(signal.SIGQUIT, receive_signal)
        signal.signal(signal.SIGINT, receive_signal)
        signal.signal(signal.SIGTERM, receive_signal)

        # Reading config file
        config_path = args.configpath
        config = {}
        try:
            # config = FileHelper.read_json_file(config_path)
            log.debug("Config file successfully read")
        except Exception as e:
            quit_app("Unable to read config file: %s" % e)
    

    window = builder.get_object("win1")
    window.fullscreen()
    window.show_all() 
    Gtk.main()
