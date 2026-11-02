from django.urls import path
from . import views
urlpatterns=[
 path('',views.projects,name='agile_projects'),path('new/',views.new_project,name='agile_new_project'),
 path('<int:pk>/',views.board,name='agile_board'),path('<int:pk>/sprints/new/',views.new_sprint,name='agile_new_sprint'),
 path('<int:pk>/sprints/<int:sid>/edit/',views.edit_sprint,name='agile_edit_sprint'),
 path('<int:pk>/items/new/',views.new_item,name='agile_new_item'),
 path('<int:pk>/items/<int:iid>/move/',views.move_item,name='agile_move_item'),
 path('<int:pk>/report/',views.report,name='agile_report'),path('<int:pk>/report.csv',views.report_csv,name='agile_report_csv'),
]
