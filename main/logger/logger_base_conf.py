import logging
import sys
import colorlog 

def setup_logger(level=logging.INFO):
    fmt = "%(asctime)s - %(name)s - %(log_color)s%(levelname)-8s%(reset)s: %(message)s"
    formatter = colorlog.ColoredFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S",
                                         log_colors={
                                             'DEBUG':    'cyan',
                                             'INFO':     'green',
                                             'WARNING':  'yellow',
                                             'ERROR':    'bold_red',
                                             'CRITICAL': 'bold_red,bg_white',
                                         })

    handler = colorlog.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    root = logging.getLogger()         
    root.setLevel(level)
    for h in list(root.handlers):
        root.removeHandler(h)
    root.addHandler(handler)
    return logging.getLogger(__name__) 