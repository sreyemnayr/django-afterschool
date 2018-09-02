from django.db import models

from django.utils import timezone
from datetime import datetime, timedelta

def ceil_dt(dt, delta):
    return dt + (datetime.min - timezone.make_naive(dt)) % delta


class DayofWeek(models.Model):
	MONDAY = '0'
	TUESDAY = '1'
	WEDNESDAY = '2'
	THURSDAY = '3'
	FRIDAY = '4'
	DOW_CHOICES = (
		(MONDAY, 'Monday'),
		(TUESDAY, 'Tuesday'),
		(WEDNESDAY, 'Wednesday'),
		(THURSDAY, 'Thursday'),
		(FRIDAY, 'Friday'),

	)
	day = models.CharField(max_length=2, choices=DOW_CHOICES)

	class Meta:
		verbose_name = 'day_of_week'
		verbose_name_plural = 'days_of_the_week'
		#app_label = 'afterschool.students'

	def __str__(self):
		if self.day == '0':
			return 'Monday'
		elif self.day == '1':
			return 'Tuesday'
		elif self.day == '2':
			return 'Wednesday'
		elif self.day == '3':
			return 'Thursday'
		elif self.day == '4':
			return 'Friday'
		else:
			return 'ERROR'


class Student(models.Model):
	name = models.CharField(max_length=60)
	first_name = models.CharField(max_length=60, null=True, blank=True)
	last_name = models.CharField(max_length=60, null=True, blank=True)
	nickname = models.CharField(max_length=60, null=True, blank=True)
	grade = models.SmallIntegerField(default=-6)
	schedule = models.ManyToManyField(DayofWeek, related_name='students', blank=True)
	pcr_id = models.SmallIntegerField(null=True, blank=True)
	
	class Meta:
		verbose_name = 'student'
		verbose_name_plural = 'students'
		indexes=[
			models.Index(fields=['pcr_id']),
			models.Index(fields=['grade','last_name']),
			]
		#app_label = 'afterschool.students'

	@property
	def gradestr(self):
		if self.grade is -4:
			return 'Ones'
		elif self.grade is -3:
			return 'Twos'
		elif self.grade is -2:
			return 'PreK-3'
		elif self.grade is -1:
			return 'PreK'
		elif self.grade is 0:
			return 'Kinder'
		elif self.grade is 1:
			return '1st'
		elif self.grade is 2:
			return '2nd'
		elif self.grade is 3:
			return '3rd'
		elif self.grade is 4:
			return '4th'
		elif self.grade is 5:
			return '5th'
		elif self.grade is 6:
			return '6th'
		elif self.grade is 7:
			return '7th'
		elif self.grade is 8:
			return '8th'
		else:
			return str(self.grade)


	def __str__(self):
		return self.name + ' ('+str(self.gradestr)+')'


class Family(models.Model):
	name = models.CharField(max_length=60)
	children = models.ManyToManyField(Student, related_name='families', related_query_name='family')

	class Meta:
		verbose_name = 'family'
		verbose_name_plural = 'families'
		#app_label = 'afterschool.students'

	def __str__(self):
		return self.name + ' (' + ','.join([str(child) for child in self.children.all()]) + ')'

class Session(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField(null=True)
	student = models.ForeignKey(Student, related_name='sessions', on_delete=models.SET_NULL, null=True)
	parent = models.CharField(max_length=60,null=True)

	class Meta:
		verbose_name = 'session'
		verbose_name_plural = 'sessions'

		#app_label = 'afterschool.students'

	@property
	def duration(self):
		"Returns the duration of the session in hours"
		if self.end is None:
			return (ceil_dt(timezone.now(),timedelta(minutes=15)) - self.start).total_seconds() / 3600  
		else:
			return (self.end - self.start).total_seconds() / 3600

	def __str__(self):
		return str(self.student) + ' ' + self.start.strftime('%x')

class ScheduledClass(models.Model):
	start = models.TimeField()
	end = models.TimeField()
	weekday = models.SmallIntegerField()
	student = models.ForeignKey(Student, related_name='scheduled_classes', on_delete=models.SET_NULL, null=True)
	course = models.CharField(max_length=60,null=True)
	room = models.CharField(max_length=60,null=True)
	teacher = models.CharField(max_length=60,null=True)

	class Meta:
		indexes = [
			models.Index(fields=['student','weekday','course','room','start','end']),
		]
	
	def __str__(self):
		return str(self.student) + ': [' + str(self.room) + '] ' + str(self.course) + ' (' + str(self.teacher) + ')'
