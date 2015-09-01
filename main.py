#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24

"""

__author__ = 'wesc+api@google.com (Wesley Chun)'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from conference import ConferenceApi
from google.appengine.ext import ndb
from google.appengine.api import memcache
from models import Session
        
class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


class getFeaturedSpeaker(webapp2.RequestHandler):
    """ Task Handler for /tasks/set_featured_speaker endpoint"""
    def post(self):
        featured_sessions = Session.query(Session.speaker == self.request.get('speaker'))
        if featured_sessions.count() != 1:
            mem_key = self.request.get('conferenceKey') + ':featured'
            print mem_key
            if memcache.get(mem_key) is None:
                # key: '{webKey}:featured', add to memcache
                sessions = [{'speaker': self.request.get('speaker'), 'sessions': [f.name for f in featured_sessions]}]
                memcache.add(mem_key, sessions, 36000)
            else:
                # key: '{webKey}:featured', set memcache
                state = list(memcache.get(mem_key))
                for s in state:
                    s['sessions'] = [f.name for f in featured_sessions]
                    state.append({'speaker': self.request.get('speaker'), 'sessions': [f.name for f in featured_sessions]})

                memcache.set(mem_key, state)


app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/set_featured_speaker', getFeaturedSpeaker),
], debug=True)
