import mysql.connector # MySql drivers
from  mysql.connector import Error
import os # Module to connect to OS properties


class MySqLConnectionCreator:

    def __init__(self):
        """class constructor
        """
        self.db_conn = self._get_db_connection()

    
    def _get_db_connection(self):
        """ Opens db connection

        Returns:
            None
        """
        try:
            host_value = os.getenv("MYSQLHOST")
            port_value = os.getenv("MYSQLPORT")
            user_value = os.getenv("MYSQLUSER")
            password_value = os.getenv("MYSQLPASSWORD")
            databse_value = os.getenv("MYSQLDATABASE")
            # Establish the connection to the MySQL database
            connection = mysql.connector.connect(
                host=host_value,
                port=port_value,
                user=user_value,
                password=password_value,
                database=databse_value
            )

            if connection.is_connected():
                print("Connection to MySQL database was successful.")
                return connection
        
        except Error as e:
            print(f"Error: '{e}'")
            return None
        
    def close_db_connection(self, connection):
        """Closes db connection

        Args:
            connection (Connection): the current connection
        """
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")



        


