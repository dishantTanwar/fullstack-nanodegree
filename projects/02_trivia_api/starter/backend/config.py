import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
# "postgresql://postgres:postgres@{}/{}".format('localhost:5432', database_name)
# test
# "postgresql://db_setup["user_name"]:dbsetup["password"]@{}/{}".format(db_setup["port"] db_setup["database_name_test"])
# main_app
# "postgresql://db_setup["user_name"]:dbsetup["password"]@{}/{}".format(db_setup["port"] db_setup["database_name_production"])



db_setup = {
    "database_name_production" : "trivia",
    "database_name_test" : "trivia_test",
    "user_name" : "postgres", # default postgres user name
    "password" : "postgres", # if applicable. If no password, just type in None
    "port" : "localhost:5432" # default postgres port
}