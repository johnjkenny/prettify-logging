#!/usr/bin/env python3


"""Prettify-Logging is a wrapper tool that colors the stream formatting of the logging module.
"""


__author__ = 'John J Kenny'
__version__ = '1.0.0'


from time import gmtime
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL

from ColorFi.color_fi import ColorFi


class TemplateFormatter(Formatter):
    def __init__(self):
        super().__init__()
        self.time_zone = str()
        self.format_display = dict()
        
    def _time_zone_converter(self):
        if self.time_zone.upper() == 'UTC':
            Formatter.converter = gmtime
            
    def _format_entry(self, entry):
        self._time_zone_converter()
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
    def __init__(self, file_format: str, time_zone: str):
        super().__init__()
        self.format_display = file_format
        self.time_zone = time_zone
    
    def format(self, entry):
        return self._format_entry(entry)
        

class StreamFormatter(TemplateFormatter):
    def __init__(self, stream_format: str, time_zone: str):
        super().__init__()
        self.format_display = stream_format
        self.time_zone = time_zone
    
    def format(self, entry):
        return self._format_entry(entry)


class PrettifyLogging(ColorFi):
    def __init__(self, **kwargs: dict):
        super().__init__()
        self.log = None
        default = '[%(asctime)s] - %(name)s - %(levelname)s - (%(module)s, %(funcName)s, %(lineno)d): %(message)s'
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.level = kwargs['level'] if 'level' in kwargs else 'error'
        self.time_zone = kwargs['time_zone'] if 'time_zone' in kwargs else 'UTC'
        self.stream_format = kwargs['stream_format'] if 'stream_format' in kwargs else default
        self.file_format = kwargs['file_format'] if 'file_format' in kwargs else default
        self.debug_display = kwargs['debug_display'] if 'debug_display' in kwargs else 'bright-black'
        self.info_display = kwargs['info_display'] if 'info_display' in kwargs else 'blue'
        self.warning_display = kwargs['warning_display'] if 'warning_display' in kwargs else 'yellow'
        self.error_display = kwargs['error_display'] if 'error_display' in kwargs else 'bright-red'
        self.critical_display = kwargs['critical_display'] if 'critical_display' in kwargs else ('red', 'invert')

    def configure(self):
        if self.name is not None:
            self.log = getLogger(self.name)
            self.log.setLevel(self._log_level_mapping(self.level.lower()))
            for config_type in ('stream', 'file'):
                self._set_config(config_type)
            return self.log
        else:
            self.print_message('No name specified for logger.', 'red')
    
    def _set_config(self, config_type: str):
        format_dict = self._create_format_dict(config_type)
        if format_dict:
            if config_type == 'stream':
                handler = StreamHandler()
                formatter = StreamFormatter(format_dict, self.time_zone)
            elif config_type == 'file':
                handler = FileHandler(self.name, mode='a+')
                formatter = FileFormatter(format_dict, self.time_zone)
            handler.setFormatter(formatter)
            self.log.addHandler(handler)
        
    def _create_format_dict(self, config_type: str):
        if config_type == 'stream':
            return {'debug': self._unpack_stream_config(self.debug_display, 'debug'),
                    'info': self._unpack_stream_config(self.info_display, 'info'),
                    'warning': self._unpack_stream_config(self.warning_display, 'warning'),
                    'error': self._unpack_stream_config(self.error_display, 'error'),
                    'critical': self._unpack_stream_config(self.critical_display, 'critical')}
        elif config_type == 'file':
            return {'debug': self.file_format, 'info': self.file_format, 'warning': self.file_format,
                    'error': self.file_format, 'critical': self.file_format}
            
    def _unpack_stream_config(self, display_config, level: str):
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
        else:
            self.print_message('Invalid stream display config for {} level: {}.\nAvailable Options:'.format(
                level,display_config), 'red')
            self.display_key_options()

    def _log_level_mapping(self, level: str):
        log_levels = {'debug': DEBUG, 'info': INFO, 'warning': WARNING, 'error': ERROR, 'critical': CRITICAL}
        try:
            return log_levels[level]
        except KeyError:
            self.print_message('Unknown log level "{}". Options: {}'.format(level, ", ".join(
                list(log_levels.keys()))), 'red')
            
    def display_test(self):
        self.log.debug('Debug message test')
        self.log.info('Info message test')
        self.log.warning('Warning message test')
        self.log.error('Error message test')
        self.log.critical('Critical message test')


if __name__ == '__main__':
    pretty_logging = PrettifyLogging(name='test.log', level='debug')
    pretty_logging.debug_display = 'green'
    pretty_logging.info_display = ('magenta', 'bold', 'foreground')
    log = pretty_logging.configure()
    pretty_logging.display_test()
