#QMod_Example
"""
QREDIS Example Model
JAH 20120923
JAH 20140118 everything has been tested and seems to be working fine with python 3
"""

class QMod_Example(QMod_Template):
	"""
	General Methods for External Use; THESE SHOULD NOT BE OVERRODE IN SPECIFIC MODEL CLASSES:
	Describe - Save a description in the QREDIS database
	ClearParams - Clear parameters from the QREDIS database for specified dates
	ClearPS - Clear parameters and signals from the QREDIS database for specified dates
	ClearSignals - Clear signals from the QREDIS database for specified dates
	GetParams - Get parameters from the QREDIS database for a specified date
	GetSettings - Get model settings from the QREDIS database
	GetSignals - Get model signals from the QREDIS database for a specified date
	NextTradeBlock - Calculate the block of dates for the next trade
	NextTrainTradeBlock - Calculate the date blocks for the next model train
	RetrainCheck - Check if the model needs to be retrained
	----------------------
	Model-Specific Methods; THESE MUST BE OVERRODE IN SPECIFIC MODEL CLASSES:
	_ParseParams - Read parameters from the QREDIS database into variables
	_ParseSettings - Read model settings from the QREDIS database into variables
	_PrintSettings - Make a nice printable string with the model settings (for print model)
	_SetMe - Save default model settings to the QREDIS database; called when model is initialized
	Train - Train the model for a specific period and save parameters (and other info) to the QREDIS database
	Trade - Trade the model for a specific day and save the signal to the QREDIS database
	----------------------
	This is a sample model that does random stupid stuff, but shows how to code a model.
	The settings dict should have elements:
		'answer' (int), example = 42
		'coolest' (str), example = 'JAH'
	Load using exec(open(QREDIS_mod+'/QMod_Example.py').read())
	"""

########################## MODEL MAKER SHOULD EDIT THESE! ###############################

	def _SetMe(self, mysettings):
		# THIS SHOULD ONLY BE RUN AS PART OF THE FIRST MODEL INITIALIZATION
		# DURING MODELING, USE _ParseSettings TO SET THEM FROM THE DB!!!
		# define and save model settings (settings as opposed to parameters, which can
		# change over time; settings are constant
		self.answer = mysettings['answer']
		self.coolest = mysettings['coolest']		
		# now save		
		self._SaveSettings(['answer','coolest'], [self.answer,self.coolest], ['int','str'])
		return True
	
	def _PrintSettings(self):
		# this prints the model settings; it is called from the __str__ function
		return '\tLife Answer: %d\n\tThe coolest: %s'%(self.answer, self.coolest)
		
	def _ParseSettings(self):
		# get the saved settings
		nams,vals,typs = self.GetSettings()		
		for n,v,t in zip(nams, vals, typs):
			exec("self.%s = %s('%s')"%(n,t,v))

	def _ParseParams(self, param_date):
		# extract the parameters from the db
		nams, vals, typs = QD.GetParams(self.model_id, param_date)
		# since GetParameters extracts everything from the database as a pair of
		# arrays of strings, here we parse them, using the 
		for n,t,v in zip(nams, typs, vals):
			exec("self.%s = %s('%s')"%(n,t,v))
	
	def GetParams(self,param_date):
		"""
		Extract stored model parameters from the QREDIS Database for a specified
		date, which is required. Returns a dictionary holding the parameters.
		JAH 20121128
		"""
		self._ParseParams(param_date)
		return {'some_coef':self.some_coef, 'some_flag':self.some_flag,'some_code':self.some_code}
		
	def Train(self,train_dates,trade_dates,rndstate=None):
		"""
		Look at some data over a specified training block, then generate some kind
		of modeling parameters to store in the QREDIS database.  These are then used
		by the Trade method on subsequent day(s) to generate signals.
		"""
		# execute the actual model
		some_coef = np.random.rand()
		some_flag = 0.5>np.random.rand()
		some_code = 'abcdefghijklmnopqrstuvwxyz'[np.random.random_integers(0,25)]
		# model is finished, so store the paramters
		param_names = ['some_coef','some_flag','some_code']
		param_values = [some_coef,some_flag,some_code]
		param_types = ['float','bool','str']
		# now store	
		self._SaveParams(trade_dates[self.buffer_days:], param_names, param_values, param_types)
		return True

	def Trade(self,buffertradedates):
		"""
		Read some model parameters generated by a previous execution of the Train
		method, then generate some model to execute trading signals that are then
		stored in the QREDIS database.
		"""
		# get parameters to use
		self._ParseParams(buffertradedates[-1])
		# execute the actual model
		self.last_signal =  np.sign(np.random.rand()-0.5)		
		# store the final signal for today, which will be in .last_signal
		self._SaveSignal(buffertradedates[-1])
		return self.last_signal
