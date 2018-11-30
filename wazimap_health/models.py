from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.text import slugify


class HealthFacilities(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    settlement = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    facility_code = models.CharField(max_length=20, unique=True)
    geo_levels = ArrayField(
        models.CharField(max_length=20), blank=True, null=True)
    dataset = models.CharField(max_length=50)
    service = HStoreField()

    class Meta:
        db_table = 'health_facilities'
        unique_together = ('name', 'latitude', 'longitude', 'facility_code')

    def __str__(self):
        return self.name


class HigherEducation(models.Model):
    institution = models.CharField(max_length=100)
    name = models.CharField(max_length=100, verbose_name='School Name')
    facility_code = models.CharField(max_length=100, unique=True)
    classification = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100, blank=True)
    dataset = models.CharField(max_length=20)
    geo_levels = ArrayField(
        models.CharField(max_length=20), blank=True, null=True)
    service = HStoreField()

    class Meta:
        db_table = 'higher_education'
        unique_together = ('name', 'latitude', 'longitude', 'institution')

    def __str__(self):
        return self.name


class BasicEducation(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=50, blank=True)
    phase = models.CharField(max_length=20, blank=True)
    special_need = models.CharField(max_length=5)
    dataset = models.CharField(max_length=50)
    facility_code = models.CharField(max_length=100, unique=True)
    geo_levels = ArrayField(
        models.CharField(max_length=20), blank=True, null=True)
    service = HStoreField()

    class Meta:
        db_table = 'basic_education'
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name


class Organisation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='uploads/')
    slug = models.SlugField(
        null=True, blank=True, allow_unicode=True, max_length=255)

    class Meta:
        db_table = 'partner_orgainisation'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Organisation, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Contact(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    class Meta:
        db_table = 'partner_contact'
        unique_together = ('organisation', 'name')

    def __str__(self):
        return self.name


class Activity(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='activities')
    activity_number = models.IntegerField()
    hiv_aids_focus = models.BooleanField(verbose_name='Main Focus on HIV/AIDS')
    category = models.CharField(
        max_length=100,
        verbose_name='Implementation activity category',
        blank=True,
        null=True)
    other_category = models.CharField(max_length=100, blank=True, null=True)
    donor_agency = models.CharField(max_length=100, blank=True, null=True)
    activity = models.CharField(max_length=255, blank=True, null=True)
    she_conquers_element = models.CharField(
        max_length=100, blank=True, null=True)
    other_she_conquers = models.CharField(
        max_length=255, blank=True, null=True)
    timeline = models.CharField(max_length=100, blank=True, null=True)
    audience = models.CharField(max_length=255, blank=True, null=True)
    other_audience = models.CharField(max_length=255, blank=True, null=True)
    location_type = models.CharField(max_length=255, blank=True, null=True)
    other_location_type = models.CharField(
        max_length=255, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    more_province = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'partner_activity'

    def __str__(self):
        return self.activity


class Target(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='targets')
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='target_activity',
        null=True)
    audience = models.CharField(max_length=255, blank=True, null=True)
    other_audience = models.CharField(max_length=255, blank=True, null=True)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_target'

    def __str__(self):
        return self.audience


class AreaImplementation(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='area_activity',
        null=True)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='areas')
    location_type = models.CharField(max_length=255, blank=True, null=True)
    other_location_type = models.CharField(
        max_length=255, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    more_province = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.TextField(blank=True, null=True)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_area_implementation'

    def __str__(self):
        return self.province


class PartnerHigherEducation(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='higher_ed')
    province = models.CharField(max_length=50)
    institution = models.CharField(max_length=50)
    campus = models.CharField(max_length=100)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_higher_education_facilities'

    def __str__(self):
        return self.institution


class PartnerHealth(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='health')
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    facility = models.CharField(max_length=50)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_health_facilities'

    def __str__(self):
        return self.facility


class PartnerBasicEducation(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='basic_ed')
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    activity_number = models.CharField(max_length=10)

    class Meta:
        db_table = 'partner_basic_education_facilities'

    def __str__(self):
        return self.school
