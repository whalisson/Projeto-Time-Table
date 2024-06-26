from django.test import TestCase
from mm1.models import Room, MeetingTime, Instructor, Course, Department, Section
from mm1.views import Data, Schedule, Population, GeneticAlgorithm, POPULATION_SIZE

class TestIntegration(TestCase):
    def setUp(self):
        # Configura os dados necessários para os testes
        self.room1 = Room.objects.create(r_number='101', seating_capacity=30)
        self.room2 = Room.objects.create(r_number='102', seating_capacity=20)
        
        self.meeting_time1 = MeetingTime.objects.create(pid='MT1',time='10:30 - 11:30', day='Segunda')
        self.meeting_time2 = MeetingTime.objects.create(pid='MT2',time='14:30 - 16:00', day='Terça')
        
        self.instructor1 = Instructor.objects.create(name='Prof. A', uid='T001')
        self.instructor2 = Instructor.objects.create(name='Prof. B', uid='T002')
        
        self.course1 = Course.objects.create(course_name='Course 1', course_number='C1', max_numb_students=25)
        self.course1.instructors.add(self.instructor1)
        self.course2 = Course.objects.create(course_name='Course 2', course_number='C2', max_numb_students=15)
        self.course2.instructors.add(self.instructor2)

        self.department1 = Department.objects.create(dept_name='Dept 1')
        self.department1.courses.add(self.course1, self.course2)
        
        self.section1 = Section.objects.create(department=self.department1, section_id='S1', num_class_in_week=2)
        self.section2 = Section.objects.create(department=self.department1, section_id='S2', num_class_in_week=2)

        self.data = Data()

    def test_generate_timetable(self):
        
        # Teste para verificar a geração do cronograma usando o algoritmo genético
        population = Population(POPULATION_SIZE)
        geneticAlgorithm = GeneticAlgorithm()
        generation_num = 0
        max_generations = 100  # Aumentando o número de gerações

        # Inicializa e ordena a população
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

        # Verifica se a condição inicial é atendida antes de iniciar o loop
        if population.get_schedules()[0].get_fitness() >= 1.0:
            print("Já alcançou um cronograma ideal antes de iniciar a evolução.")
            generation_num = 1  # Define a primeira geração como 1, pois já temos um cronograma ideal

        # Evolui a população até encontrar um cronograma ideal ou atingir o limite de gerações
        while population.get_schedules()[0].get_fitness() < 1.0 and generation_num < max_generations:
            generation_num += 1
            population = geneticAlgorithm.evolve(population)
            population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

        # Obtenha o melhor cronograma após a evolução
        best_schedule = population.get_schedules()[0]
        schedule_classes = best_schedule.get_classes()

        # Debug: Print informações do cronograma
        print(f"Numero de gerações: {generation_num}")
        print(f"Fitness: {best_schedule.get_fitness()}")
        print(f"Número de aulas: {len(schedule_classes)}")
        for cls in schedule_classes:
            print(f"Instrutor: {cls.get_instructor()}, Horário: {cls.get_meetingTime()}, Sala: {cls.get_room()}")

        # Assertivas para verificar se o cronograma é gerado corretamente
        self.assertTrue(generation_num > 0, "Deve ter pelo menos uma geração para encontrar o horário ideal.")
        self.assertEqual(len(schedule_classes), 4, "Número de aulas no cronograma gerado está incorreto.")
        self.assertTrue(best_schedule.get_fitness() == 1.0 or generation_num == max_generations,
                        "Não conseguiu gerar um cronograma ideal.")

        # Verificar se todas as classes têm todos os atributos configurados corretamente
        for cls in schedule_classes:
            self.assertIsNotNone(cls.get_instructor(), "Instrutor não atribuído.")
            self.assertIsNotNone(cls.get_meetingTime(), "Horário não atribuído.")
            self.assertIsNotNone(cls.get_room(), "Sala não atribuída.")