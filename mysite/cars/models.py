from django.db import models


class Cars(models.Model):
	brand = models.CharField(max_length=50)
	model = models.CharField(max_length=100)
	version = models.CharField(default='', max_length=100)
	year = models.IntegerField()
	prise_usd = models.IntegerField()
	prise_uah = models.IntegerField()
	race = models.CharField(max_length=50)
	transmission = models.CharField(max_length=20)
	region = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	engine_type = models.CharField(max_length=20)
	engine_capacity = models.FloatField()
	plate_number = models.CharField(max_length=20)
	vin_code = models.CharField(max_length=50)
	type_of_transport = models.CharField(max_length=20)
	body_type = models.CharField(max_length=20)
	drive_type = models.CharField(max_length=20)
	description = models.TextField()
	date_created = models.DateTimeField()
	date_added_to_DB = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Cars"
