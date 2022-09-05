Setup Instructions:

Python version required - 3.8


1. Create a virtual environment with **Python 3.8**, activate the virtual environment and follow the upcoming steps.
2. navigate to the git project directory and install the requirements with the command, **pip install -r requirements.txt**
3. In git project directory migrate the database using, **python manage.py migrate**
4. Create superuser/admin user using **python manage.py createsuperuser**
5. Run the server using **python manage.py runserver**.
6. Hit the postman collection starting from sign up API.

If facing any difficulties in setting up the server please contact me - +91 9566273674

POSTMAN COLLECTION:
https://www.getpostman.com/collections/60820f2b85e174ec4082

All the details for each api is given in the postman collecton. Refer to that for queries related to params to send.
 
Note:
Schools can only edit/filter students belonging to their own school and not other schools.
