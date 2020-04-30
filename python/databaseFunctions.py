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
    cursor.execute("CREATE TABLE IF NOT EXISTS senateDisclosures ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "transaction_date text,"
                   "owner text,"
                   "ticker text,"
                   "asset_description text,"
                   "asset_type text,"
                   "transaction_type text,"
                   "amount text,"
                   "comment text,"
                   "senator text,"
                   "ptr_link text);")
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


def createSearch(sql, search, fields):
    # Create search syntax
    values = ()
    for i in range(len(fields)):
        if i <= 1 or search[i] is None:  # Skip id, sendto, and anything empty
            continue
        else:
            switch = search[i][:2]  # Test if searching for LIKE or IS
            if switch == "c/":
                values += (search[i][2:],)
                sql += f"LOWER({fields[i]}) LIKE '%' || LOWER(?) || '%' AND "
            elif switch == "e/":
                values += (search[i][2:],)
                sql += f"LOWER({fields[i]}) = LOWER(?) AND "
            else:
                print(f"Error processesing search: {search[0]}")
    # Remove trailing AND and add semicolon
    sql = sql[:-5] + ";"
    return sql, values


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
    sql, values = createSearch(sql, search, fields)
    # Commit
    print(sql, values)
    cursor.execute(sql, values)
    # Return response
    return cursor.fetchall()


def searchSenateDisclosures(cursor, search):
    sql = f"SELECT * FROM senateDisclosures WHERE "
    fields = ["id", "sendto", "transaction_date", "owner", "ticker", "asset_type", "transaction_type", "amount",
              "comment", "senator", "ptr_link"]
    sql, values = createSearch(sql, search, fields)
    # Commit
    print(sql, values)
    cursor.execute(sql, values)
    # Return response
    return cursor.fetchall()


def insertSenateDisclosure(cursor, transaction_date, owner, ticker, asset_description, asset_type, transaction_type,
                           amount, comment, senator, ptr_link):
    """
    Insert a new senate disclosure transaction into the memory database
    :param cursor: Database cursor
    :param transaction_date: Value
    :param owner: Value
    :param ticker: Value
    :param asset_description: Value
    :param asset_type: Value
    :param transaction_type: Value
    :param amount: Value
    :param comment: Value
    :param senator: Value
    :param ptr_link: Value
    :return: None
    """
    sql = "INSERT INTO senateDisclosures " \
          "(transaction_date, owner, ticker, asset_description, asset_type, transaction_type, amount, comment, " \
          "senator, ptr_link) " \
          "VALUES (?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(
        sql,
        (transaction_date, owner, ticker, asset_description, asset_type, transaction_type, amount, comment, senator,
         ptr_link)
    )


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


def getOpportunityFiltersByEmail(cursor, email):
    """
    Returns a list of filters for a given email address
    :param cursor: connection cursor
    :param email: email address to search
    :return: Array
    """
    cursor.execute(f"SELECT * FROM opportunityFilters WHERE sendto='{email}';")
    filters = cursor.fetchall()
    return filters


def getSenateDisclosureFiltersByEmail(cursor, email):
    cursor.execute(f"SELECT * FROM senateDisclosureFilters WHERE sendto='{email}';")
    filters = cursor.fetchall()
    return filters
