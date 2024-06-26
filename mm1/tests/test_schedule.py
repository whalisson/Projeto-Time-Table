import unittest
from django.test import TestCase
from mm1.models import Room, MeetingTime, Instructor, Course, Department, Section
from mm1.views import Data, Schedule, Population, GeneticAlgorithm, Class, POPULATION_SIZE, TOURNAMENT_SELECTION_SIZE
from django.utils import timezone

class TestSchedule(TestCase):
    def setUp(self):
        # Configura os dados necessários
        self.room = Room.objects.create(r_number='101', seating_capacity=30)
        self.meeting_time = MeetingTime.objects.create(day='Monday', time='09:00-11:00')
        self.instructor = Instructor.objects.create(name='Prof. Test', uid='T001')
        self.course = Course.objects.create(course_name='Course 1', course_number='C1', max_numb_students=20)
        self.course.instructors.add(self.instructor)
        self.department = Department.objects.create(dept_name='Dept 1')
        self.department.courses.add(self.course)
        self.section = Section.objects.create(department=self.department, section_id='S1', num_class_in_week=3)
        self.data = Data()

    def test_initialize_schedule(self):
        schedule = Schedule().initialize()
        self.assertEqual(len(schedule.get_classes()), 3, "Número de classes inicializado incorretamente.")

    def test_calculate_fitness_no_conflicts(self):
        schedule = Schedule().initialize()
        fitness = schedule.calculate_fitness()
        self.assertEqual(fitness, 1.0, "Fitness deve ser 1.0 quando não há conflitos.")

    def test_calculate_fitness_no_conflicts(self):
        schedule = Schedule()
        test_class = Class(
            id=1,
            dept=self.department,
            section=self.section,
            course=self.course
        )
        test_class.set_meetingTime(self.meeting_time)
        test_class.set_room(self.room)
        test_class.set_instructor(self.instructor)

        schedule._classes = [test_class]
        fitness = schedule.calculate_fitness()

        self.assertEqual(fitness, 1.0, f"Fitness deve ser 1.0 quando não há conflitos, mas foi {fitness}.")

    def test_crossover_population(self):
        ga = GeneticAlgorithm()
        pop = Population(POPULATION_SIZE)
        new_pop = ga._crossover_population(pop)
        self.assertEqual(len(new_pop.get_schedules()), POPULATION_SIZE, "Crossover não gerou a população correta.")

    def test_mutate_population(self):
        ga = GeneticAlgorithm()
        pop = Population(POPULATION_SIZE)
        new_pop = ga._mutate_population(pop)
        self.assertEqual(len(new_pop.get_schedules()), POPULATION_SIZE, "Mutação não gerou a população correta.")

    def test_select_tournament_population(self):
        ga = GeneticAlgorithm()
        pop = Population(POPULATION_SIZE)
        tournament_pop = ga._select_tournament_population(pop)
        self.assertEqual(len(tournament_pop.get_schedules()), TOURNAMENT_SELECTION_SIZE,
                         "Seleção por torneio não gerou o tamanho correto da população.")

if __name__ == '__main__':
    unittest.main()
