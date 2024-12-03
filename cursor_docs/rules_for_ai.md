# **Cursor IDE Pre-Prompt: Coding Standards and Project Practices**

We are the software company MetaReps so all liceneces are attributed :

License

MetaReps Copyright 2024 - 2025

Unless otherwise noted

## **Environment Setup**

* **Operating System:** macOS
* **Primary Package Managers:**
  * `pyenv` for Python version management
  * `pip` for Python package management
  * `homebrew` for installing system-level dependencies
* **Additional Tools:**
  * `npm` for JavaScript package management
  * `conda` for managing isolated Python environments when needed
  * `docker` for containerization and consistent deployment environments
* **Available Frameworks:**
  * **Backend:** `Flask`, `Django`, `FastAPI`
  * **Frontend:** `React`, `Vue.js`, `Angular`
* **Primary Programming Languages:**
  * **Default:** Python
  * Others: JavaScript, CSS, HTML, C, C++

## **Project Initialization and Structure**

* **Version Control:**
  * Always initiate a new **Git** repository at the start of every project.
    * Use `git init` in the project directory.
    * Before initiating, search for existing repositories to avoid duplication.
  * Create and maintain a `.gitignore` file to exclude unnecessary files.
  * Use `.cursorignore` to manage files specific to Cursor IDE.
* **Directory Structure:**
  * **Top-Level Project Folder:**
    * Named after the project.
    * May contain initial documentation (`docs/`) but avoid cluttering with files not related to overall project management.
  * **Subdirectories:**
    * Organize code into subfolders like `src/`, `frontend/`, `backend/`, `tests/`, etc.
    * Each subdirectory focuses on a specific feature or component of the project.
    * Avoid creating new folders in the top-level directory unless necessary.
  * **File Management:**
    * Before creating new files or folders, check if they already exist.
    * Ensure new files follow the established directory tree.
* **Configuration Files:**
  * Centralize configuration in files like `config.py` or `.env`.
  * Sanitize all hard-coded paths; use dynamic paths linked to the project directory.
  * Store secrets and sensitive data securely, using environment variables or secret management tools.

## **Coding Standards and Best Practices**

* **General Principles:**
  * **Professional-Grade Code:** Aim for maintainable, scalable, and efficient code suitable for production environments.
  * **No Boilerplate Code:** Avoid unnecessary or placeholder code; every line should serve a purpose.
  * **Iterative Development:** Continuously refine and improve codebases, focusing on growth and scalability.

### **Code Quality**

* **Strong Typing:**
  * Use type hints and annotations throughout the code (PEP 484 compliance).
  * Utilize **Pydantic** as a standard for data validation and settings management.
    * **Pydantic** ensures data integrity and simplifies settings management.
* **Error Handling:**
  * Implement robust error handling using `try-except` blocks.
  * Catch specific exceptions and handle them appropriately.
  * Avoid bare `except` clauses.
* **Input Validation and Sanitization:**
  * Validate all inputs at the boundaries of the system (e.g., API endpoints, user inputs).
  * Sanitize inputs to prevent injections and security vulnerabilities.
  * Use validation libraries or frameworks when available.
    * Leverage **Pydantic** models for input validation.
* **Logging:**
  * Implement **verbose logging** for every function.
  * Use Python's built-in `logging` module.
  * Configure loggers to output to both console and log files.
  * Include timestamps, log levels, and contextual information.
* **Documentation:**
  * **Docstrings:**
    * Write comprehensive docstrings for all modules, classes, and functions (PEP 257 compliance).
    * Include descriptions of parameters, return values, exceptions raised, and usage examples.
  * **Comments:**
    * Add inline comments to explain complex logic or important decisions.
    * Keep comments up-to-date with code changes.
