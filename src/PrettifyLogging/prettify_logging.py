#!/usr/bin/env python3


"""Prettify-Logging is a wrapper tool that colors the stream formatting of the logging module.
"""


__author__ = 'John J Kenny'
__version__ = '1.0.2'


from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, FileHandler, Formatter, LogRecord, StreamHandler, getLogger
from time import gmtime

from ColorFi.color_fi import ColorFi


class TemplateFormatter(Formatter):
    """Template formatter for the logging module. Inherits from the Formatter class in the logging module."""
    def __init__(self):
        """Initializes the formatter."""
        super().__init__()
        self.set_utc = True
        self.format_display = dict()

    def _format_entry(self, entry: LogRecord):
        """A helper function that formats the log entry.

        Args:
            entry (LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record.
        """
        if self.set_utc:
            Formatter.converter = gmtime
        format_original = self._style._fmt
        if entry.levelno == DEBUG:
            self._style._fmt = self.format_display['debug']
        elif entry.levelno == INFO:
            self._style._fmt = self.format_display['info']
        elif entry.levelno == WARNING:
            self._style._fmt = self.format_display['warning']
        elif entry.levelno == ERROR:
            self._style._fmt = self.format_display['error']
        elif entry.levelno == CRITICAL:
            self._style._fmt = self.format_display['critical']
        formated_entry = Formatter.format(self, entry)
        self._style._fmt = format_original
        return formated_entry


class FileFormatter(TemplateFormatter):
    """Log File Formatter. Inherits from TemplateFormatter."""
    def __init__(self, file_format: dict, set_utc: bool = True):
        """Initializes file formatter.

        Args:
            file_format (dict): dictionary of format strings of log levels for the log file.
            set_utc (bool): Set time entry in log to UTC. Default is True.
        """
        super().__init__()
        self.format_display = file_format
        self.set_utc = set_utc

    def format(self, record: LogRecord):
        """Formats the log record.

        Args:
            record (LogRecord): The log record to be formatted.
        Returns:
            str: The formatted log record.
        """
        return self._format_entry(record)


class StreamFormatter(TemplateFormatter):
    """Log Stream Formatter. Inherits from TemplateFormatter."""
    def __init__(self, stream_format: dict, set_utc: bool = True):
        """Initializes stream formatter.

        Args:
            stream_format (dict): dictionary of format strings of log levels for the log stream.
            set_utc (bool): Set time entry in log to UTC. Default is True.
        """
        super().__init__()
        self.format_display = stream_format
        self.set_utc = set_utc

    def format(self, record: LogRecord):
        """Formats the log record.

        Args:
            record (LogRecord): The log record to be formatted.
        Returns:
            str: The formatted log record.
        """
        return self._format_entry(record)


