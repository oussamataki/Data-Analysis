# Django Data Manipulation and Visualization

This project is a Django-based web application that allows users to upload CSV files, perform data manipulation and statistical analysis, and visualize data with interactive charts.

---

## Features

### 1. **CSV File Upload**

- Upload CSV files via a user-friendly interface.
- Validate uploaded files for format and column presence.
- Display data in a table format for quick inspection.

### 2. **Data Manipulation**

- Perform common operations like:
  - Mean
  - Median
  - Mode
  - Standard Deviation
  - Variance
- Select specific columns for operations.

### 3. **Data Visualization**

- Generate interactive visualizations using Plotly:
  - Line charts
  - Bar charts
  - Scatter plots
  - Pie charts
- Visualize probability distributions and statistical properties.

### 4. **Probability and Statistical Analysis**

- Explore probability distributions.
- Perform statistical tests (e.g., hypothesis testing).

---

## Installation

### Prerequisites

- Python 3.8+
- Django 4.2+
- Virtual environment tool (optional but recommended)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/django-data-visualization.git
   cd django-data-visualization
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your browser and go to `http://127.0.0.1:8000/`.

---

## File Structure

```plaintext
.
├── Data
│   ├── Data
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── media
│   ├── pandass
│   │   ├── __pycache__
│   │   ├── migrations
│   │   ├── templates
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── forms.py
│   │   │   ├── models.py
│   │   │   ├── tests.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
├── proba
│   ├── __pycache__
│   ├── migrations
│   ├── templates
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
├── static
│   ├── css
│   ├── docs
│   ├── img
│   ├── js
│   ├── lib
│   ├── scss
├── test
├── vis
│   ├── __pycache__
│   ├── migrations
│   ├── templates
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
```

---

## Example CSV File

Here is a sample CSV file structure to test the application:

```csv
Name,Age,Grade,City
Alice,22,88,Paris
Bob,24,92,Lyon
Charlie,23,85,Marseille
David,21,78,Paris
Eve,22,95,Lyon
```

---

## Screenshots

### Upload CSV



### Data Visualization



### Statistical Analysis



---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Django Framework](https://www.djangoproject.com/)
- [Pandas Library](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Bootstrap](https://getbootstrap.com/)

