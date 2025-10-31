1. How is SQL injection prevented in raw-db-connector? How is it prevented in ORM?

**Raw-db-connector (psycopg2):**
- Uses **parameterized queries** with placeholders (`%s`) instead of string interpolation
- Example: `cursor.execute("SELECT * FROM thoughts WHERE id = %s", (thought_id,))`
- Parameters are passed as tuples separately from the SQL string
- The database driver properly escapes and sanitizes the values
- Additional protection: `_sanitize_search_term()` method uses regex to remove dangerous characters from user input (e.g., semicolons, quotes)
- Sort field validation against a whitelist prevents injecting arbitrary SQL in ORDER BY clauses

**ORM (SQLAlchemy):**
- Uses **SQLAlchemy's query builder** which automatically parameterizes all values
- Example: `query.filter(Thought.id == thought_id)` is automatically converted to parameterized SQL
- Field names are validated against model attributes, preventing injection through field selection
- Uses `.ilike()` method for case-insensitive searches, which automatically escapes wildcards
- Sort field validation: `Thought.validate_sort_field()` ensures only whitelisted columns can be used
- Additional protection: `_sanitize_search_term()` method removes potentially dangerous characters

**Key Difference:** 
- Raw SQL requires manual attention to always use parameters; ORM makes it automatic by design
- ORM provides an extra layer of protection by abstracting away raw SQL construction

---

2. How is db connection implemented in both versions?

**Raw-db-connector:**
- Uses `psycopg2` directly
- Connection created in `DatabaseManager.__init__()`: `psycopg2.connect()`
- Connection string format: `dbname=api_db user=api_user password=api_password host=localhost port=5432`
- Configuration loaded from environment variables (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
- Connection stored as instance variable: `self.connection`
- Provides `get_cursor()` context manager for executing queries
- Manual connection management with explicit `close()` method

**ORM (SQLAlchemy):**
- Uses SQLAlchemy engine and session factory
- Engine created with: `create_engine(database_url, pool_size=5, max_overflow=10, pool_timeout=30)`
- Connection URL format: `postgresql://api_user:api_password@localhost:5432/api_db`
- Configuration loaded from environment variables via `DatabaseConfig` class
- Session factory created with: `sessionmaker(autocommit=False, autoflush=False, bind=self.engine)`
- Provides `get_session()` context manager that yields sessions
- Automatic connection management via context managers

**Key Difference:**
- Raw version manages a single connection object directly
- ORM uses engine + session factory pattern with connection pooling built-in
- ORM separates configuration (DatabaseConfig) from connection management (DatabaseManager)

---

3. How id db pool managed? Compare both versions?

**Raw-db-connector:**
- **No built-in connection pooling** in the basic implementation
- Uses a single connection per DatabaseManager instance
- Each request potentially shares the same connection (not thread-safe by default)
- To add pooling, would need to implement manually or use `psycopg2.pool.SimpleConnectionPool`
- Connection is reused across multiple queries until explicitly closed
- Suitable for single-threaded applications or low concurrency

**ORM (SQLAlchemy):**
- **Built-in connection pooling** via SQLAlchemy's QueuePool (default)
- Pool configuration in engine creation:
  ```python
  pool_size=5           # Keep 5 connections open
  max_overflow=10       # Allow up to 10 additional connections under load
  pool_timeout=30       # Wait 30 seconds for available connection
  pool_pre_ping=True    # Validate connections before use
  ```
- Connections are checked out from pool when session is created
- Automatically returned to pool when session is closed
- Handles connection lifecycle: creation, validation, recycling
- Thread-safe and optimized for concurrent requests
- Stale connection detection with `pool_pre_ping`

**Key Difference:**
- Raw version: manual connection management, no pooling
- ORM version: automatic pooling with configurable size and overflow
- ORM is production-ready for high-concurrency scenarios

---

4. How is a transaction managed? Compare both versions?

**Raw-db-connector:**
- Uses psycopg2's connection-level transactions
- Auto-commit mode is OFF by default
- Transaction control via connection methods:
  - `connection.commit()` - commits the transaction
  - `connection.rollback()` - rolls back on error
- Context manager pattern in `execute_transaction()`:
  ```python
  try:
      results = []
      for operation in operations:
          cursor.execute(operation['query'], operation['params'])
          results.append(cursor.fetchone())
      self.connection.commit()
  except Exception as e:
      self.connection.rollback()
      raise
  ```
- Multiple operations bundled into single transaction using a list of operations
- Example: bulk insert of 5 thoughts uses one transaction with 5 INSERT statements

**ORM (SQLAlchemy):**
- Uses session-level transactions
- Automatic transaction management via `get_session()` context manager:
  ```python
  session = self.SessionLocal()
  try:
      yield session
      session.commit()  # Auto-commit on successful completion
  except Exception as e:
      session.rollback()  # Auto-rollback on error
  finally:
      session.close()
  ```
- Explicit transaction control via `get_transaction()` context manager:
  ```python
  with self.get_session() as session:
      transaction = session.begin()
      try:
          # operations
          transaction.commit()
      except:
          transaction.rollback()
  ```
- Bulk operations use `add_all()` to batch multiple inserts in one transaction
- Session tracks all changes (Unit of Work pattern) and commits atomically

**Key Differences:**
- Raw version: explicit commit/rollback on connection object, manual transaction boundaries
- ORM version: automatic transaction management via context managers, session tracks changes
- ORM provides better abstraction with Unit of Work pattern
- Both support atomic multi-operation transactions
- ORM's session.flush() allows getting generated IDs before committing