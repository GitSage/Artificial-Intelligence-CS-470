__author__ = 'lexi'

class KalmanFilter():
	def __init__(self, Ex, Ez):
		#THESE MUST BE GIVEN IN ADVANCE. THEY NEVER CHANGE.
		# Transition noise ~ N(0, Ex)
		# Observation noise ~ N(0, Ez)

		# (Learning Sutie Variable Name), (variable name from Walter's packet), (Description)
		self.Ex = Ex #Sigma_x (R_k) (variance of predicted state noise.)
		self.Ez = Ez #Sigma_z (Q_k) (variance of observation noise)

		#K_tplus1 = Ek H^T (H Ek H^T + Ez)^(-1)
		self.kalmanGain #(K_tplus1) (K_k) ("Kalman Gain": Higher if sensor is more certain. Lower if sensor is more uncertain (high variance).)
		self.H # (H_k) (converts from state to sensor reading)
		self.Ht #H Transpose

		self.predictedObservation #(z_tplus1) (Z_k) (predicted observation)
		self.Et #Sigma_t (E_{k-1}) (previous "variance posterior")

		#Mean and Variance of X_k (x_k is Gaussian a.k.a. Normal distribution)
		#ut = F u^_{k-1} + B uk
		#Ek = A E_{k-1} A^T + Ex
		self.variancePrior #(Ek) (E_k) (variance prior (of the predicted state))
		self.priorMean #(ut) (u-_k) (mean of the predicted state)
		self.F # (A) (a physics matrix)
		self.posteriorMean #u_{t+1} (u^_t)
		self.I #Identity matrix

	def update(self, uk):
		'''
		Do Bayesian Kalman-Filter update. (Get new prior based on observation.)
		:param uk: The observation (from the sensor)
		:return: A sample point from the Posterior distribution (A Gaussian distribution
		with mean u^_k and variance E^_K).
		'''

		self.predictedObservation = (self.H * self.predictedState) + self.observationNoise()

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
		pass
	def transitionNoise(self):
		'''
		Returns a sample value from the N(0, Ex) distribution.
		:return:
		'''
		pass