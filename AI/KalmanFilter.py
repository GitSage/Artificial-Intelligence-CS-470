__author__ = 'lexi'
import numpy
import Timer

class KalmanFilter():
	def __init__(self, Ex, Ez):
		'''
		NOTE: Ex and Ez are given in advance and never change.

		:param Ex: Transition noise variance. Transition noise ~ N(0, Ex). A.K.A. Rk in the packet.
		:param Ez: Observation noise variance. Observation noise ~ N(0, Ez). A.K.A. Qk in the packet.
		:return:
		'''
		self.Ex = Ex
		self.Ez = Ez

		#-----------------------------------------------------------------------------
		# VARIABLES THAT DO NOT CHANGE
		#-----------------------------------------------------------------------------

		# ------------------ F ---------------
		# Learning Suite: F
		# Packet: A
		# Description: a physics matrix
		dt = Timer.TIME_PER_TICK
                c = 0
                self.F = numpy.array([
	                [1, dt, dt**2/2, 0, 0, 0],
                        [0, 1,  dt,      0, 0, 0],
                        [0, -c, 1,       0, 0, 0],
                        [0, 0,  0,       1, dt, dt**2/2],
                        [0, 0,  0,       0, 1, dt],
                        [0, 0,  0,       0, -c, 1]])


		# ------------------ F^T ---------------
		# Description: Transpose of F
		self.Ft = self.F.transpose()

		# ------------------ H ---------------
		# Learning Suite: H_k
		# Packet: H_k
		# Description: converts from state to sensor reading
		self.H = numpy.array([
			[1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0]])

		# ------------------ H^T ---------------
		# Description: Transpose of H
		self.Ht = self.H.transpose()


		#-----------------------------------------------------------------------------
		# VARIABLES THAT CHANGE/ARE UPDATED
		#-----------------------------------------------------------------------------

		# ------------------ xt ---------------
		# Learning Suite: Xt+1∼N(FXt,Σx)
		# Packet: the xk in "xk = Ak(xk-1) + Bk(uk) + wk"
		# Description: Predicted state value (Prior)

		# Starting off predicting that it is completely still.
		self.xt = [0,0,0,0,0,0]


		#-----------------------------------------------------------------------------
		# DELETE
		#-----------------------------------------------------------------------------

		#K_tplus1 = Ek H^T (H Ek H^T + Ez)^(-1)
		#(K_tplus1) (K_k) ("Kalman Gain": Higher if sensor is more certain. Lower if sensor is more uncertain (high variance).)
		self.kalmanGain = 0

		#(z_tplus1) (Z_k) (predicted observation)
		self.predictedObservation = 0

		#Sigma_t (E_{k-1}) (previous "variance posterior")
		self.Et = numpy.array([
			  [100.0, 0.0, 0.0, 0.0,   0.0, 0.0],
                          [0.0,   0.1, 0.0, 0.0,   0.0, 0.0],
                          [0.0,   0.0, 0.1, 0.0,   0.0, 0.0],
                          [0.0,   0.0, 0.0, 100.0, 0.0, 0.0],
                          [0.0,   0.0, 0.0, 0.0,   0.1, 0.0],
                          [0.0,   0.0, 0.0, 0.0,   0.0, 0.1]])

		#Mean and Variance of X_k (x_k is Gaussian a.k.a. Normal distribution)
		#ut = F u^_{k-1} + B uk
		#Ek = A E_{k-1} A^T + Ex

		#(Ek) (E_k) (variance prior (of the predicted state))
		self.variancePrior = 0

		#(ut) (u-_k) (mean of the predicted state)
		self.priorMean = 0




		#u_{t+1} (u^_t)
		self.posteriorMean = 0

		#Identity matrix
		self.I = 0



	def update(self, uk):
		'''
		Do Bayesian Kalman-Filter update. (Get new prior based on observation.)
		:param uk: The observation (from the sensor)
		:return: A sample point from the Posterior distribution (A Gaussian distribution
		with mean u^_k and variance E^_K).
		'''

		# ------------------ xt ---------------
		# Learning Suite: Xt+1∼N(FXt,Σx)
		# Packet: the xk in "xk = Ak(xk-1) + Bk(uk) + wk"
		# Description: Predicted state value (Prior)
		mean = self.F.dot(self.xt)
		covariance = self.Ex
		self.xt = numpy.random.multivariate_normal(mean, covariance)

		# ------------------ zt ---------------
		# Learning Suite: Zt∼N(HXt,ΣZ)
		# Packet: the zk in "zk = Hk * xk + vk"
		self.zt = numpy.random.multivariate_normal(self.H.dot(self.xt), self.Ez)

		#Kalman gain
		self.kalmanGain = self.variancePrior * self.Ht * ((self.H * self.variancePrior * self.Ht) + self.Ez)

		#mean posterior
		#posteriorMean = priorMean + kalmanGain(predictedObservation - H * priorMean)
		self.meanPosterior = self.priorMean + (self.kalmanGain * (self.predictedObservation - (self.H * self.priorMean)))

		#variance posterior
		#variancePrior = (I - KH)(variancePrior)
		self.variancePrior = (self.I - (self.kalmanGain * self.H)) * self.variancePrior

	def observationNoise(self):
		'''
		Returns a sample value from the N(0, Ez) distribution.
		:return:
		'''
		mu = 0
		sigma = self.Ez
		s = numpy.random.normal(mu, sigma, 1)
		return s
	def transitionNoise(self):
		'''
		Returns a sample value from the N(0, Ex) distribution.
		:return:
		'''
		mu = 0
		sigma = self.Ex
		s = numpy.random.normal(mu, sigma, 1)
		return s
	def add(self, matrix1, matrix2):
		matrix3 = [0,0,0,0,0,0]
		matrix3[0] = matrix1[0] + matrix2[0]
		matrix3[1] = matrix1[1] + matrix2[1]
		matrix3[2] = matrix1[2] + matrix2[2]
		matrix3[3] = matrix1[3] + matrix2[3]
		matrix3[4] = matrix1[4] + matrix2[4]
		matrix3[5] = matrix1[5] + matrix2[5]
		return matrix3

if __name__ == "__main__":
	#Sigma_x (R_k) (variance of predicted state noise.)
	Ex = numpy.array([
			  [0.1, 0.0, 0.0,   0.0,   0.0, 0.0],
                          [0.0, 0.1, 0.0,   0.0,   0.0, 0.0],
                          [0.0, 0.0, 100.0, 0.0,   0.0, 0.0],
                          [0.0, 0.0, 0.0,   0.1,   0.0, 0.0],
                          [0.0, 0.0, 0.0,   0.0,   0.1, 0.0],
                          [0.0, 0.0, 0.0,   0.0,   0.0, 100.0]])

	#Sigma_z (Q_k) (variance of observation noise)
	Ez = numpy.array([
			  [25, 0],
                          [0, 25]])

	k = KalmanFilter(Ex=Ex,Ez=Ez)
	print k.observationNoise()
	print k.transitionNoise()