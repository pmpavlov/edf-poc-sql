
import re



class GetSQLFromS3:
	def __init__(self, body, sql):
		self.sample_sqls = body
		self.sqlTag = "@" + sql + "@"
		self.sql = []

	def readSQL(self):
		found = 0
		for line in self.sample_sqls.decode("utf-8").split("\n"):
			if re.search(self.sqlTag,line):
				found = (found + 1)%2
			elif found:
				self.sql.append(line.strip())

	def constructSQL(self):
		self.readSQL()
		sqlArray = []
		sql = ""

		for i in self.sql:
			if re.match(r'.*;$',i):
				sqlArray.append(sql + " " + i)
			else:
				sql = sql + i + " "

		return sqlArray
