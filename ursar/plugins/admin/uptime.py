from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

from datetime import datetime, timedelta

class UptimePlugin(UrsarPlugin):

    def __init__(self):
        self.boot_time = datetime.now()

    @respond_to('^uptime$')
    def uptime(self, message):
        diff = datetime.now() - self.boot_time
        days, hours, minutes, seconds = diff.days, diff.seconds // 3600, diff.seconds // 60 % 60, diff.seconds % 60

        return 'I\'ve been running for %s days, %s hours, %s minutes, %s seconds' % (days, hours, minutes, seconds)