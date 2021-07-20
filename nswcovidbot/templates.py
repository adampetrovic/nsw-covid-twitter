from jinja2 import Template

AGGREGATE_TEMPLATE = Template(
"""⚠️ {{ venue_count }} New venues added in {{ suburbs | length }} suburbs.
See thread for venue details 🧵👇
Updated: {{ now }} #nswcovidvenue
""")

CASE_TEMPLATE = Template(
"""{{ venue.suburb | upper }}: {{ venue.name }}
{% for date in dates %}
{{- date[0].strftime('%a %d/%b') }} {{ date[1] or '' }}
{% endfor %}

Address: {{ venue.address}}, {{ venue.suburb }}
{{ venue.alert -}}""")
