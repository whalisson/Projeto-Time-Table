from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import random as rnd
from. forms import *

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05


class Data:
    def __init__(self):
        self._rooms = Room.objects.all()
        self._meetingTimes = MeetingTime.objects.all()
        self._instructors = Instructor.objects.all()
        self._courses = Course.objects.all()
        self._depts = Department.objects.all()

    def get_rooms(self): return self._rooms

    def get_instructors(self): return self._instructors

    def get_courses(self): return self._courses

    def get_depts(self): return self._depts

    def get_meetingTimes(self): return self._meetingTimes


class Schedule:
    def __init__(self):
        self._data = data  # Instância de Data para acessar dados
        self._classes = []  # Lista de classes no cronograma
        self._numberOfConflicts = 0  # Contador de conflitos
        self._fitness = -1  # Valor de fitness
        self._classNumb = 0  # Contador de classes
        self._isFitnessChanged = True  # Flag para indicar se o valor de fitness mudou

    # Métodos de acesso
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()  # Calcula a fitness se ela mudou
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        sections = Section.objects.all()
        for section in sections:
            dept = section.department
            n = section.num_class_in_week
            courses = dept.courses.all()
            for course in courses:
                for i in range(n // len(courses)):
                    crs_inst = course.instructors.all()
                    newClass = Class(self._classNumb, dept, section.section_id, course)
                    self._classNumb += 1
                    meeting_time = data.get_meetingTimes()[rnd.randrange(0, len(MeetingTime.objects.all()))]
                    
                    # Verifica disponibilidade opcional do instrutor
                    available_instructors = [inst for inst in crs_inst if not inst.available_times.exists() or meeting_time in inst.available_times.all()]
                    if not available_instructors:
                        available_instructors = crs_inst  # Se nenhum instrutor disponível, use todos os instrutores

                    newClass.set_meetingTime(meeting_time)
                    newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                    newClass.set_instructor(available_instructors[rnd.randrange(0, len(available_instructors))])
                    self._classes.append(newClass)
        return self


    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            if classes[i].instructor.available_times.exists() and classes[i].meeting_time not in classes[i].instructor.available_times.all():
                self._numberOfConflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                            (classes[i].section_id != classes[j].section_id) and (classes[i].section == classes[j].section):
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].instructor == classes[j].instructor:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)


# Classe para representar uma população de cronogramas
class Population:
    def __init__(self, size):
        self._size = size  # Tamanho da população
        self._data = data  # Dados da instância Data
        self._schedules = [Schedule().initialize() for i in range(size)]  # Inicializa a população

    def get_schedules(self):
        return self._schedules

# Implementação do algoritmo genético
class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))  # Realiza cruzamento e mutação

    def _crossover_population(self, pop):
        crossover_pop = Population(0)  # População de cruzamento vazia
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])  # Mantém os cronogramas elite
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]  # Seleção por torneio
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))  # Cruza cronogramas
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])  # Aplica mutação nos cronogramas
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()  # Inicializa um novo cronograma para cruzamento
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]  # Escolhe classe do primeiro cronograma
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]  # Escolhe classe do segundo cronograma
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()  # Inicializa novo cronograma para mutação
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]  # Substitui classes aleatoriamente
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)  # População de torneio vazia
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])  # Seleção aleatória
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)  # Ordena pela fitness
        return tournament_pop

# Classe que representa uma aula
class Class:
    def __init__(self, id, dept, section, course):
        self.section_id = id  # ID da seção
        self.department = dept  # Departamento
        self.course = course  # Curso
        self.instructor = None  # Instrutor (a definir)
        self.meeting_time = None  # Horário (a definir)
        self.room = None  # Sala (a definir)
        self.section = section  # Seção

    # Métodos de acesso e configuração
    def get_id(self): return self.section_id
    def get_dept(self): return self.department
    def get_course(self): return self.course
    def get_instructor(self): return self.instructor
    def get_meetingTime(self): return self.meeting_time
    def get_room(self): return self.room
    def set_instructor(self, instructor): self.instructor = instructor
    def set_meetingTime(self, meetingTime): self.meeting_time = meetingTime
    def set_room(self, room): self.room = room

