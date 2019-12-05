from datetime import datetime
import short_url
from app import db

class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortLink = db.Column(db.String(64), index=True)
    longLink = db.Column(db.UnicodeText())
    genTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Short {}>, <Long {}>, <Gen Time {}>'.format(self.shortLink, self.longLink, self.genTime)

    def generateShortLink(self, id):
        self.shortLink = short_url.encode_url(id)