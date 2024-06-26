from django.db import models

from customer_auth.models import Customer

class Emirate(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Freezone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="", blank=False)
    allowed_packages = models.TextField(default="", blank=False)
    compliance_details = models.TextField(default="", blank=False)

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
    freezone_and_emirate = models.ForeignKey(FreezoneInEmirates, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('freezone_and_emirate', 'business')

    def __str__(self):
        return f"{self.business.name} in {self.freezone_and_emirate.freezone.name} in {self.freezone_and_emirate.emirate.name}"
    

class VisaPackage(models.Model):
    number_of_package = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.number_of_package}"
    

class VisaPackagesInBusiness(models.Model):
    business_in_freezone = models.ForeignKey(BusinessInFreezone, on_delete=models.CASCADE)
    visa_packages = models.ForeignKey(VisaPackage, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('business_in_freezone', 'visa_packages')

    def __str__(self) -> str:
        return f"{self.visa_packages.number_of_package} in {self.business_in_freezone.freezone_and_emirate.freezone} on {self.business_in_freezone.freezone_and_emirate.emirate}"
    

class Quotation(models.Model):
    emirate = models.ForeignKey(Emirate, on_delete=models.CASCADE, related_name="emirate_details")
    freezone = models.ForeignKey(Freezone, on_delete=models.CASCADE, related_name='details')
    business_activity = models.ForeignKey(BusinessActivity, on_delete=models.CASCADE, related_name='details')
    visa_packages = models.ForeignKey(VisaPackage, on_delete=models.CASCADE, null=True, blank=True)
    license_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    establishment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    e_channel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    residence_visa = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('freezone', 'business_activity', 'visa_packages')

    def __str__(self):
        return f"{self.freezone} - {self.business_activity}"
    
    def total(self):
        sum = self.license_cost + self.e_channel + self.medical + self.residence_visa + self.establishment
        return sum
    
    def save(self, *args, **kwargs):
        self.total_amount = self.total()
        freezone_and_emirate_mapping, created = FreezoneInEmirates.objects.get_or_create(
            emirate=self.emirate,
            freezone=self.freezone
        )
        business_in_freezone, created = BusinessInFreezone.objects.get_or_create(
            freezone_and_emirate=freezone_and_emirate_mapping,
            business=self.business_activity
        )
        visa_packages, created = VisaPackagesInBusiness.objects.get_or_create(business_in_freezone=business_in_freezone, visa_packages=self.visa_packages)
        super().save(*args, **kwargs)


class LogoImage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    image = models.CharField(max_length=500)