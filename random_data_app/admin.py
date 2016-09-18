from django.contrib import admin

from random_data_app.models.population import Population, PopulationMember, Sample, FieldSpec, ChoiceDistribution
#from random_data_app.models.sample import Sample
from random_data_app.models.demo import Name
import random
# Register your models here
class NameAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public', 'added', 'used', 'population')
    fields = ('name', 'is_public', 'added', 'used', 'avatar', 'avatar_tag', 'population')
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
    list_display = ('model_name', 'population_name_or_id', 'field_type', 'field_name', 'random')
    fields = ('field_type', 'field_name', 'random')
    inlines = [ChoiceDistributionInline]

    def model_name(self, obj):
        return str(obj.population.model)

    def population_name_or_id(self, obj):
        nm = obj.population.name
        if nm != None and len(nm) > 0:
            return str(nm)
        return str(obj.population.id)

class FieldSpecInline(admin.TabularInline):
    model = FieldSpec
    fields = ('field_type', 'field_name', 'random', 'choices')
    extra = 0

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        print db_field
        print request.__dict__
        print kwargs
        if db_field == 'choices':
            print "FGGGGFFFFFFFFFF"

        r = ChoiceDistribution.objects.filter(field=self.instance)
        kwargs["queryset"] = r
        """
        return super(FieldSpecInline, self).formfield_for_manytomany(db_field, request, **kwargs)
        #if db_field.name == 'choices':
            #kwargs["queryset"] = ChoiceDistribution.objects.filter(field=
class PopulationAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'size')
    fieldsets = (
            (None, {
                'fields':('name', 'model', 'size',)
            }),
        )
    inlines = [FieldSpecInline]

    def get_model_fields(self, obj):
        print obj
        return ""
class PopulationMemberInline(admin.TabularInline):
    model = PopulationMember
    fields = ('population', 'content_object')

class SampleAdmin(admin.ModelAdmin):
    list_display = ('population', 'size', 'member_count')
    #inlines = [PopulationMemberInline]

    def member_count(self, obj):
        return str(len(obj.member.all()))

admin.site.register(Name, NameAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(PopulationMember)
admin.site.register(Sample, SampleAdmin)
admin.site.register(ChoiceDistribution, ChoiceDistributionAdmin)
admin.site.register(FieldSpec, FieldSpecAdmin)
