from flask import Flask, render_template, request, redirect, url_for
from abc import ABC, abstractmethod

app = Flask(__name__)

# ======= SRP & Strategy Pattern Implementation ========
class AuthenticationManager:
    """Handles authentication logic (SRP)"""
    @staticmethod
    def validate_credentials(username: str, password: str) -> str:
        if len(username) != 5 or not username.isalpha():
            return 'Username must be exactly 5 alphabetic characters.'
        if 'SWUST' not in password:
            return 'Password must contain "SWUST".'
        return None

class TriangleValidator(ABC):
    """Abstract base class for validation (Open/Closed)"""
    @abstractmethod
    def validate(self, a: float, b: float, c: float) -> bool:
        pass

class BasicTriangleValidator(TriangleValidator):
    """Concrete implementation of triangle validation"""
    def validate(self, a: float, b: float, c: float) -> bool:
        return (a + b > c) and (a + c > b) and (b + c > a)

# ======= Dependency Injection Setup ========
class AppController:
    """Coordinates application workflow (Dependency Injection)"""
    def __init__(self, auth_manager: AuthenticationManager, triangle_validator: TriangleValidator):
        self.auth_manager = auth_manager
        self.triangle_validator = triangle_validator

    def handle_login(self, username: str, password: str):
        error = self.auth_manager.validate_credentials(username, password)
        return error

    def handle_triangle_check(self, a: float, b: float, c: float):
        if a <= 0 or b <= 0 or c <= 0:
            return False, 'All numbers must be positive.'
        return self.triangle_validator.validate(a, b, c), None

# ======= Application Setup ========
controller = AppController(
    auth_manager=AuthenticationManager(),
    triangle_validator=BasicTriangleValidator()
)

# ======= Routes ========
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    error = controller.handle_login(
        request.form['username'],
        request.form['password']
    )
    if error:
        return render_template('login.html', error=error)
    return redirect(url_for('triangle'))

@app.route('/triangle')
def triangle():
    return render_template('triangle.html')

@app.route('/check-triangle', methods=['POST'])
def check_triangle():
    try:
        a = float(request.form['a'])
        b = float(request.form['b'])
        c = float(request.form['c'])
    except ValueError:
        return render_template('triangle.html', error='Please enter valid numbers.')
    
    is_triangle_result, error = controller.handle_triangle_check(a, b, c)
    if error:
        return render_template('triangle.html', error=error)
    
    return render_template('result.html', 
        is_triangle=is_triangle_result,
        a=a, b=b, c=c
    )

if __name__ == '__main__':
    app.run(debug=True)