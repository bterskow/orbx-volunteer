from abc import ABC, abstractmethod

class Base(ABC):
	@abstractmethod
	def select(self):
		pass
