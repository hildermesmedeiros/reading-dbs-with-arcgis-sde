from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
conf_rel_path = "config.ini"
config.read(conf_rel_path)

ENV_TYPE = 'Dev'
DBHOST = config[ENV_TYPE]['DBHOST']
DBPORT = config[ENV_TYPE]['DBPORT']
DB = config[ENV_TYPE]['DB']
DBUSER = config[ENV_TYPE]['DBUSER']
DBPASS = config[ENV_TYPE]['DBPASS']


class GetConn:
    def __init__(self, host: str = DBHOST, port: str = DBPORT, dbname: str = DB, user: str = DBUSER,
                 password: str = DBPASS):
        """
        Initialize with database connection details.
        :param host: Host address of the PostgreSQL server
        :param port: Port number
        :param dbname: Database name
        :param user: Username for the database
        :param password: Password for the database
        """
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None

    def __enter__(self):
        # Create an engine
        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')
        # Create a Session class bound to the engine
        Session = sessionmaker(bind=self.engine)
        # Instantiate a session
        self.session = Session()
        print("Database connection and session established.")
        # Return both the session and the engine
        return self.session, self.engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the session
        if self.session:
            self.session.close()
            print("Session and connection closed.")
        # Dispose the engine
        if self.engine:
            self.engine.dispose()
            print("Engine Disposed")
