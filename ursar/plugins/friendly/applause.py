from ursar.plugin import UrsarPlugin
from ursar.decorators import hear

import random 

class ApplausePlugin(UrsarPlugin):

    @hear("^(?P<sentiment>.*)(applause|applauze|aplauze|clap|bravo|felicitari)$")
    def applause(self, message, sentiment=None):
        gif_url = None

        if sentiment.strip() in ['insincere', 'nesincere', 'slow']:
            gif_url = random.choice([
                    'http://i.imgur.com/2QXgcqP.gif',
                    'http://i.imgur.com/Yih2Lcg.gif',
                    'http://i.imgur.com/un3MuET.gif',
                    'http://i.imgur.com/H2wPc1d.gif',
                    'http://i.imgur.com/uOtALBE.gif',
                    'http://i.imgur.com/nmqrdiF.gif',
                    'http://i.imgur.com/GgxOUGt.gif',
                    'http://i.imgur.com/wyTQMD6.gif',
                    'http://i.imgur.com/GYRGOy6.gif',
                    'http://i.imgur.com/ojIsLUA.gif',
                    'http://i.imgur.com/bRetADl.gif',
                    'http://i.imgur.com/814mkEC.gif',
                    'http://i.imgur.com/uYryMyr.gif',
                    'http://i.imgur.com/YfrikPR.gif',
                    'http://i.imgur.com/sBEFqYR.gif',
                    'http://i.imgur.com/Sx8iAS8.gif',
                    'http://i.imgur.com/5zKXz.gif'
                ])
        else:
            gif_url = random.choice([
                'http://i.imgur.com/pfrtv6H.gif',
                'http://i.imgur.com/Bp4P8l3.gif',
                'http://i.imgur.com/v7mZ22P.gif',
                'http://i.imgur.com/S1v4KuY.gif',
                'http://i.imgur.com/YTaSAkq.gif',
                'http://i.imgur.com/JO6Wz3r.gif',
                'http://i.imgur.com/pWEd6cF.gif',
                'http://i.imgur.com/zumSlIA.gif',
                'http://i.imgur.com/RGczKmV.gif',
                'http://i.imgur.com/KAQhoCm.gif',
                'http://i.imgur.com/PASRKXo.gif',
                'http://i.imgur.com/ZOWQTO6.gif',
                'http://i.imgur.com/cY0eH5c.gif',
                'http://i.imgur.com/wf5qvOM.gif',
                'http://i.imgur.com/9Zv4V.gif',
                'http://i.imgur.com/t8zvc.gif'
            ])

        return '<a href="{url}">{url}</a>'.format(url=gif_url)