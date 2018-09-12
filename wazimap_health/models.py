from django.db import models


class PublicHealthFacilities(models.Model):
    name = models.CharField(max_length=100)
    settlement = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(decimal_places=5, max_digits=7, blank=True)
    longitude = models.DecimalField(decimal_places=5, max_digits=7, blank=True)
    parent_geo_code = models.CharField(max_length=10)
    facility_code = models.CharField(max_length=20, unique=True)

    #stats = PublicHealthQuerySet.as_manager()

    class Meta:
        db_table = 'public_health_facilities'
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name


class PublicHealthServices(models.Model):
    facility = models.ForeignKey(PublicHealthFacilities)
    oral_pills = models.BooleanField(verbose_name='Oral Pills (Contraception)', blank=True)
    injectables = models.BooleanField(blank=True)
    iud = models.BooleanField(verbose_name='IUDs (Contraception)', blank=True)
    female_sterialization = models.BooleanField(verbose_name='Female Sterilization (Contraception)', blank=True)
    male_sterialization = models.BooleanField(verbose_name='Male Sterilization (Contraception)', blank=True)
    male_circumcision = models.BooleanField(verbose_name='Male Medical Circumcision (MMC)')
    tb = models.BooleanField(verbose_name="TB", blank=True)
    maternal_health = models.BooleanField(verbose_name='Maternal Health', blank=True)
    mental_health = models.BooleanField(verbose_name='Mental Health', blank=True)
    child_health = models.BooleanField(verbose_name='Child Health', blank=True)
    oral_health = models.BooleanField(verbose_name='Oral Health Services',
                                      blank=True)
    rehabilitation = models.BooleanField(verbose_name='Rehabilitation Services',
                                         blank=True)
    minor_ailments = models.BooleanField(verbose_name='Minor Ailments', blank=True)
    std = models.BooleanField(verbose_name='Sexually Transmitted infections Screenings', blank=True)
    hiv_testing = models.BooleanField(verbose_name='HIV Testing', blank=True)
    hiv_treatment = models.BooleanField(verbose_name='HIV Treatment (ART)', blank=True)
    oral_prep = models.BooleanField(verbose_name='Oral PrEP', blank=True)
    first_trimester = models.BooleanField(verbose_name='Termination of Pregnancy - 1st Trimester', blank=True)
    second_trimester = models.BooleanField(verbose_name='Termination of Pregnancy - 2nd Trimester', blank=True)
    ayfs = models.BooleanField(verbose_name='AYFS Accredited', blank=True)
    ccmdd_pick = models.CharField(verbose_name='CCMDD Pick Up Point', blank=True, max_length=50)
    status = models.BooleanField(blank=True)
    implants = models.BooleanField(blank=True, verbose_name='Implants (Contraception)')

    class Meta:
        db_table = 'public_health_services'

    def __str__(self):
        return self.facility.name