* **Modularity and Code Organization:**
  * **Script/Module Size:**
    * Keep individual scripts/modules between **50 to 300 lines**.
    * If a module exceeds this, consider refactoring and modularizing.
  * **Reusability:**
    * Identify and extract reusable code into utility modules or packages.
    * Promote DRY (Don't Repeat Yourself) principles.
  * **Imports:**
    * Organize imports following PEP 8 guidelines.
    * Remove unused imports; ensure all necessary imports are present.
    * Before removing functions or imports, thoroughly check for dependencies.

### **Framework-Specific Practices**

* **Backend Frameworks:**
  * Use frameworks like `Flask`, `Django`, or `FastAPI` based on project requirements.
  * Follow the conventions and best practices of the chosen framework.
  * **FastAPI:**
    * When using FastAPI, utilize **Pydantic** models for request and response validation.
    * Leverage built-in features for efficient API development.
  * **Flask/Django:**
    * Use the frameworks' tools for routing, middleware, and templating.
    * Adhere to the frameworks' conventions for directory structures and naming.

### **Testing and Quality Assurance**

* **Unit Testing:**
  * Write unit tests for all functions and modules using `unittest` or `pytest`.
  * Aim for high test coverage, particularly for critical components.
* **Integration Testing:**
  * Test the interaction between different modules and services.
  * Use tools appropriate for the framework and language.
* **Continuous Integration:**
  * Set up CI/CD pipelines (e.g., with GitHub Actions, Jenkins).
  * Automate testing, linting, and deployment processes.

### **Security Practices**

* **Input Sanitization:**
  * Always sanitize user inputs to prevent SQL injection, XSS, and other attacks.
  * Use parameterized queries or ORM features to interact with databases.
* **Dependency Management:**
  * Regularly update dependencies to patch vulnerabilities.
  * Use tools like `pip-audit` to check for known security issues.
* **Secret Management:**
  * Do not hard-code secrets or credentials.
  * Use environment variables or secret management systems.

### **Performance Optimization**

* **Efficiency:**
  * Write code optimized for performance without sacrificing readability.
  * Use profiling tools to identify bottlenecks (e.g., `cProfile`, `PyInstrument`).
* **Scalability:**
  * Design systems that can scale horizontally and vertically.
  * Consider asynchronous programming and concurrency where appropriate.
    * Use `asyncio`, `Celery` for background tasks.

## **File and Folder Documentation**

* **README.md Files:**
  * **Project-Level README:**
    * Overview of the project.
    * Installation instructions.
    * Usage examples.
    * Contribution guidelines.
    * License information.
  * **Folder-Level READMEs:**
    * Detailed descriptions of the folder's purpose.
    * Explanation of contained modules, scripts, and their interactions.
    * Technical details, design decisions, and reasoning.
  * **Script-Level Documentation:**
    * Inline documentation and comments within scripts.
    * Docstrings for functions, classes, and methods.
* **Additional Documentation:**
  * **To-Do Lists:** Maintain `TODO` sections or files for tracking upcoming tasks.
  * **Coding Standards:** Include a `CODING_STANDARDS.md` outlining conventions specific to the project.
  * **Changelogs:** Keep a `CHANGELOG.md` to document changes over time.

## **Collaboration and Workflow**

* **Communication:**
  * Encourage asking questions and making suggestions for improvement.
  * Document discussions and decisions for future reference.
* **Code Reviews:**
  * Implement peer reviews for all significant code changes.
  * Use pull requests with detailed descriptions and context.
* **Branching Strategy:**
  * Use a consistent branching model (e.g., GitFlow).
  * Keep the `main` branch stable and release-ready.
* **Commit Messages:**
  * Write clear, concise commit messages following the convention:

    ```javascript
    graphqlCopy code[Type] Short description (Fixes #issue_number)
    
    Detailed description of the changes.
    
    ```
    * Types include `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

## **Development Workflow**

* **IDE Usage:**
  * Run code directly from Cursor IDE.
  * Use the integrated terminal for CLI interactions.
* **Task Automation:**
  * Use `Makefile` or task runners like `invoke` or `fabric` for common tasks.
* **Environment Consistency:**
  * Use virtual environments (`venv`, `conda`) to maintain consistent dependencies.
  * Provide `requirements.txt` or `Pipfile` for dependency management.

## **Additional Tools and Libraries**

* **Pydantic:**
  * Use **Pydantic** as a standard for data validation and settings management.
  * Define data models with type hints and validation rules.
  * Example:

    ```javascript
    pythonCopy codefrom pydantic import BaseModel
    
    class User(BaseModel):
        id: int
        name: str
        email: str
    
    ```
* **Linters and Formatters:**
  * Use `flake8`, `pylint`, or `black` for code linting and formatting.
  * Enforce coding standards automatically.
* **Documentation Generation:**
  * Use tools like `Sphinx` or `MkDocs` to generate project documentation.

## **Future-Proofing and Scalability**

* **Planning for Upgrades:**
  * Design with extensibility in mind; make it easy to add new features.
  * Use design patterns that promote scalability.
* **Dependency Injection:**
  * Use dependency injection to decouple components and improve testability.
* **Microservices and APIs:**
  * Consider breaking down large applications into microservices when appropriate.
  * Design clear and well-documented APIs for inter-service communication.

## **Data Handling and Storage**

* **Database Management:**
  * Use ORM tools like `SQLAlchemy` or Django ORM for database interactions.
  * Ensure that data models are well-defined and normalized.
* **Data Serialization:**
  * Use formats like JSON or YAML for data interchange.
  * Validate serialized data before processing.

## **User Interface and Experience**

* **Frontend Development:**
  * Use modern JavaScript frameworks (`React`, `Vue.js`, `Angular`) as per project requirements.
  * Ensure responsive design and accessibility compliance.
* **Styling:**
  * Use CSS preprocessors like SASS or LESS for maintainable stylesheets.
  * Follow consistent styling conventions.
* **Template Engines:**
  * Use template engines like Jinja2 (Flask, Django) for rendering HTML templates.

## **Deployment and Operations**

* **Containerization:**
  * Use **Docker** to containerize applications for consistent deployment.
  * Maintain `Dockerfile`s and `docker-compose.yml` files as needed.
* **Continuous Deployment:**
  * Automate deployment processes to staging and production environments.
* **Monitoring and Logging:**
  * Implement application monitoring using tools like **Prometheus** or **Grafana**.
  * Ensure logs are aggregated and searchable (e.g., using the **ELK Stack**).

## **Miscellaneous Best Practices**

* **License Compliance:**
  * Ensure all dependencies comply with the project's licensing.
  * Include a `LICENSE` file in the project root.
* **Ethical Considerations:**
  * Be mindful of the ethical implications of the software being developed.
  * Ensure compliance with data protection regulations (e.g., GDPR).
* **SEO and Performance (Web Applications):**
  * Optimize web applications for search engines and performance.
  * Use tools like Google Lighthouse to audit web applications.

## License

MetaReps Cpoyright 2024


By integrating these comprehensive guidelines into our development workflow, we ensure that our projects meet professional standards and are well-prepared for future growth and maintenance. These practices promote code quality, security, collaboration, and efficiency across all stages of development.