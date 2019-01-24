from django import template
register = template.Library()


@register.filter
def activity(partner_data, activity_number):
    "return any facilities that have a matching activity number"
    if partner_data:
        return [
            facility for facility in partner_data
            if facility.activity_number == activity_number
        ]
    else:
        return []
