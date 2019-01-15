from django import forms
from django.db import IntegrityError
from django.db import transaction
from models import (Organisation, PartnerBasicEducation, PartnerHealth,
                    PartnerHigherEducation)
from openpyxl import load_workbook
import traceback


class PartnerForm(forms.Form):
    excel_sheet = forms.FileField()
    logo = forms.ImageField()


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
        org_name = sheet['A8'].value
        org = Organisation.objects.create(name=org_name, logo=logo)

        contact = sheet['B8':'D15']
        persons = []
        for person in contact:
            if not is_row_empty(person):
                persons.append({
                    'name': person[0].value,
                    'email': person[1].value,
                    'phone': person[2].value
                })
        activity = sheet['E8':'U20']
        for act in activity:
            if not is_row_empty(act):
                row_activities = {
                    'activity_number': act[0].value,
                    'hiv_aids_focus': True if act[1].value == 'Yes' else False,
                    'category': act[2].value,
                    'other_category': act[3].value,
                    'donor_agency': act[4].value,
                    'activity': act[5].value,
                    'she_conquers_element': act[6].value,
                    'other_she_conquers': act[7].value,
                    'timeline': act[8].value,
                    'audience': act[9].value,
                    'other_audience': act[10].value,
                    'location_type': act[11].value,
                    'other_location_type': act[12].value,
                    'province': act[13].value,
                    'more_province': act[14].value,
                    'district': act[15].value,
                    'municipality': act[16].value
                }
                org.activities.create(**row_activities)

        for p in persons:
            try:
                org.contacts.create(**p)
            except IntegrityError:
                pass
        process_basic_education(org, template)
        process_health(org, template)
        process_higher_education(org, template)
    except Exception as error:
        traceback.print_exc()
        raise


def process_higher_education(organisation, template):
    """
    Inset the institutions that the organisation is working in.
    """
    partner_locations = []
    sheet = template['University and TVETS']
    location = sheet['A2':'D560']
    for place in location:
        if place[3].value is not None:
            try:
                for act_no in place[3].value.split(','):
                    partner_locations.append(
                        PartnerHigherEducation(
                            organisation=organisation,
                            province=place[0].value,
                            institution=place[1].value,
                            campus=place[2].value,
                            activity_number=act_no))
            except AttributeError:
                partner_locations.append(
                    PartnerHigherEducation(
                        organisation=organisation,
                        province=place[0].value,
                        institution=place[1].value,
                        campus=place[2].value,
                        activity_number=place[3].value))
    if partner_locations:
        organisation.higher_ed.bulk_create(partner_locations)


def process_basic_education(organisation, template):
    """
    Save the schools that the org is working in
    """
    partner_locations = []
    sheet = template['Basic Ed. Facilities sheet']
    location = sheet['A2':'D25290']
    for place in location:
        if place[3].value is not None:
            try:
                for act_no in place[3].value.split(','):
                    partner_locations.append(
                        PartnerBasicEducation(
                            organisation=organisation,
                            province=place[1].value,
                            district=place[0].value,
                            school=place[2].value,
                            activity_number=act_no))
            except AttributeError:
                partner_locations.append(
                    PartnerBasicEducation(
                        organisation=organisation,
                        province=place[1].value,
                        district=place[0].value,
                        school=place[2].value,
                        activity_number=place[3].value))
    if partner_locations:
        organisation.basic_ed.bulk_create(partner_locations)


def process_health(organisation, template):
    """
    Save the health facilities that the org is working in
    """
    partner_locations = []
    sheet = template['Public health facilities sheet']
    location = sheet['A2':'D5060']
    for place in location:
        if place[3].value is not None:
            try:
                for act_no in place[3].value.split(','):
                    partner_locations.append(
                        PartnerHealth(
                            organisation=organisation,
                            province=place[1].value,
                            district=place[0].value,
                            facility=place[2].value,
                            activity_number=act_no))
            except AttributeError:
                partner_locations.append(
                    PartnerHealth(
                        organisation=organisation,
                        province=place[1].value,
                        district=place[0].value,
                        facility=place[2].value,
                        activity_number=place[3].value))
    if partner_locations:
        organisation.health.bulk_create(partner_locations)
