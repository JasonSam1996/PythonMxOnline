from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict


# Create your views here.

class OrgListView(View):
    def get(self, request):
        """展示课程列表，筛选，"""
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 城市列表
        all_city = CityDict.objects.all()

        hot_org = all_orgs.order_by('-chick_nums')[:3]

        # 取出筛选所在城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 取出筛选机构类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 筛选出一共有多少家机构
        org_nums = all_orgs.count()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_city,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_org':hot_org,
        })
