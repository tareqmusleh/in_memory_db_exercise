#!/usr/bin/env python

""" 
To run the in memory database program just run:

python in_memory_db.py

From there each command can be entered in one at a time. 
"""

from collections import defaultdict

# Special command to end the program
END_COMMAND = 'END'

# Mapping of command with database function
INPUT_COMMANDS = {'SET': 'set', 'UNSET': 'unset', 'NUMEQUALTO': 'num_equal_to', 'GET': 'get',
				  'BEGIN': 'begin', 'COMMIT': 'commit', 'ROLLBACK': 'rollback'}

class InMemoryDatabase(object):

	def __init__(self, *args, **kwargs):

		"""
		__db: in memory database that stores the data
		__transactions: stack of transactions for use in a rollback 
		__value_count: count of each value in the database for quick count lookups
		"""

		self.__db = {}
		self.__transactions = []
		self.__value_count = defaultdict(int)


	def get(self, name):
		""" Returns the value from the database. If value does not exist, returns NULL """

		return self.__db.get(name, 'NULL')


	def set(self, name, value, commit=False):

		"""
		Inserts/Updates the name's value in the database. 
		"""
		
		old_value = self.__db.get(name, 'NULL')
		self.__db[name] = value
		self.__value_count[value] += 1
		if self.__value_count[old_value]:
			self.__value_count[old_value] -= 1

		# if a transaction is open, then append the command to the last element of the stack
		if self.__transactions and not commit:
			# if the element didn't exist before (old_value is NULL) make the rollback command UNSET
			if old_value != 'NULL':
				self.__transactions[-1].append('SET {name} {old_value}'.format(name=name, old_value=old_value))
			else:
				self.__transactions[-1].append('UNSET {name}'.format(name=name))
	
	def unset(self, name, commit=False):

		""" Deletes the name variable from the database and decrements the value count for it's value. """

		value = self.__db[name]
		del self.__db[name]
		self.__value_count[value] -= 1

		# if a transaction is open, then append the command to the last element of the stack
		if self.__transactions and not commit:
			self.__transactions[-1].append('SET {name} {value}'.format(name=name, value=value))


	def num_equal_to(self, value):
		""" Returns the number of elements in the database equal to the value. """

		return self.__value_count[value]


	def rollback(self):
		""" Rollsback the most recent transaction if it exists """

		if not self.__transactions:
			return "NO TRANSACTION"

		transaction = self.__transactions.pop()

		for rollback_command in reversed(transaction):
			command = rollback_command.split()
			db_command = INPUT_COMMANDS[command.pop(0)]
			db_function = getattr(self, db_command)
			# for rollbacks, we don't want to rollback a rollback, just commit straight to the db.
			db_function(*command, commit=True)


	def commit(self):
		""" Commits to the database """

		if not self.__transactions:
			return "NO TRANSACTION"

		# reset __transactions to initial state
		self.__transactions = []


	def begin(self):
		""" Initializes a new transaction block """

		self.__transactions.append([])

def process_command(command, database):
	""" Processes a list of commands """

	try:
		db_command = INPUT_COMMANDS[command.pop(0).upper()]
		# get the db function
		db_function = getattr(database, db_command)
		output = db_function(*command)
		if output is not None:
			print output

	except (TypeError, KeyError, IndexError, AttributeError):
		print "Invalid Command!"

if __name__ == "__main__":

	database = InMemoryDatabase()
	while True:
		# continuously ask the user for input commands until they enter END
		user_input = raw_input()
		if user_input == END_COMMAND:
			break
		process_command(user_input.split(), database)