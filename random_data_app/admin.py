from django.contrib import admin

from random_data_app.models.population import Population, PopulationMember, Sample, FieldSpec, ChoiceDistribution
#from random_data_app.models.sample import Sample
from random_data_app.models.demo import Name
import random
# Register your models here
class NameAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public', 'added', 'used', 'population')
    fields = ('name', 'is_public', 'added', 'used', 'avatar', 'avatar_tag', 'population', 'rel')
    readonly_fields = ('avatar_tag', 'population')

    def population(self, obj):
        #print obj.__dict__
        #ct = ContentType.objects.get(model="Name")
        #p = Population.objects.filter(model=ct)
        #pm = PopulationMember.objects.filter(content_type__model="Name", name__id=obj.id)

        #if (len(pm) > 0):
        #    return str(pm.population)
        pm = PopulationMember.objects.filter(content_type__model="name", object_id=obj.id)
        if range(len(pm)):
            return " ,".join([str(m.population.id) for m in pm])

        return "no population"


class ChoiceDistributionAdmin(admin.ModelAdmin):
    pass

class ChoiceDistributionInline(admin.TabularInline):
    model = ChoiceDistribution
    extra = 0

class FieldSpecAdmin(admin.ModelAdmin):
    list_display = ('field_type', 'field_name', 'random')
    fields = ('field_type', 'field_name', 'random')
    inlines = [ChoiceDistributionInline]


class FieldSpecInline(admin.TabularInline):
    model = FieldSpec
    extra = 0

class SampleInline(admin.StackedInline):
    model = Sample
    readonly_fields = ('population', 'member')
    extra = 1

class PopulationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
            (None, {
                'fields':('name',)
            }),
        )
    inlines = [SampleInline]

    def get_model_fields(self, obj):
        print obj
        return ""

class PopulationMemberInline(admin.TabularInline):
    model = PopulationMember
    fields = ('population', 'content_object')

class SampleAdmin(admin.ModelAdmin):
    list_display = ('population', 'size', 'member_count')
    fields = ('population', 'member', 'size', 'model', 'specs')
    readonly_fields = ('member',)

    def member_count(self, obj):
        m = PopulationMember.objects.filter(population=obj.population, content_type=obj.model)
        return str(len(m))

admin.site.register(Name, NameAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(PopulationMember)
admin.site.register(Sample, SampleAdmin)
admin.site.register(ChoiceDistribution, ChoiceDistributionAdmin)
admin.site.register(FieldSpec, FieldSpecAdmin)
