__author__ = 'lexi'
import numpy
import Timer

class KalmanFilter():
	def __init__(self):
		'''
		NOTE: Ex and Ez are given in advance and never change.
		self.Ex = numpy.array([
							  [0.1, 0.0, 0.0,   0.0,   0.0, 0.0],
										  [0.0, 0.1, 0.0,   0.0,   0.0, 0.0],
										  [0.0, 0.0, 100.0, 0.0,   0.0, 0.0],
										  [0.0, 0.0, 0.0,   0.1,   0.0, 0.0],
										  [0.0, 0.0, 0.0,   0.0,   0.1, 0.0],
										  [0.0, 0.0, 0.0,   0.0,   0.0, 100.0]])
		self.Ez = numpy.array([
							  [25, 0],
										  [0, 25]])
		:param Ex: Transition noise variance. Transition noise ~ N(0, Ex). A.K.A. Rk in the packet.
		:param Ez: Observation noise variance. Observation noise ~ N(0, Ez). A.K.A. Qk in the packet.
		:return:
		'''
		self.Ex = numpy.array([
							  [0.1, 0.0, 0.0,   0.0,   0.0, 0.0],
							  [0.0, 0.1, 0.0,   0.0,   0.0, 0.0],
							  [0.0, 0.0, 100.0, 0.0,   0.0, 0.0],
							  [0.0, 0.0, 0.0,   0.1,   0.0, 0.0],
							  [0.0, 0.0, 0.0,   0.0,   0.1, 0.0],
							  [0.0, 0.0, 0.0,   0.0,   0.0, 100.0]])
		self.Ez = numpy.array([
							  [25, 0],
							  [0, 25]])

		#-----------------------------------------------------------------------------
		# VARIABLES THAT DO NOT CHANGE
		#-----------------------------------------------------------------------------

		# ------------------ F ---------------
		# Learning Suite: F
		# Description: a physics matrix
		dt = Timer.Timer.TIME_PER_TICK
                c = 0
                self.F = numpy.array([
	                [1, dt, dt**2/2, 0, 0, 0],
                        [0, 1,  dt,      0, 0, 0],
                        [0, -c, 1,       0, 0, 0],
                        [0, 0,  0,       1, dt, dt**2/2],
                        [0, 0,  0,       0, 1, dt],
                        [0, 0,  0,       0, -c, 1]])


		# ------------------ F^T ---------------
		# Learning Suite: F^T
		# Description: Transpose of F
		self.FT = self.F.transpose()

		# ------------------ H ---------------
		# Learning Suite: H
		# Description: converts from state to sensor reading
		self.H = numpy.array([
			[1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0]])

		# ------------------ H^T ---------------
		# Learning Suite: H^T
		# Description: Transpose of H
		self.HT = self.H.transpose()


		# ------------------ E0 ---------------
		# Learning Suite: E_0
		# Description: Our initial guess of Et
		self.E0 = numpy.array([
			  [100.0, 0.0, 0.0, 0.0,   0.0, 0.0],
                          [0.0,   0.1, 0.0, 0.0,   0.0, 0.0],
                          [0.0,   0.0, 0.1, 0.0,   0.0, 0.0],
                          [0.0,   0.0, 0.0, 100.0, 0.0, 0.0],
                          [0.0,   0.0, 0.0, 0.0,   0.1, 0.0],
                          [0.0,   0.0, 0.0, 0.0,   0.0, 0.1]])

		# ------------------ u0 ---------------
		# Learning Suite: u_0
		# Description: Our initial guess of ut
		self.u0 = numpy.array([
			[0],
		        [0],
		        [0],
		        [0],
		        [0],
		        [0]
		])

		# ------------------ I ---------------
		# Learning Suite: I
		# Description: Identity Matrix
		self.I = numpy.array([
			  [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])



		#-----------------------------------------------------------------------------
		# VARIABLES THAT CHANGE/ARE UPDATED
		#-----------------------------------------------------------------------------

		# ------------------ Et ---------------
		# Learning Suite: E_t
		# Description: Previous estimated covariance
		self.Et = numpy.copy(self.E0)

		# ------------------ ut ---------------
		# Learning Suite: u_t
		# Description: Previous estimated mean
		self.ut = numpy.copy(self.u0)



	def update(self, zt):
		'''
		Do Bayesian Kalman-Filter update.
		:param zt: The observation from the server. This is a "2 x 1"-dimension matrix
			   containing the (x,y) position coordinates of the tank.
		:return: A tuple containing the estimated mean ("self.ut") and the ellipse width
		("a"), and the ellipse height ("b").
		'''

		# -------------------- Update Kt --------------------
		#(F)(Et)(FT) + Ex
		F_Et_FT_plus_Ex = numpy.add(self.F.dot(self.Et).dot(self.FT), self.Ex)

		#(H * ((F)(Et)(FT) + Ex) * HT) + Ez
		hugeTerm = numpy.add(self.H.dot(F_Et_FT_plus_Ex).dot(self.HT), self.Ez)

		#Kalman gain
		#(Inverse code from http://stackoverflow.com/questions/21638895/inverse-of-a-matrix-using-numpy)
		Kt = F_Et_FT_plus_Ex.dot(self.HT).dot(numpy.linalg.inv(hugeTerm))

		# -------------------- Update ut --------------------
		Fut = self.F.dot(self.ut)
		HFut = self.H.dot(Fut)
		zt_minus_HFut = numpy.subtract(zt, HFut)
		self.ut = numpy.add(Fut, Kt.dot(zt_minus_HFut))

		# -------------------- Update Et --------------------
		KtH = Kt.dot(self.H)
		I_minus_KtH = numpy.subtract(self.I, KtH)
		self.Et = I_minus_KtH.dot(F_Et_FT_plus_Ex)

		# -------- Return relevant variables for visualizing ---------
		# The ellipse width
		a = self.Et[0][0]

		# The ellipse height
		b = self.Et[3][3]

		return (self.ut, a, b)

if __name__ == "__main__":
	#Ex and Ez may be adjusted to attempt to get better performance. These are the
	#default values given in Learning Suite.
	# Ex =
	# Ez =

	k = KalmanFilter(Ex=Ex,Ez=Ez)


	print k.observationNoise()
	print k.transitionNoise()