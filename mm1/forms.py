from django.forms import ModelForm
from. models import *
from django import forms


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = [
            'r_number',
            'seating_capacity'
        ]
        labels = {
            'r_number': 'No. Sala',
            'seating_capacity':'Capacidade'
        }


class InstructorForm(ModelForm):

    available_times = forms.ModelMultipleChoiceField(
        queryset=MeetingTime.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Campo opcional
        label='Horários Disponíveis'  # Rótulo personalizado
    )
    class Meta:
        model = Instructor
        fields = [
            'uid',
            'name',
            'available_times',
        ]
        
        labels = {
            'uid': 'ProfessorID',
            'name':'Nome do Professor',
            'available_times':'Horario disponivel',
        }

class MeetingTimeForm(ModelForm):
    class Meta:
        model = MeetingTime
        fields = [
            'pid',
            'time',
            'day'
        ]
        widgets = {
            'pid': forms.TextInput(),
            'time': forms.Select(),
            'day': forms.Select(),
        }

        labels = {
            'pid': 'Id da Reunião',
            'time':'Horário',
            'day':'Dia da Semana'
        }

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'course_name', 'max_numb_students', 'instructors']

        labels = {
            'course_number': 'No. Matéria',
            'course_name':'Nome Matéria',
            'max_numb_students':'Numero de Alunos',
            'instructors':'Professor',
        }

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'courses']

        labels = {
            'dept_name': 'Nome do Curso e Periodo',
            'courses':'Matérias',
        }


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_id', 'department', 'num_class_in_week']
        labels = {
            'section_id': 'ID Turma',
            'department':'Curso & Turma',
            'num_class_in_week':'No. Aulas Semanais'
        }