import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'chick_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'chick_nums', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'chick_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['name', 'work_year', 'work_company', 'work_position', 'points', 'chick_nums', 'fav_nums',
                    'org', 'add_time']
    search_fields = ['name', 'work_year', 'work_company', 'work_position', 'points', 'chick_nums', 'fav_nums', 'org']
    list_filter = ['name', 'work_year', 'work_company', 'work_position', 'points', 'chick_nums', 'fav_nums',
                   'org', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
