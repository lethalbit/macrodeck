from enum import Enum

class ActionType(Enum):
	TEXT = 1,
	KEYSTROKE = 2,
	EXEC = 3,
	NOP = 255,

class KeyDirection(Enum):
	PRESS = 1,
	RELEASED = 2,

class Action:
	def __init__(self, on = KeyDirection.PRESS, act_type = ActionType.NOP, payload = '', f_json = None):
		if f_json is not None:
			self.on      = f_json['on'] if 'on' in f_json else on
			self.type    = f_json['type'] if 'type' in f_json else act_type
			self.payload = f_json['payload'] if 'payload' in f_json else payload
		else:
			self.on      = on
			self.type    = act_type
			self.payload = payload

	def __str__(self):
		return f'   Type: {self.type}\n    Payload: {self.payload}\n'

	def __repr__(self):
		return self.__str__()
