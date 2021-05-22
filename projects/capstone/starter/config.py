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
    "database_name_production" : "capstone_db",
    "database_name_test" : "capstone_test_db",
    "user_name" : "postgres", # default postgres username
    "password" : "postgres", # If no password is there then just set value to None
    "port" : "localhost:5432" # default postgres port
}

bearer_tokens = {
    "actor": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRiaENmZERWb09CYmVVb1k2bTJyZCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbGVhcm4tYXV0aC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBhMjM2MWJjYmU2YzEwMDZiNmYyYjZlIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MjE2NjM0MjMsImV4cCI6MTYyMTc0OTgyMywiYXpwIjoiYjZkbDZoM29ROVR0Z2xESlZWMThUTHJDenFINU9NOHUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyJdfQ.mSgyMHgON4ll4ElwgfbNxseYkFWz2YP-GiQE_eELT_5ICLtKhro-gSuDeASi7DzFpQ_t2Vrp2vhumNd72QrZ72PNYji5toMg1aEPEb1rGgz18idZ7ofw8G4ZyjTnw5UyNCs_wmF7pKwo8ZkRzA7IkTc0f-LPWxJ0uGBMKSzI3FuMspS0KyDEZKtp3_lxgnezldaMJzdPEzS644d6eBJCEfak99NcJ9VqELAjwWj33ClLVeWTZIiQsSxJRoVXigNL9-jOkIRdGTzX5dFwviQLV82QY5Eo7OUw4Utc5Eq8Y6PLcdWxEcAWC-3vBfnT2nULE_E6Y2gLwgRC3LPmxuzDDg",
    "director" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRiaENmZERWb09CYmVVb1k2bTJyZCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbGVhcm4tYXV0aC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBhMjM1ZTJhMGIwYmIwMDZhZDljY2FlIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MjE2NjM3NTIsImV4cCI6MTYyMTc1MDE1MiwiYXpwIjoiYjZkbDZoM29ROVR0Z2xESlZWMThUTHJDenFINU9NOHUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Gw58ALfzhiu8cN7iz0DzYw6HQInVYgaTcfllfTykr9PRTiGcGT_wLxPULTV-X1deJxL7TqQSWEQPJWfS2ToBK5E887jObNcesSwogwhwzwfkDJij42CY0FP6wGE3O-wGP9SPc1kWzROYSDjUsEIcNljVUHFssotW-kMf7SpFUWxef_5koy4wOPy9dHbKF3oE5DE93cvBZ78Qk8rESYwgaQNroKI_Qttc4pTQl4g6lZuMX61P0v7zwCxd2yGZ4hzJ0WDSXqpZ0EMWtLdJgL_swvB7odlMt02cbMPscO04TIxluGXEXjGXlc2YXZ4xKhkfsQdlT6MqGQ4o_mZTwXD2cg"
}