# CafeApp

## Project Background

CafeApp is designed to meet the needs of a pop-up café located in a busy business district. The café offers homemade lunches and refreshments to the surrounding offices and requires a software application to log and track orders efficiently.

## Client Requirements

The application aims to fulfill the following client requirements:
- Maintain a collection of products, couriers, and customers.
- Create and manage customer orders within the system.
- Update the status of orders (e.g., READY, PREPARING, DELIVERED).
- Ensure data persistence between sessions to avoid data loss.
- Load all persisted data on startup.
- Ensure the application is well-tested and reliable.
- Provide regular software updates.
- **New**: Provide data visualization for sales and orders.

## How to Run the App

To run CafeApp, follow these steps:

### Using Docker

1. **Clone the repository:**
   ```sh
   git clone https://github.com/generation-de-nat2/marko-girga-mini-project.git
   cd app
   ```

2. **Ensure you have Docker installed.**
   **Set up the environment:**
   Ensure you have Python 3.x installed. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

3. **Create and configure the `.env` file:**
   Create a `.env` file in the root directory of the project and add the following:
   ```env
   MYSQL_USER=your_mysql_username
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=your_database_name
   ```

4. **Run the Docker Compose setup:**
   ```sh
   docker-compose up -d
   ```

5. **Set up the MySQL database:**
   Ensure you have MySQL running. Create a database and set up the necessary tables using the provided SQL script `init.sql`:
   ```sh
   mysql -u your_mysql_username -p your_database_name < init.sql
   ```

6. **Run the application:**
   ```sh
   python src/app.py
   ```

## How to Run Unit Tests

CafeApp includes unit tests to ensure the functionality of its components. To run the tests, use the following command:
```sh
python -m pytest
```

## Data Visualization

CafeApp now includes data visualization features to help analyze sales and order data. To generate visualizations, follow these steps:

1. **Run the Jupyter notebook:**
   ```sh
   jupyter notebook data_visualization.ipynb
   ```

## Project Reflections

### How did your design meet the project's requirements?
The design of CafeApp addresses all the client requirements by providing a CLI-based application that allows for CRUD operations on products, couriers, customers, and orders. Data persistence is achieved using a MySQL database, ensuring no data loss between sessions. The addition of data visualization provides insights into sales and order trends.

### How did you guarantee the project's requirements?
Regular testing using Python's built-in testing framework ensured the app's reliability. The use of MySQL for data persistence, coupled with clear and logical UI design, ensured the app met the client's operational needs.

### Example of a Challenge: Database Setup
Setting up the database was a significant challenge. Ensuring all tables were created correctly with the appropriate foreign keys required careful planning and execution. Writing the SQL scripts to create tables and establish relationships between them was complex. After setting up the database, I had to write code to query data, insert new records, update existing ones, and handle transactions safely. Handling these operations and ensuring data consistency required meticulous attention to detail.

### If you had more time, what is one thing you would improve upon?
Given more time, I would improve the application's user interface by adding a graphical user interface (GUI) to make it more user-friendly.

### What did you most enjoy implementing?
I most enjoyed implementing the order management functionality, especially the interaction between different entities like customers, products, and couriers within the order menu. It was fulfilling to see the complete workflow.