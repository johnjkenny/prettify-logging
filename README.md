# Prettify-Logging
Prettify-Logging is a wrapper tool that colors the stream formatting of the logging module.

## Installation

Prettify-Logging is a python package which can be found on [Python Package Index (PyPi)](https://pypi.org/project/Prettify-Logging/). Run the following command to install:<br>
``` bash
pip install prettify-logging
```

## Import Prettify-Logging Into Your Projects
``` python
from PrettifyLogging.prettify_logging import PrettifyLogging
```

## Usage
Making changes from the default configuration of PrettifyLogging must be completed before calling PrettifyLogging().configure(). PrettifyLogging config options:

    key: name = (str) [Required]. Name of the log file to be created. Example: 'my_log_file.log'
    
    key: level = (str) Log level to log records. Default is 'error'. Example: 'debug'
    
    key: set_utc = (bool) Set time entry in log to UTC. Default is True.
    
    key: default_format = (str) Default log record formatting. Default is:
          [%(asctime)s] - %(name)s - %(levelname)s - (%(module)s, %(funcName)s, %(lineno)d): %(message)s
          
    key: stream_format = (str) Log record formatting. Default is default_format. Example:
          %(asctime)s - %(name)s - %(levelname)s - %(message)s
          
    key: file_format = (str) Log record formatting. Default is default_format. Example:
          %(asctime)s - %(name)s - %(levelname)s - %(message)s

    key: debug_display  = (str, tuple): Debug stream formatting. Default is "bright-black".
    
    key: info_display  = (str, tuple): Info stream formatting. Default is "blue".

    key: warning_display = (str, tuple): Warning stream formatting. Default is "yellow".

    key: error_display  = (str, tuple): Error stream formatting. Default is "bright-red".

    key: critical_display  = (str, tuple): Critical stream formatting. Default is ('red', 'invert').

Setting the configuration options on PrettifyLogging() can be made by passing the config as key=value to the class, using a dictionary to define the key values, or by using dot notation to define particular values.

The name (file name for the log file) must be set before calling PrettifyLogging().configure(). Example:
``` python
log = PrettifyLogging(name="my_log_file.log").configure()
# or
logger = PrettifyLogging()
logger.name = "my_log_file.log"
logger.configure()
```
When making display changes (debug_display, info_display, warning_display, error_display, or critical_display keys) the value can be either a string or tuple. If the value is a string, then the value string must define a color type. If the value is a tuple, the tuple must include a string that defines a color type. To view the coloring options, please see [Color-Fi](https://github.com/johnjkenny/color-Fi#readme) or you can print to console by running the following:
```python
logging = PrettifyLogging()
logging.display_key_options()
```
Coloring examples can be found in the below examples.

### Using Key=Value to Define Config Settings and View Default Stream Output:
``` python
logging = PrettifyLogging(name="test.log", level="debug")
logging.configure()
logging.display_test()
```
Output as png:<br>
![message Sample](/assets/default_stream_output.png)

### Using Dictionary To Define Config Settings:
``` python
default = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s: %(message)s'
config = {
    'name': 'test.log',
    'level': 'debug',
    'set_utc': False,
    'default_format': default,
    'stream_format': default,
    'file_format': default,
    'debug_display': 'blue',
    'info_display': ('cyan', 'bold'),
    'warning_display': ('invert', 'bright-magenta'),
    'error_display': 'yellow',
    'critical_display': ('underline', 'bright-green', 'background')
}
logging = PrettifyLogging(**config)
logging.configure()
logging.display_test()
```
Output as png:<br>
![message Sample](/assets/dict_output.png)

### Using Dot Notation to Define Settings:
``` python
logging = PrettifyLogging()
logging.name = "test.log"
logging.level = "debug"
logging.debug_display = ('magenta', 'bold')
logging.info_display = 'cyan'
logging.warning_display = ('italic', 'bright-green', 'foreground')
logging.error_display = ('blue', 'invert')
logging.critical_display = ('yellow', 'bold', 'background')
logging.stream_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.configure()
logging.display_test()
```
Output as png:<br>
![message Sample](/assets/dot_notation_output.png)

### Making Log Entries:
``` python
log = PrettifyLogging(name="test.log", level="info").configure()
log.info('I am logging this...')
# or
logger = PrettifyLogging(name="test.log", level="debug")
log = logger.configure()
log.debug('I am also logging this...')
# or
logger = PrettifyLogging(name="test.log")
logger.configure()
logger.log.error('This also is getting logged...')
```

### Print to Console in Color Without Logging:
``` python
logger = PrettifyLogging()
logger.print_message('Message 1', 'green')
logger.print_message('Message 2', 'red', _format='bold')
logger.print_message('Message 3', 'yellow', 'background', 'underline')
```
Output as png:<br>
![message Sample](/assets/print_example.png)
