from frozendict import frozendict

import numpy as numpy


def softmax(x, beta=1):
    numerator = np.exp(beta * x)
    denominator = numerator.sum()
    return numerator / denominator


class CuriosityBinaryChoice(object):
	def __init__(self,
			     curiosity_function,
			     linking_function=softmax,
			     curiosity_kwargs=frozendict({}),
			     linking_kwargs=frozendict({})):
		self.curiosity_function = curiosity_function
		self.linking_function = linking_function
		self.curiosity_kwargs = curiosity_kwargs
		self.linking_kwargs = linking_kwargs

	def judgement(self, data):
		data_left, data_right = data
		m0 = self.curiosity(data_left, **self.curiosity_kwargs)
		m1 = self.curiosity(data_right, **self.curiosity_kwargs)
		judgement = self.linking_function([m0, m1], **self.linking_kwargs)
		return {'curiosity_left': m0,
			    'curiosity_right': m1,
			    'judgement': judgement}