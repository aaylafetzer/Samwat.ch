# Imports for memory database
import sqlite3

# Imports for managed pgSQL database
import psycopg2


def createMemoryDatabase(path):
    """
    Creates a SQLite database in memory
    :return: connection, cursor
    """
    print("Making database at " + path)
    conn = sqlite3.connect(path)
    return conn, conn.cursor()


def createMemoryTables(cursor):
    """
    Creates a table in the memory database to hold opportunity data
    :return: None
    """
    cursor.execute("DROP TABLE IF EXISTS opportunities;")
    cursor.execute("CREATE TABLE IF NOT EXISTS opportunities ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "department text,"
                   "subTier text,"
                   "office text,"
                   "title text,"
                   "solicitationNumber text,"
                   "naicsCode text,"
                   "classificationCode text,"
                   "uiLink text,"
                   "baseType text);")
    # TODO: Awards


def insertOpportunity(cursor, department, subTier, office, title, solicitationNumber, naicsCode, classificationCode,
                      uiLink, baseType):
    """
    Insert a new opportunity into the memory database
    :param cursor: Database cursor
    :param department: Value
    :param subTier: Value
    :param office: Value
    :param title: Value
    :param solicitationNumber: Value
    :param naicsCode: Value
    :param classificationCode: Value
    :param uiLink: Value
    :param baseType: Value
    :return: None
    """
    sql = "INSERT INTO opportunities " \
          "(department, subtier, office, title, solicitationnumber, naicscode, classificationcode, uilink, basetype) " \
          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(sql,
                   (department, subTier, office, title, solicitationNumber, naicsCode, classificationCode, uiLink,
                    baseType))


def searchOpportunities(cursor, search):
    """
    Search for matching opportunities in the memory database
    :param cursor: Database cursor
    :param search: tuple
    :return: Dict
    """
    sql = f"SELECT * FROM opportunities WHERE "
    fields = ["id", "sendto", "department", "subTier", "office", "title", "solicitationNumber",
              "naicsCode", "classificationCode"]
    # Create search syntax
    for i in range(len(fields)):
        if i <= 1 or search[i] is None:  # Skip id, sendto, and anything empty
            continue
        else:
            switch = search[i][:2]  # Test if searching for LIKE or IS
            if switch == "c/":
                sql += f"LOWER({fields[i]}) LIKE LOWER('%{search[i][2:]}%') AND "
            elif switch == "e/":
                sql += f"LOWER({fields[i]}) = LOWER('{search[i][2:]}') AND "
            else:
                print(f"Error processesing search: {search[0]}")
    # Remove trailing AND and add semicolon
    sql = sql[:-5] + ";"
    # Commit
    print(sql)
    cursor.execute(sql)
    # Return response
    return cursor.fetchall()


def insertAward():
    # TODO: Awards
    pass


def searchAwards():
    # TODO: Awards
    pass


def pSQLConnection(host, port, username, password):
    """
    Create a connection to a pSQL server
    :param host: IP address of server
    :param port: Port of server
    :param username: Username
    :param password: Password
    :return: connection, cursor
    """
    conn = psycopg2.connect(database="filters",
                            user=username,
                            password=password,
                            host=host,
                            port=port)
    cursor = conn.cursor()
    return conn, cursor


def getEmailAddresses(cursor):
    """
    Get the unique email addresses from the managed pgSQL database
    :param cursor: Connection cursor
    :return: Array
    """
    cursor.execute("SELECT DISTINCT sendto FROM filters;")
    emails = cursor.fetchall()
    return emails


def getFiltersByEmail(cursor, email):
    """
    Returns a list of filters for a given email address
    :param cursor: connection cursor
    :param email: email address to search
    :return: Array
    """
    cursor.execute(f"SELECT * FROM filters WHERE sendto=\'{email}\'")
    filters = cursor.fetchall()
    return filters
