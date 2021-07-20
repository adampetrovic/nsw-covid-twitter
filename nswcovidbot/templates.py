from jinja2 import Template
import arrow

AGGREGATE_TEMPLATE = Template(
"""⚠️ {{ venue_count }} New venues added in {{ suburbs | length }} suburbs.
See thread for venue details 🧵👇
Updated: {{ now }} #nswcovidvenue
""")

AGGREGATE_TEMPLATE.globals['now'] = arrow.get(tzinfo='Australia/Sydney').format('ddd D/MMM h:mma')

CASE_TEMPLATE = Template(
"""{{ venue.suburb | upper }}: {{ venue.name }}
{% for date in dates %}
{{- date[0].strftime('%a %d/%b') }} {{ date[1] or '' }}
{% endfor %}

Address: {{ venue.address}}, {{ venue.suburb }}
{{ venue.alert -}}""")
