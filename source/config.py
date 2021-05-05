NODE_NUMBER_ENVIRONMENT_VAR: str = 'NODE'
DATABASE_PASSWORD_VAR: str = 'COURSEWORK2_DB_PASSWORD'
NODE_NUMBER: int = 1  # Should be unique for each node

DB_NAME: str = 'age-of-python'
DB_USER: str = 'postgres'
DB_HOST: str = '185.139.70.166'

SQL_GET_SOLUTION: str = f'''SELECT *
                FROM management_solution
                WHERE management_solution.status=%s
                AND management_solution.node=%s;'''

SQL_GET_CODE_FILE: str = f'''SELECT * 
                FROM management_codefile
                WHERE id=%s;'''

SQL_GET_TESTS: str = f'''SELECT *
                FROM management_test
                WHERE task_id=%s'''

SQL_UPDATE_SOLUTION: str = '''UPDATE management_solution
                        SET {field} = '{value}'
                        WHERE id = {id};'''

CATCH_SOLUTIONS_DELAY: int = 5  # Time in seconds

BUILD_SOURCE_MAX_TIME: int = 15  # Time in seconds
