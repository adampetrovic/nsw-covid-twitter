from jinja2 import Template, Environment


def pluralize(number, singular='', plural='s'):
    if number == 1:
        return singular
    else:
        return plural


env = Environment()
env.filters['pluralize'] = pluralize

AGGREGATE_TEMPLATE = env.from_string(
"""⚠️ {{ venue_count }} new venue{{ venue_count | pluralize }} added in {{ suburbs | length }} suburb{{ suburbs | length | pluralize }}.
See thread for venue details 🧵👇
Updated: {{ now }} #nswcovidvenue
""")

CASE_TEMPLATE = env.from_string(
"""{{ venue.suburb | upper }}: {{ venue.name }}
{% for date in dates %}
{{- date[0].strftime('%a %d/%b') }} {{ date[1] or '' }}
{% endfor %}

Address: {{ venue.address}}, {{ venue.suburb }}
{{ venue.alert -}}""")