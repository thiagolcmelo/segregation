from django.db import models

# Create your models here.

class Alloy(models.Model):
    name = models.CharField("Alloy's name", max_length = 30)
    alloy_size = (
        ('d', 'Double'),
        ('d', 'Ternary')
    )
    def __str__(self):
        return self.name
    
class Parameter(models.Model):
    alloy = models.ForeignKey(Alloy, verbose_name="The related alloy")
    a0 = models.FloatField("Lattice parameter")
    ac = models.FloatField("Conductions's hydrostatic deformation potential")
    av = models.FloatField("Valence's hydrostatic deformation potential")
    b = models.FloatField("Deformation potential for tetragonal distorion")
    c11 = models.FloatField("Elastic constant")
    c12 = models.FloatField("Elastic constant")
    me = models.FloatField("Electron effective mass")
    mhh = models.FloatField("Heavy-hole effective mass", null = True)
    mlh = models.FloatField("Light-hole effective mass", null = True)
    eg2 = models.FloatField("Gap energy at 2 K")
    eg77 = models.FloatField("Gap energy at 77 K")
    eg300 = models.FloatField("Gap energy at 300 K")
    def __str__(self):
        return self.alloy.name + "'s parameters"
    
class Interpolation(models.Model):
    alloy = models.ForeignKey(Alloy, verbose_name="The related alloy")
    a0 = models.CharField("Lattice parameter", max_length = 200)
    ac = models.CharField("Conductions's hydrostatic deformation potential", max_length = 200)
    av = models.CharField("Valence's hydrostatic deformation potential", max_length = 200)
    b = models.CharField("Deformation potential for tetragonal distorion", max_length = 200)
    c11 = models.CharField("Elastic constant", max_length = 200)
    c12 = models.CharField("Elastic constant", max_length = 200)
    me = models.CharField("Electron effective mass", max_length = 200)
    mhh = models.CharField("Heavy-hole effective mass", max_length = 200, null = True)
    mlh = models.CharField("Light-hole effective mass", max_length = 200, null = True)
    eg2 = models.CharField("Gap energy at 2 K", max_length = 200)
    eg77 = models.CharField("Gap energy at 77 K", max_length = 200)
    eg300 = models.CharField("Gap energy at 300 K", max_length = 200)
    def __str__(self):
        return self.alloy.name + "'s interpolations"