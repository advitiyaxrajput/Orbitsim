# Orbital Simulator
This is a python project which i built in order to understand how different numerical methods could be used to simulate orbits while checking how accurate they are. 

## Numerical Methods
This simualator currently make use of four methods:
- Euler
- Symplectics
- Velocity Verlet
- Runge-Kutta 4 (RK4)
These methods calculate the object's position and velocity at each step.
I will be comparing how the results differ, particularly in terms of their energy conversion and orbital stability.

## How to Run:
To run the simulator, open the terminal in the folder and enter - 
```bash
python -m orbitsim run configs/circular.toml
```
To compare the results for different step sizes, run
``` bash
python -m orbitsim sweep configs/circular.toml
```
The results and plots are saved within the `runs/` folder

## Results

### Orbital Trajectory

![Orbital Trajectory](docs/orbit.png)
This plot shows the path followed by the orbiting object during the simulation

### Step-Size Comparison

![Orbital Trajectory](docs/drift.png)
This plot shows the comparison between the changes in numerical drift when the a different step size is used. 

### Comparison of Numerical Methods
![Energy Drift Across Four Methods](docs/drift_four_methods.png)
This is the plot which shows how the enrgy of an orbit changes over time using the four numerical methods. It also allows us to compare how efficiently each of the methods coserve energy, where Euler presents a continuous increase in the energy error, while the symplectic methods like Symplectic Euler and Verlet have oscillating errors. RK4 has a very small energy error as well.

### Numerical Convergence
![Numerical Convergence](docs/convergence_four_methods.png)
This is the plot which presents how the error chagnes when the step size is redued for each method. It allows us to understand how rapidly each numerical method becomes more accurate as the corresponding step size decreases. 

### Elliptical Orbits
![Elliptical Orbits](docs/elliptical_orbit.png)
This is the plot which presents the elliptical orbit using Velocity Verlet. It identifies the periapsis and apoapsis along with the eccentricity and the semi major axis of the orbit. 

## Acceptance Tests
Made use of pytest in order to check wether or not the simulator is behaving as expected. The tests cover the accuracy of the conservation of energy, orbit, and the angular momentum, including the differences between the four numerical methods

The criteriaare as follows:
- **AC-1** Velocity Verlet keeps the relative radius error below \(10^{-3}\) over 10 orbits
- **AC-2** RK4 keeps relative energy and angular momentum drift below \(10^{-6}\) over 10 obrits
- **AC-3** Symplectic Euler and Velocity verlet kep the relative angular momentum drift below \(10^{-12}\) after 10 orbits
- **AC-4** The maximum energy error for the symplectic methods over 100 orbits stay below twice the maximum error over 10 orbits
- **AC-5** Euler's energy icnrases at every step, and its final orbital radius exceeds its initial radius.
- **AC-6** The four numerical methods are tested for convergence using an elliptical orbit. Euler and Symplectic Euler should have a convergence ratio close to 2, Verlet close to 4, and RK4 close to 16 when the step size is halved.
- **AC-7** The simulator measures the orbital period by detecting successive upward crossings of the positive x-axis. The measured period should be within 0.1% of the theoretical orbital period.
- **AC-8** The simulator identifies whether an orbit is bound or unbound based on its specific orbital energy. Velocities below escape velocity should be classified as bound, while velocities at or above escape velocity should be classified as unbound.

### Measured Results
The following are the results obtained when running the acceptance tests:
- **AC-1:** Maximum relative radius error = `1.97390139933e-05`
- **AC-2:** Maximum relative energy drift = `1.70916614195e-11`, angular momentum drift = `8.54583070975e-12`
- **AC-3:** Symplectic Euler angular momentum drift = `2.10942374679e-15`, Verlet angular momentum drift = `8.881784197e-16`
- **AC-4:** Energy error ratio over 100 orbits compared to 10 orbits = `1.00000000057` for Symplectic Euler and `1.0` for Verlet.
- **AC-5:** Euler's minimum energy increase per step = `7.730198766264795e-06`. Total energy increase = `0.1664044611563935`, and final radius = `1.492719969432555`.
- **AC-7:** Measured orbital period = `6.283267989142053`, compared to the theoretical period of `6.283185307179586`. Relative error = `1.3159243031138905e-05` (approximately `0.00132%`).

To run the acceptance tests:
```bash
pytest tests/test_acceptance.py -v
```
To run all tests:
```bash
pytest -v
```

## Limitations
The simulator currently models motion in two dimensions around a fixed central body making use of Newtonian Gravity
It uses a fixed timestep and doesn't simulate multiple intereacting bodies, a moving central body, atmospheric drag, thrust or relativistic effects. It also doesn't include 3D visualisations or adaptive timesteps. 