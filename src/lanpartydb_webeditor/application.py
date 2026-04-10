"""
lanpartydb_webeditor.application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2024-2026 Jochen Kupperschmidt
:License: MIT
"""

from decimal import Decimal

from flask import Blueprint, Flask, render_template, request, Response
import jinja2
from lanpartydb.models import Location, Party, PartyLinks, Resource, Series, SeriesLinks
from lanpartydb.serialization import serialize_party_to_toml, serialize_series_to_toml
from wtforms import BooleanField, DateField, Form, IntegerField, StringField
from wtforms.validators import InputRequired, Optional, ReadOnly

from .forms import CreateOfflinePartyForm, CreateOnlineOnlyPartyForm, CreateSeriesForm


blueprint = Blueprint('blueprint', __name__)


@blueprint.get('/')
def index():
    return render_template('index.html')


@blueprint.get('/series/create')
def create_series_form(*, erroneous_form: CreateSeriesForm = None, output: str = ''):
    form = erroneous_form if erroneous_form else CreateSeriesForm()

    context = {
        'form': form,
        'output': output,
    }

    return render_template('create_series_form.html', **context)


@blueprint.post('/series/create')
def create_series():
    form = CreateSeriesForm(request.form)

    if not form.validate():
        return create_series_form(erroneous_form=form)

    series = _build_series(form)
    toml = serialize_series_to_toml(series)

    if request.args.get('download') == 'true':
        filename = f'{series.slug}.toml'
        return _build_toml_download_response(toml, filename)
    else:
        return create_series_form(erroneous_form=form, output=toml)


def _build_series(form: CreateSeriesForm) -> Series:
    def split(s: str, delimiter: str) -> list[str]:
        tokens = s.split(delimiter)
        stripped = [token.strip() for token in tokens]
        return [token for token in stripped if token]

    slug = form.slug.data.strip().lower()
    title = form.title.data.strip()
    alternative_titles = split(form.alternative_titles.data, '\r\n')
    country_codes = split(form.country_codes.data, ',')
    website_url = form.website_url.data.strip()
    website_offline = form.website_offline.data

    if website_url:
        links = SeriesLinks(
            website=Resource(
                url=website_url,
                offline=website_offline,
            ),
        )
    else:
        links = None

    return Series(
        slug=slug,
        title=title,
        alternative_titles=alternative_titles,
        country_codes=country_codes,
        links=links,
    )


@blueprint.get('/party/offline/create')
def create_offline_party_form(
    *, erroneous_form: CreateOfflinePartyForm = None, output: str = ''
):
    form = erroneous_form if erroneous_form else CreateOfflinePartyForm()

    context = {
        'form': form,
        'output': output,
    }

    return render_template('create_offline_party_form.html', **context)


@blueprint.post('/party/offline/create')
def create_offline_party():
    form = CreateOfflinePartyForm(request.form)

    if not form.validate():
        return create_offline_party_form(erroneous_form=form)

    party = _build_offline_party(form)
    toml = serialize_party_to_toml(party)

    if request.args.get('download') == 'true':
        filename = f'{party.slug}.toml'
        return _build_toml_download_response(toml, filename)
    else:
        return create_offline_party_form(erroneous_form=form, output=toml)


def _build_offline_party(form: CreateOfflinePartyForm) -> Party:
    def to_decimal(s: str | None) -> Decimal | None:
        return Decimal(s) if (s is not None) else None

    slug = form.slug.data.strip().lower()
    title = form.title.data.strip()
    series_slug = form.series_slug.data.strip() or None
    organizer_entity = form.organizer_entity.data.strip() or None
    start_on = form.start_on.data
    end_on = form.end_on.data
    seats = form.seats.data
    attendees = form.attendees.data or None
    location_country_code = form.location_country_code.data
    location_city = form.location_city.data
    location_name = form.location_name.data or None
    location_postal_code = form.location_postal_code.data or None
    location_street = form.location_street.data or None
    location_latitude = to_decimal(form.location_latitude.data or None)
    location_longitude = to_decimal(form.location_longitude.data or None)
    website_url = form.website_url.data.strip()
    website_offline = form.website_offline.data

    location = Location(
        name=location_name,
        country_code=location_country_code,
        city=location_city,
        postal_code=location_postal_code,
        street=location_street,
        latitude=location_latitude,
        longitude=location_longitude,
    )

    if website_url:
        links = PartyLinks(
            website=Resource(
                url=website_url,
                offline=website_offline,
            ),
        )
    else:
        links = None

    return Party(
        slug=slug,
        title=title,
        series_slug=series_slug,
        organizer_entity=organizer_entity,
        start_on=start_on,
        end_on=end_on,
        online_only=False,
        seats=seats,
        attendees=attendees,
        location=location,
        links=links,
    )


@blueprint.get('/party/online_only/create')
def create_online_only_party_form(
    *, erroneous_form: CreateOnlineOnlyPartyForm = None, output: str = ''
):
    form = erroneous_form if erroneous_form else CreateOnlineOnlyPartyForm()

    context = {
        'form': form,
        'output': output,
    }

    return render_template('create_online_only_party_form.html', **context)


@blueprint.post('/party/online_only/create')
def create_online_only_party():
    form = CreateOnlineOnlyPartyForm(request.form)

    if not form.validate():
        return create_online_only_party_form(erroneous_form=form)

    party = _build_online_only_party(form)
    toml = serialize_party_to_toml(party)

    if request.args.get('download') == 'true':
        filename = f'{party.slug}.toml'
        return _build_toml_download_response(toml, filename)
    else:
        return create_online_only_party_form(erroneous_form=form, output=toml)


def _build_online_only_party(form: CreateOnlineOnlyPartyForm) -> Party:
    slug = form.slug.data.strip().lower()
    title = form.title.data.strip()
    series_slug = form.series_slug.data.strip() or None
    organizer_entity = form.organizer_entity.data.strip() or None
    start_on = form.start_on.data
    end_on = form.end_on.data
    attendees = form.attendees.data or None
    website_url = form.website_url.data.strip()
    website_offline = form.website_offline.data

    if website_url:
        links = PartyLinks(
            website=Resource(
                url=website_url,
                offline=website_offline,
            ),
        )
    else:
        links = None

    return Party(
        slug=slug,
        title=title,
        series_slug=series_slug,
        organizer_entity=organizer_entity,
        start_on=start_on,
        end_on=end_on,
        online_only=True,
        seats=None,
        attendees=attendees,
        location=None,
        links=links,
    )


def _build_toml_download_response(toml: str, filename: str) -> Response:
    return _build_download_response(toml, 'application/toml', filename)


def _build_download_response(body: str, mimetype: str, filename: str) -> Response:
    response = Response(body, mimetype=mimetype)
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def create_app() -> Flask:
    app = Flask(__name__)

    # Throw an exception when an undefined name is referenced in a template.
    app.jinja_env.undefined = jinja2.StrictUndefined

    app.register_blueprint(blueprint)

    return app
