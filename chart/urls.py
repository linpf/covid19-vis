from django.urls import path
from . import views

urlpatterns = [
   path("", views.home_view, name="home"),
   path("canada/", views.canada_view, name="canada"),
   path("provinces/", views.provinces_view, name="provinces"),
   path("provs_simple/", views.provs_simple_view, name="provs_simple"),
   path("canada_hrs/", views.canada_hrs_view, name="canada_hrs"),
   path("bc_cases_by_age_group/", views.bc_cases_by_age_group_view, name="bc_cases_by_age_group"),
   path("bc_lab_tests/", views.bc_lab_tests_view, name="bc_lab_tests"),
   path("province_hrs/<str:province>/", views.province_hrs_view, name="province_hrs"),
   path("province_mortality_hrs/<str:province>/", views.province_mortality_hrs_view, name="province_mortality_hrs"),
   path("province_hrs_cumulative/<str:province>/", views.province_hrs_cumulative_view, name="province_hrs_cumulative"),
   path("provinces_testing/", views.provinces_testing_view, name="provinces_testing"),
   path("provinces_mortality/", views.provinces_mortality_view, name="provinces_mortality"),
   path("provinces_cases/", views.provinces_cases_view, name="provinces_cases"),
   path("provinces_recovered/", views.provinces_recovered_view, name="provinces_recovered"),
   path("province/<str:province>/", views.province_view, name="province"),
   path("province_cases/<str:province>/", views.province_cases_view, name="province_cases"),
   path("province_cumulative/<str:province>/", views.province_cumulative_view, name="province_cumulative"),
   path("health_region/<str:province>/<str:health_region>/", views.health_region_view, name="health_region"),
   path("health_region_mortality/<str:province>/<str:health_region>/", views.health_region_mortality_view, name="health_region_mortality"),
   path("health_region_cases/<str:province>/<str:health_region>/", views.health_region_cases_view, name="health_region_cases"),
]
