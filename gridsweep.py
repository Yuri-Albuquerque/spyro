import sys
sys.path.append('/home/alexandre/Development/Spyro-main/spyro')
from datetime import datetime
import spyro

## Selecting sweep parameters
# Reference solution values
G_reference = 15
p_reference = 5

# Degrees and Gs for sweep
Gs = [x for x in range(3,13) ]
degrees = [1,2,3,4,5]

# Experiment parameters
experiment_type = 'homogeneous'
method = 'CG'
minimum_mesh_velocity = 1.0
frequency = 5.0

## Generating comm
model = spyro.tools.create_model_for_grid_point_calculation(frequency,1,method,minimum_mesh_velocity,experiment_type=experiment_type)
comm = spyro.utils.mpi_init(model)

## Output file for saving data
date = datetime.today().strftime('%Y_%m_%d')
text_file = open("output_sigmaCG500FullSweepWithItselfReference"+date+".txt", "w")
text_file.write('Homogenous and KMV \n')


## Starting sweep
for degree in degrees:
    if degree == 1:
        G_reference = 17.0
    else:
        G_reference = 15.0
    model = spyro.tools.create_model_for_grid_point_calculation(frequency, degree, method, minimum_mesh_velocity, experiment_type = experiment_type, receiver_type = 'near')
    print('Calculating reference solution of G = '+str(G_reference)+' and p = '+str(degree), flush = True)
    p_exact = spyro.tools.wave_solver(model, G =G_reference, comm = comm)
    comm.comm.barrier()

    print('\nFor p of '+str(degree), flush = True)
    text_file.write('For p of '+str(degree)+'\n')
    print('Starting sweep:', flush = True)
    text_file.write('\tG\t\tError \n')
    for G in Gs:
        model = spyro.tools.create_model_for_grid_point_calculation(frequency, degree, method, minimum_mesh_velocity, experiment_type = experiment_type, receiver_type = 'near')
        print('G of '+str(G), flush = True)
        p_0 = spyro.tools.wave_solver(model, G =G, comm = comm)
        error = spyro.tools.error_calc(p_exact, p_0, model, comm = comm)
        print('With P of '+ str(degree) +' and G of '+str(G)+' Error = '+str(error), flush = True)
        text_file.write('\t'+ str(G) +'\t\t'+str(error)+' \n')
        #spyro.plots.plot_receiver_difference(model, p_exact, p_0, 1, appear=True)

text_file.close()

