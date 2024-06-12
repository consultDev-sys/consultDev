from django.db import models

class Emirate(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Freezone(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class BusinessActivity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FreezoneInEmirates(models.Model):
    freezone = models.ForeignKey(Freezone, on_delete=models.CASCADE)
    emirate = models.ForeignKey(Emirate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('freezone', 'emirate')

    def __str__(self):
        return f"{self.freezone.name} in {self.emirate.name}"


class BusinessInFreezone(models.Model):
    business = models.ForeignKey(BusinessActivity, on_delete=models.CASCADE)
    freezone = models.ForeignKey(Freezone, on_delete=models.CASCADE)
    emirate = models.ForeignKey(Emirate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('freezone', 'emirate', 'business')

    def __str__(self):
        return f"{self.business.name} at {self.freezone.name} in {self.emirate.name}"
    

class Quotation(models.Model):
    emirate = models.ForeignKey(Emirate, on_delete=models.CASCADE, related_name="emirate_details")
    freezone = models.ForeignKey(Freezone, on_delete=models.CASCADE, related_name='details')
    business_activity = models.ForeignKey(BusinessActivity, on_delete=models.CASCADE, related_name='details')
    number_of_visa_packages = models.IntegerField(default=0)
    license_cost = models.DecimalField(max_digits=10, decimal_places=2)
    establishment = models.DecimalField(max_digits=10, decimal_places=2)
    e_channel = models.DecimalField(max_digits=10, decimal_places=2)
    residence_visa = models.DecimalField(max_digits=10, decimal_places=2)
    medical = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('freezone', 'business_activity')

    def __str__(self):
        return f"{self.freezone} - {self.business_activity}"
    
    def total(self):
        sum = self.license_cost + self.e_channel + self.medical + self.residence_visa + self.establishment
        return sum
    
    def save(self, *args, **kwargs):
        self.total_amount = self.total()
        super().save(*args, **kwargs)

