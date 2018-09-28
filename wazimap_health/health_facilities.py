from .models import HealthFacilities


def pharmacies(reader, code_prefix):
    code = 5084
    for row in reader:
        row.pop('Province')
        row.pop('District')
        row.pop('Sub-District')
        HealthFacilities\
            .objects\
            .update_or_create(
                {
                    'name': row.pop('Facility'),
                    'settlement': row.pop('Organization Unit Rural_Urban_Semi'),
                    'latitude': row.pop('Latitude'),
                    'longitude': row.pop('Longitude'),
                    'unit': row.pop('Organization Unit Type'),
                    'address': row.pop('Physical Address'),
                    'dataset': 'private_pharmacies',
                    'facility_code': '{}{}'.format(code_prefix, code),
                    'service': dict(row)
                },
                facility_code='{}{}'.format(code_prefix, code)
            )
        code += 1
        print("Facility Entered")
    print(code)


def public_facilities(reader, code_prefix):
    code = 19
    for row in reader:
        row.pop('Province')
        row.pop('District')
        row.pop('Sub-District')
        row.pop('Facility Name 1')
        HealthFacilities\
            .objects\
            .update_or_create(
                {
                    'name': row.pop('Facility Name_2'),
                    'settlement': row.pop('Organization Unit Rural_Urban_Semi'),
                    'unit': row.pop('Organization Unit Type'),
                    'latitude': row.pop('Latitude'),
                    'longitude': row.pop('Longitude'),
                    'facility_code': '{}{}'.format(code_prefix, code),
                    'dataset': 'public_health',
                    'service': dict(row)
                },
                facility_code='{}{}'.format(code_prefix, code)
            )
        code += 1
        print("Facility Entered")
    print(code)


def marie_stopes(reader, code_prefix):
    code = 1
    for row in reader:
        row.pop('Province')
        row.pop('Sub-District')
        HealthFacilities\
            .objects\
            .update_or_create(
                {
                    'name': row.pop('Facility'),
                    'settlement': row.pop('Org Unit Rural_Urban_Semi'),
                    'latitude': row.pop('Latitude'),
                    'longitude': row.pop('Longitude'),
                    'address': row.pop('Physical Address'),
                    'facility_code': '{}{}'.format(code_prefix, code),
                    'dataset': 'marie_stopes',
                    'service': dict(row)
                },
                facility_code='{}{}'.format(code_prefix, code)
            )
        code += 1
        print("Facility Entered")
    print(code)
