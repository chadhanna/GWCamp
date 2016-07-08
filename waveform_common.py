import argparse
import lal
import lalsimulation as lalsim
import numpy

def parse():
	parser = argparse.ArgumentParser(description="This program uses an approximation to the dynamics of general relativity to predict the gravitational wave strain signal from a merging black hole binary.")
	parser.add_argument("--mass1", action="store", type=float, default=10.0, help="Mass 1 (Solar Masses): default 10.0")
	parser.add_argument("--mass2", action="store", type=float, default=10.0, help="Mass 2 (Solar Masses): default 10.0")
	parser.add_argument("--spin1", action="store", type=float, default=0, help="Spin 1 (dimensionless): default 0")
	parser.add_argument("--spin2", action="store", type=float, default=0, help="Spin 2 (dimensionless): default 0")
	parser.add_argument("--distance", action="store", type=float, default=300, help="Distance (Mpc): default 300")
	parser.add_argument("--secret", action="store", type=int, default=0, help="Make a secret waveform by setting a positive integer, e.g., 1,2,3...")
	args = parser.parse_args()
	for arg in ("mass1", "mass2"):
		if getattr(args,arg) < 5. or getattr(args,arg) > 30.:
			raise ValueError("Please choose masses between 10 and 30 Solar Masses")
	for arg in ("spin1", "spin2"):
		if getattr(args,arg) < -0.95 or getattr(args,arg) > 0.95:
			raise ValueError("Please choose spins between -0.95 and 0.95")
	if args.distance > 1000 or args.distance < 300:
		raise ValueError("Please choose a distance between 300 and 1000 Mpc")

	dt = 1. / 4096.

	m1 = args.mass1
	m2 = args.mass2
	s1 = args.spin1
	s2 = args.spin2
	dist = args.distance

	hplus, hcross = lalsim.SimInspiralChooseTDWaveform(0, dt, m1*lal.MSUN_SI, m2*lal.MSUN_SI, 0, 0, s1, 0, 0, s2, 40., 0, dist*1.e6 * lal.PC_SI, 0, 0, 0, None, None, 0, 8, lalsim.GetApproximantFromString(str("IMRPhenomD")))

	rate = 4096
	dt = 1. / rate

	# 2 seconds
	t = numpy.arange(2 * rate) * dt
	data = numpy.zeros(8192)
	if len(hplus.data.data) > 8192:
		data[:] = hplus.data.data[-8192:]
	else:
		data[-len(hplus.data.data):] = hplus.data.data

	return m1,m2,s1,s2,dist,args.secret,data,t,rate,dt
