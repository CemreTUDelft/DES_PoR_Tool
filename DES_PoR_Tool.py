import random
import numpy as np
import simpy

#input settings
NUM_DOCTORS=2
TREATMENTTIME=5
T_INTER=7
SingleBedRoom_Num=20
OutpatientDept_Num=16
MultipleBedRoom_BedNum=40
SingleBed_DeliveryRoom_Num=12
MultipleBed_DeliveryRoom_BedNum=10
ICU_BedNum=10
Administrative_Num=20
TotalBeds_Num=SingleBedRoom_Num+MultipleBedRoom_BedNum+SingleBed_DeliveryRoom_Num+MultipleBed_DeliveryRoom_BedNum+ICU_BedNum

#Area calculation of treatment rooms & waiting areas in each outpatient department
if NUM_DOCTORS == 1:
    Outpatient_Dept_Area = (16 * NUM_DOCTORS) + 12 #treatment rooms + waiting areas
elif NUM_DOCTORS == 2:
    Outpatient_Dept_Area = (16 * NUM_DOCTORS) + 24 #treatment rooms + waiting areas
elif NUM_DOCTORS > 2:
    Outpatient_Dept_Area = (16 * NUM_DOCTORS) + 24 + (5 * (NUM_DOCTORS - 2)) #treatment rooms + waiting areas


RANDOM_SEED = 42 #seed number of simulation
SIM_TIME = 480 #simulation time in minutes: 8 hours
data_wait = []
data_patientdisposed = []

#create outpatient components
class Outpatient(object):

    def __init__(self, env, num_doctors, treatmenttime):
        self.env = env
        self.doctor = simpy.Resource(env, num_doctors)
        self.treatmenttime = treatmenttime

    def treat(self, patient):
        yield self.env.timeout(random.expovariate(1/TREATMENTTIME)) #exponential treatment time

#create patient arrivals
def patient(env, name, pr):
    print('%s arrives at the outpatient department at %.2f.' % (name, env.now))
    arrivetime=env.now
    with pr.doctor.request() as request:
        yield request 
        print('%s enters the outpatient department at %.2f.' % (name, env.now))
        entertime=env.now
        yield env.process(pr.treat(name))
        print('%s leaves the outpatient department at %.2f.' % (name, env.now))
        print('%s waiting time %.2f.' % (name, entertime-arrivetime))
        data_wait.append(entertime-arrivetime)

#create treatment process
def setup(env, num_doctors, treatmenttime, t_inter):
    outpatient_department = Outpatient(env, num_doctors, treatmenttime)
    #create 4 initial patients
    for i in range(4):
        env.process(patient(env, 'patient %d' % i, outpatient_department))
    #create more patients
    while True:
        yield env.timeout(np.random.poisson(t_inter)) #simulate patient arrivals in a poisson process with a lambda value of 7
        i += 1
        env.process(patient(env, 'patient %d' % i, outpatient_department))
        data_patientdisposed.append(i)

#run the simulation 
random.seed(RANDOM_SEED)  
env = simpy.Environment()
env.process(setup(env, NUM_DOCTORS, TREATMENTTIME, T_INTER))
env.run(until=SIM_TIME)
#get the outputs of DES from a,b
a=data_patientdisposed #number of patients disposed (treated) from the system
b=data_wait #number of waiting times

#calculate space requirements of hospital units
c=Outpatient_Dept_Area*OutpatientDept_Num 
#total area of all outpatient dept.s
d=(SingleBedRoom_Num*9)+(MultipleBedRoom_BedNum*7) 
#One-bed patient rooms must be min 9 m2.Patient wards must be min 7 m2 per each bed.
e=(SingleBed_DeliveryRoom_Num*12)+(MultipleBed_DeliveryRoom_BedNum*10) #One-bed delivery patient rooms must be min 12 m2.Delivery patient wards must be min 10 m2 per each bed.
f=ICU_BedNum*12 #ICU units must be min 12 m2 per each bed.
g=Administrative_Num*random.randint(8,12) 
#Administrative offices must be 8-12 m2 for each personnel. 
h=TotalBeds_Num+(TotalBeds_Num*0.2) 
#Bunker area = (number of beds) + (number of beds*20%)
#There must be min 6 elevators in 60-200 bed hospitals. 
#There must be min 9 elevators in 201-350 bed hospitals. 
if TotalBeds_Num >= 60 and TotalBeds_Num <= 200:
    MIN_ELEV = 6
elif TotalBeds_Num > 200 and TotalBeds_Num <= 350:
    MIN_ELEV = 9
i=MIN_ELEV
#get the outputs of PoR from c,d,e,f,g,h,i
print()
print('Outpatient area should be minimum', c,'m2')
print('Inpatient area should be minimum', d,'m2')
print('Delivery area should be minimum', e,'m2')
print('Intensive Care Units should be minimum', f,'m2')
print('Administrative offices should be minimum', g,'m2')
print('Bunker area should be minimum', h,'m2')
print('Elevator number should be minimum', i)
