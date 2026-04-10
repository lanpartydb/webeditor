"""
lanpartydb_webeditor.forms
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2026 Jochen Kupperschmidt
:License: MIT
"""

from wtforms import (
    BooleanField,
    DateField,
    Form,
    IntegerField,
    StringField,
    TextAreaField,
)
from wtforms.validators import InputRequired, Optional, ReadOnly


class CreateSeriesForm(Form):
    slug = StringField('Slug', validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    alternative_titles = TextAreaField('Alternative titles', validators=[Optional()])
    country_codes = StringField('Country codes', validators=[InputRequired()])
    website_url = StringField('Website URL', validators=[Optional()])
    website_offline = BooleanField('Website is offline')


class CreatePartyFormBase(Form):
    slug = StringField('Slug', validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    series_slug = StringField('Series slug', validators=[Optional()])
    organizer_entity = StringField('Organizer entity', validators=[Optional()])
    start_on = DateField('Start on', validators=[InputRequired()])
    end_on = DateField('End on', validators=[InputRequired()])
    attendees = IntegerField('Attendees', validators=[Optional()])
    website_url = StringField('Website URL', validators=[Optional()])
    website_offline = BooleanField('Website is offline')


class CreateOfflinePartyForm(CreatePartyFormBase):
    seats = IntegerField('Seats', validators=[InputRequired()])
    location_country_code = StringField('Country code', validators=[InputRequired()])
    location_city = StringField('City', validators=[InputRequired()])
    location_name = StringField('Name', validators=[Optional()])
    location_postal_code = StringField('Postal code', validators=[Optional()])
    location_street = StringField('Street', validators=[Optional()])
    location_latitude = StringField('Latitude', validators=[Optional()])
    location_longitude = StringField('Longitude', validators=[Optional()])


class CreateOnlineOnlyPartyForm(CreatePartyFormBase):
    pass
