from django.db import IntegrityError
from django.db import transaction
from partner.models import (Partner, BasicEducationFacility,
                            HigherEducationFacility, HealthFacility, Location)
from openpyxl import load_workbook
import traceback


def is_row_empty(row):
    """
    check if row contains only Nones
    """
    none_count = 0
    row_length = len(row)
    for r in row:
        if r.value is None:
            none_count += 1
    if none_count == row_length:
        return True
    return False


@transaction.atomic
def process_excelsheet(logo, excel_sheet):
    """
    process excel sheet and extract relevent information
    """
    try:
        template = load_workbook(excel_sheet)
        sheet = template['Partner input request']
        partner_name = sheet['A8'].value
        partner = Partner.objects.create(name=partner_name, logo=logo)

        contact = sheet['B8':'D15']
        persons = []
        for person in contact:
            if not is_row_empty(person):
                persons.append({
                    'name': person[0].value,
                    'email': person[1].value,
                    'phone': person[2].value
                })
        activity = sheet['E8':'P20']
        for act in activity:
            if not is_row_empty(act):
                row_activities = {
                    'activity_number': act[0].value,
                    'hiv_aids_focus': True if act[1].value == 'Yes' else False,
                    'category': act[2].value,
                    'donor_agency': act[3].value,
                    'activity': act[4].value,
                    'she_conquers_element': act[5].value,
                    'timeline': act[6].value,
                    'audience': act[7].value,
                    'location_type': act[8].value,
                    'province': act[9].value,
                    'district': act[10].value,
                    'municipality': act[11].value
                }
                partner.activities.create(**row_activities)

        for p in persons:
            try:
                partner.contacts.create(**p)
            except IntegrityError:
                pass
        process_basic_education(partner, template)
        process_health(partner, template)
        process_higher_education(partner, template)
        process_location(partner, template)
    except Exception as error:
        traceback.print_exc()
        raise


def process_higher_education(partner, template):
    """
    Inset the institutions that the partner is working in.
    """
    education_locations = []
    sheet = template['University and TVETS']
    location = sheet['A2':'D560']
    for place in location:
        if place[3].value is not None:
            try:
                for act_no in place[3].value.split(','):
                    education_locations.append(
                        HigherEducationFacility(
                            partner=partner,
                            province=place[0].value,
                            institution=place[1].value,
                            campus=place[2].value,
                            activity_number=act_no.strip()))
            except AttributeError:
                education_locations.append(
                    HigherEducationFacility(
                        partner=partner,
                        province=place[0].value,
                        institution=place[1].value,
                        campus=place[2].value,
                        activity_number=place[3].value))
    if education_locations:
        partner.higher_ed.bulk_create(education_locations)


def process_basic_education(partner, template):
    """
    Save the schools that the org is working in
    """
    education_locations = []
    sheet = template['Basic Ed. facilities sheet']
    location = sheet['A2':'D25290']
    for place in location:
        if place[3].value is not None:
            try:
                for act_no in place[3].value.split(','):
                    education_locations.append(
                        BasicEducationFacility(
                            partner=partner,
                            district=place[0].value,
                            province=place[1].value,
                            school=place[2].value,
                            activity_number=act_no.strip()))
            except AttributeError:
                education_locations.append(
                    BasicEducationFacility(
                        partner=partner,
                        district=place[0].value,
                        province=place[1].value,
                        school=place[2].value,
                        activity_number=place[3].value))
    if education_locations:
        partner.basic_ed.bulk_create(education_locations)


def process_health(partner, template):
    """
    Save the health facilities that the org is working in
    """
    health_locations = []
    sheet = template['Health facilities sheet']
    location = sheet['A2':'D5060']
    for place in location:
        if place[3].value is not None:
            try:
                for act_no in place[3].value.split(','):
                    health_locations.append(
                        HealthFacility(
                            partner=partner,
                            province=place[1].value,
                            district=place[0].value,
                            facility=place[2].value,
                            activity_number=act_no))
            except AttributeError:
                health_locations.append(
                    HealthFacility(
                        partner=partner,
                        province=place[1].value,
                        district=place[0].value,
                        facility=place[2].value,
                        activity_number=place[3].value))
    if health_locations:
        partner.health.bulk_create(health_locations)


def process_location(partner, template):
    """
    Extract the location that the partner will be working in.
    """
    locations = []
    district_sheet = template['Districts']
    muni_sheet = template['Municipalities']
    d_col_rows = district_sheet['A2':'D100']
    m_col_rows = muni_sheet['A2':'D300']
    for district in d_col_rows:
        if district[2].value is not None:
            try:
                for act_no in district[2].value.split(','):
                    locations.append(
                        Location(
                            partner=partner,
                            location_code=district[0].value,
                            location_name=district[1].value,
                            activity_number=act_no))
            except AttributeError:
                locations.append(
                    Location(
                        partner=partner,
                        location_code=district[0].value,
                        location_name=district[1].value,
                        activity_number=district[2].value))

    for muni in m_col_rows:
        if muni[2].value is not None:
            try:
                for act_no in muni[2].value.split(','):
                    locations.append(
                        Location(
                            partner=partner,
                            location_code=muni[0].value,
                            location_name=muni[1].value,
                            activity_number=act_no))
            except AttributeError:
                locations.append(
                    Location(
                        partner=partner,
                        location_code=muni[0].value,
                        location_name=muni[1].value,
                        activity_number=muni[2].value))
    if locations:
        partner.location.bulk_create(locations)
