from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
engine = create_engine('sqlite:///../databases/employees.sqlite')
Base = automap_base()
Base.prepare(autoload_with=engine)

# Получение класса для существующей таблицы
ExistingTable = Base.classes.existing_table_name
print(ExistingTable)
