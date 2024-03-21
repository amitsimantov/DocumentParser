# **Document Parser App**

### **Prerequisites**

- Python 3.9+
- MongoDB

### **Installation**

1. **Install Requirements**

   Install the required packages using: `pip install -r requirements.txt`

2. **MongoDB Setup**

    Create a new database that includes the following collections:
- `documents`
- `discrepancies`

3. **Environment Variables**

    Set the following environment variables:

- `DB_URI`: The URI connection string for your MongoDB instance.
- `DB_NAME`: The name of your database.


### **Running the Application**

To run the application, run the following command with the required arguments:

`python main.py -N <max_title_length> -D <date> -SUM <max_sum> -PATH <path_to_html_files>
`

- `-N`: Integer, specifying the maximum valid length of a title.
- `-D`: Date, in the format `YYYY-MM-DD`, specifying the maximum valid creation date. 
- `-SUM`: Integer, specifying the maximum sum of the first row.
- `-PATH`: String, path to the directory that contains your HTML files.



#### **Examples**

`python main.py -N 100 -D 2023-03-25 -SUM 500 -PATH "/path/to/html/files"`


### Design Patterns
I used factory design pattern for creating collection handlers to simplify managing different collections. 
This pattern gives the ability to encapsulate object creation, making the codebase more modular and easier to maintain. 
By using the Factory design pattern - the application can dynamically determine at runtime which specific handler is needed, without hard-coded object instantiations. 

#### Pros:

1. Scalability: adding support for new collections only requires extending the factory logic, without modifying existing code.
2. Loose Coupling: code interacts with a common interface instead of concrete implementations, reducing dependencies.
3. Code Organization: cleaner and easier to understand.

#### Cons:

1. Complexity: adding a factory design pattern may increase code complexity.
2. Indirection: additional abstraction layer can make the code harder to trace and debug.


