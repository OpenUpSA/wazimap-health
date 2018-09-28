from .models import HealthFacilities, BasicEducation, HigherEducation

DATASET_CHOICE = (('public_health', 'Public Health Facilities'),
                  ('private_pharmacies',
                   'Private Pharamacies'), ('marie_stopes', 'Marie Stopes'))


class ProcessImport():
    """
    process the imported csv to the correct model
    """

    def __init__(self, dataset, reader):
        self.dataset = dataset
        self.reader = reader

    def process_type(self):
        return {
            'basic_education': self.process_basic_education,
            'higher_education': self.process_higher_education,
            'marie_stopes': self.process_health,
            'public_health': self.process_health,
            'private_pharmacies': self.process_health
        }

    def import_csv(self):
        process = self.process_type()
        process[self.dataset]()

    def process_health(self):
        try:
            for row in self.reader:
                code = row['facility_code']
                HealthFacilities\
                    .objects\
                    .update_or_create(
                        {
                            'name': row.pop('name'),
                            'settlement': row.pop('settlement'),
                            'unit': row.pop('unit'),
                            'latitude': row.pop('latitude'),
                            'longitude': row.pop('longitude'),
                            'address': row.pop('address'),
                            'facility_code': row.pop('facility_code'),
                            'dataset': self.dataset,
                            'service': dict(row)
                        },
                        facility_code=code
                    )
        except Exception as error:
            raise

    def process_basic_education(self):
        try:
            for row in self.reader:
                code = row['facility_code']
                BasicEducation\
                    .objects\
                    .update_or_create(
                        {
                            'name': row.pop('name'),
                            'sector': row.pop('sector'),
                            'phase': row.pop('phase') or '',
                            'latitude': row.pop('latitude'),
                            'longitude': row.pop('longitude'),
                            'address': row.pop('address'),
                            'special_need': row.pop('special_need'),
                            'dataset': 'basic_education',
                            'facility_code': row.pop('facility_code'),
                            'service': dict(row)
                        },
                        facility_code=code
                    )
        except Exception as error:
            raise

    def process_higher_education(self):
        try:
            for row in self.reader:
                code = row['facility_code']
                HigherEducation\
                    .objects\
                    .update_or_create(
                        {
                            'name': row.pop('name'),
                            'classification': row.pop('classification'),
                            'latitude': row.pop('latitude'),
                            'longitude': row.pop('longitude'),
                            'institution': row.pop('institution'),
                            'address': row.pop('address'),
                            'dataset': 'higher_education',
                            'facility_code': row.pop('facility_code'),
                            'service': dict(row)
                        },
                        facility_code=code
                    )
        except Exception:
            raise