# Instância global de dados
data = Data()

# Função para gerar o contexto do cronograma para renderizar
def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    cls = {}
    for i in range(len(classes)):
        cls["section"] = classes[i].section_id
        cls['dept'] = classes[i].department.dept_name
        cls['course'] = f'{classes[i].course.course_name} ({classes[i].course.course_number}, ' \
                        f'{classes[i].course.max_numb_students}'
        cls['room'] = f'{classes[i].room.r_number} ({classes[i].room.seating_capacity})'
        cls['instructor'] = f'{classes[i].instructor.name} ({classes[i].instructor.uid})'
        cls['meeting_time'] = [classes[i].meeting_time.pid, classes[i].meeting_time.day, classes[i].meeting_time.time]
        context.append(cls)
    return context

# Função para renderizar a página inicial
def home(request):
    return render(request, 'index.html', {})

# Função para gerar e renderizar o horário
def timetable(request):
    schedule = []
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Geração #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()

    return render(request, 'timetable.html', {'schedule': schedule, 'sections': Section.objects.all(),
                                              'times': MeetingTime.objects.all()})

# Função para adicionar instrutor
def add_instructor(request):
    form = InstructorForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addinstructor')
    context = {
        'form': form
    }
    return render(request, 'adins.html', context)

# Função para listar instrutores
def inst_list_view(request):
    context = {
        'instructors': Instructor.objects.all()
    }
    return render(request, 'instlist.html', context)

# Função para deletar instrutor
def delete_instructor(request, pk):
    inst = Instructor.objects.filter(pk=pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('editinstructor')

# Função para adicionar sala
def add_room(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addroom')
    context = {
        'form': form
    }
    return render(request, 'addrm.html', context)

# Função para listar salas
def room_list(request):
    context = {
        'rooms': Room.objects.all()
    }
    return render(request, 'rmlist.html', context)

# Função para deletar sala
def delete_room(request, pk):
    rm = Room.objects.filter(pk=pk)
    if request.method == 'POST':
        rm.delete()
        return redirect('editrooms')

# Função para listar horários
def meeting_list_view(request):
    context = {
        'meeting_times': MeetingTime.objects.all()
    }
    return render(request, 'mtlist.html', context)

# Função para adicionar horário
def add_meeting_time(request):
    form = MeetingTimeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addmeetingtime')
        else:
            print('Invalid')
    context = {
        'form': form
    }
    return render(request, 'addmt.html', context)

# Função para deletar horário
def delete_meeting_time(request, pk):
    mt = MeetingTime.objects.filter(pk=pk)
    if request.method == 'POST':
        mt.delete()
        return redirect('editmeetingtime')

# Função para listar cursos
def course_list_view(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'crslist.html', context)

# Função para adicionar curso
def add_course(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addcourse')
        else:
            print('Invalid')
    context = {
        'form': form
    }
    return render(request, 'adcrs.html', context)

# Função para deletar curso
def delete_course(request, pk):
    crs = Course.objects.filter(pk=pk)
    if request.method == 'POST':
        crs.delete()
        return redirect('editcourse')

# Função para adicionar departamento
def add_department(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('adddepartment')
    context = {
        'form': form
    }
    return render(request, 'addep.html', context)

# Função para listar departamentos
def department_list(request):
    context = {
        'departments': Department.objects.all()
    }
    return render(request, 'deptlist.html', context)

# Função para deletar departamento
def delete_department(request, pk):
    dept = Department.objects.filter(pk=pk)
    if request.method == 'POST':
        dept.delete()
        return redirect('editdepartment')

# Função para adicionar seção
def add_section(request):
    form = SectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addsection')
    context = {
        'form': form
    }
    return render(request, 'addsec.html', context)

# Função para listar seções
def section_list(request):
    context = {
        'sections': Section.objects.all()
    }
    return render(request, 'seclist.html', context)

# Função para deletar seção
def delete_section(request, pk):
    sec = Section.objects.filter(pk=pk)
    if request.method == 'POST':
        sec.delete()
        return redirect('editsection')