class PrettifyLogging(ColorFi):
    """Sets user log settings for the stream and file handlers. Inherits from ColorFi to help color log streams."""
    def __init__(self, **kwargs: dict):
        """Initializes the PrettifyLogging class.

        kwargs options:

        key: name = (str) [Required]. Name of the log file to be created. Example: 'my_log_file.log'

        key: level = (str) Log level to log records. Default is 'error'. Example: 'debug'

        key: set_utc = (bool) Set time entry in log to UTC. Default is True.

        key: default_format = (str) Default log record formatting. Default is:\n
            [%(asctime)s] - %(name)s - %(levelname)s - (%(module)s, %(funcName)s, %(lineno)d): %(message)s

        key: stream_format = (str) Log record formatting. Default is default_format. Example:\n
            %(asctime)s - %(name)s - %(levelname)s - %(message)s

        key: file_format = (str) Log record formatting. Default is default_format. Example:\n
            %(asctime)s - %(name)s - %(levelname)s - %(message)s

        key: debug_display  = (str, tuple): Debug stream formatting. Default is "bright-black".

        key: info_display  = (str, tuple): Info stream formatting. Default is "blue".

        key: warning_display = (str, tuple): Warning stream formatting. Default is "yellow".

        key: error_display  = (str, tuple): Error stream formatting. Default is "bright-red".

        key: critical_display  = (str, tuple): Critical stream formatting. Default is ('red', 'invert').
        """
        super().__init__()
        self.log = None
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.level = kwargs['level'] if 'level' in kwargs else 'error'
        self.set_utc = kwargs['set_utc'] if 'set_utc' in kwargs else True
        self.default_format = kwargs['default_format'] if 'default_format' in kwargs else (
            '[%(asctime)s] - %(name)s - %(levelname)s - (%(module)s, %(funcName)s, %(lineno)d): %(message)s')
        self.stream_format = kwargs['stream_format'] if 'stream_format' in kwargs else self.default_format
        self.file_format = kwargs['file_format'] if 'file_format' in kwargs else self.default_format
        self.debug_display = kwargs['debug_display'] if 'debug_display' in kwargs else 'bright-black'
        self.info_display = kwargs['info_display'] if 'info_display' in kwargs else 'blue'
        self.warning_display = kwargs['warning_display'] if 'warning_display' in kwargs else 'yellow'
        self.error_display = kwargs['error_display'] if 'error_display' in kwargs else 'bright-red'
        self.critical_display = kwargs['critical_display'] if 'critical_display' in kwargs else ('red', 'invert')

    def configure(self):
        """configure creates the logger and sets the log settings for the stream and file handlers.

        Returns:
            (Logger): the logger object.
        """
        if self.name is not None:
            self.log = getLogger(self.name)
            self.log.setLevel(self._log_level_mapping(self.level.lower()))
            for config_type in ('stream', 'file'):
                self._set_config(config_type)
            return self.log
        self.print_message('No name specified for logger.', 'red')
        return None

    def _set_config(self, config_type: str):
        """_set_config sets the log settings for the stream and file handlers.

        Args:
            config_type (str): 'stream' or 'file'.
        """
        format_dict = self._create_format_dict(config_type)
        if format_dict:
            if config_type == 'stream':
                handler = StreamHandler()
                formatter = StreamFormatter(format_dict, self.set_utc)
            elif config_type == 'file':
                handler = FileHandler(self.name, mode='a+')
                formatter = FileFormatter(format_dict, self.set_utc)
            handler.setFormatter(formatter)
            self.log.addHandler(handler)

    def _create_format_dict(self, config_type: str):
        """_create_format_dict creates the format dictionary for the stream and file handlers.

        Args:
            config_type (str): 'stream' or 'file'.

        Returns:
            dict: dictionary of format strings for the stream and file handlers.
        """
        if config_type == 'stream':
            return {'debug': self._unpack_stream_config(self.debug_display, 'debug'),
                    'info': self._unpack_stream_config(self.info_display, 'info'),
                    'warning': self._unpack_stream_config(self.warning_display, 'warning'),
                    'error': self._unpack_stream_config(self.error_display, 'error'),
                    'critical': self._unpack_stream_config(self.critical_display, 'critical')}
        return {'debug': self.file_format, 'info': self.file_format, 'warning': self.file_format,
                'error': self.file_format, 'critical': self.file_format}

    def _unpack_stream_config(self, display_config, level: str):
        """_unpack_stream_config unpacks the stream config and creates the formatting.

        Args:
            display_config (str or tuple): The stream config.
            level (str): The log level.

        Returns:
            str or None: The formatted stream config or None if the config is not valid.
        """
        color = None
        ground = 'foreground'
        formatting = 'default'
        if isinstance(display_config, str):
            if display_config in self.colors['foreground'] or display_config in self.colors['background']:
                color = display_config
        elif isinstance(display_config, tuple):
            for item in display_config:
                if item in self.colors['foreground'] or item in self.colors['background']:
                    color = item
                elif item in self.colors:
                    ground = item
                elif item in self.formatting:
                    formatting = item
        if color:
            return self.format_message(self.stream_format, color, ground, formatting)
        self.print_message('Invalid stream display config for {} level: {}.\nAvailable Options:'.format(
            level, display_config), 'red')
        self.display_key_options()
        return None

    def _log_level_mapping(self, level: str):
        """_log_level_mapping maps the log level to the logging module level.

        Args:
            level (str): The log level.

        Returns:
            int or None: The logging module level or None if the level is not valid.
        """
        log_levels = {'debug': DEBUG, 'info': INFO, 'warning': WARNING, 'error': ERROR, 'critical': CRITICAL}
        try:
            return log_levels[level]
        except KeyError:
            self.print_message('Unknown log level "{}". Options: {}'.format(level, ", ".join(
                list(log_levels.keys()))), 'red')

    def display_test(self):
        """display_test creates a test entry for all log levels to verify the settings are to the users liking.
        Be sure to set the log level to 'debug' when initializing PrettifyLogging to see all log level entries.
        """
        self.log.debug('Debug message test')
        self.log.info('Info message test')
        self.log.warning('Warning message test')
        self.log.error('Error message test')
        self.log.critical('Critical message test')
