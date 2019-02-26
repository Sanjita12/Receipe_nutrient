from django.db import models

class Ingredient(models.Model):
    NDB_No = models.CharField(max_length=5, primary_key=True)
    FdGrp_Cd = models.CharField(max_length=4)
    Long_Desc = models.CharField(max_length=200)
    Shrt_Desc = models.CharField(max_length=60)
    ComName = models.CharField(max_length=100, null=True, blank=True)
    ManufacName = models.CharField(max_length=65, null=True, blank=True)
    Survey = models.CharField(max_length=1, null=True, blank=True)
    Ref_desc = models.CharField(max_length=135, null=True, blank=True)
    Refuse = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    SciName = models.CharField(max_length=65, null=True, blank=True)
    N_Factor = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    Pro_Factor = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    Fat_Factor = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    CHO_Factor = models.DecimalField(max_digits=4, decimal_places=2, blank=True,  null=True)

class NutrientDef(models.Model):
    Nutr_No = models.CharField(max_length=3, primary_key=True)
    Units = models.CharField(max_length=7)
    Tagname = models.CharField(max_length=20, null=True, blank=True)
    NutrDesc = models.CharField(max_length=60)
    Num_Dec = models.CharField(max_length=1)
    SR_Order =  models.DecimalField(max_digits=48, decimal_places=6)

class FetchSmallNutrientReportManager(models.Manager):
    def get_queryset(self):
        major_nutrient_no = ['208', '203', '204', '205', '291', '269']
        return super().get_queryset().select_related('Nutr_No').filter(Nutr_No__in=major_nutrient_no).order_by('Nutr_No')

class Nutrient(models.Model):
    Nutr_No = models.ForeignKey('NutrientDef', on_delete=models.CASCADE, related_name='nutrient_def')
    NDB_No = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='nutrients')
    Nutr_Val = models.DecimalField(max_digits=10, decimal_places=3)
    Std_Error = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    Deriv_Cd = models.CharField(max_length=4, null=True, blank=True)
    Ref_NDB_No = models.CharField(max_length=5, null=True, blank=True)
    Add_Nutr_Mark = models.CharField(max_length=1, null=True, blank=True)
    objects = models.Manager()
    small_reports = FetchSmallNutrientReportManager()

    class Meta:
        unique_together = (('NDB_No', 'Nutr_No'),)



class Weight(models.Model):
    NDB_No = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='weights')
    Seq = models.CharField(max_length=3)
    Msre_Desc = models.CharField(max_length=84, null=True)
    Amount = models.DecimalField(max_digits=5, decimal_places=3)
    Gm_Wgt = models.DecimalField(max_digits=7, decimal_places=1)
    Std_Dev = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)

    class Meta:
        unique_together = (('NDB_No', 'Seq'),)

