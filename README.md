# In Memory Database

A simple programming exercise implementing an in memory database.

The database supports the following commands.

**SET** *NAME VALUE*
Set the variable name to the value value. Neither variable names nor values will contain spaces.

**GET** *NAME*
Print out the value of the variable name, or NULL if that variable is not set.

**UNSET** *NAME*
Unset the variable name, making it just like that variable was never set.

**NUMEQUALTO** *VALUE*
 Print out the number of variables that are currently set to value. If no variables equal that value, print 0.
 
 **BEGIN**
  Open a new transaction block. Transaction blocks can be nested; a BEGIN can be issued inside of an existing block.
  
  **ROLLBACK**
 Undo all of the commands issued in the most recent transaction block, and close the block. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
 
 **COMMIT**
 Close all open transaction blocks, permanently applying the changes made in them. Print nothing if successful, or print NO TRANSACTION if no transaction is in progress.
 
 **END** 
 Exit the program

##Examples


```
BEGIN
SET a 10
GET a # 10
BEGIN
SET a 20
GET a # 20
ROLLBACK
GET a # 10
ROLLBACK
GET a # NULL
END

```
```
SET a 20
BEGIN
NUMEQUALTO 20 # 1
BEGIN
UNSET a
NUMEQUALTO 20 # 0
ROLLBACK
NUMEQUALTO 20 # 1
COMMIT
END
```
