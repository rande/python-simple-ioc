# Python Simple IoC - Dependency Injection Container

[![CI](https://github.com/rande/python-simple-ioc/workflows/CI/badge.svg)](https://github.com/rande/python-simple-ioc/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A lightweight, **Pythonic** dependency injection container inspired by Symfony's DependencyInjection component. This library embraces Python's philosophy of simplicity while providing powerful tools for organizing complex applications.

## 🎯 Why Use Dependency Injection?

Dependency injection isn't just enterprise complexity - it's a **Pythonic pattern** that promotes:

- **Clear separation of concerns** - Each class has a single responsibility
- **Testability** - Easy to mock dependencies for unit tests
- **Flexibility** - Change implementations without touching existing code
- **Maintainability** - Explicit dependencies make code easier to understand

This approach aligns perfectly with Python's zen: *"Explicit is better than implicit"* and *"Readability counts"*.

## 🚀 Quick Start

### Installation

```bash
pip install ioc
```

### Basic Usage

1. **Define your services** in a `services.yml` file:

```yaml
parameters:
  database_url: "sqlite:///app.db"
  debug_mode: true

services:
  # Database connection
  database:
    class: myapp.database.Database
    arguments: ["%database_url%"]
  
  # User repository with injected database
  user_repository:
    class: myapp.repositories.UserRepository
    arguments: ["@database"]
  
  # User service with injected repository
  user_service:
    class: myapp.services.UserService
    arguments: ["@user_repository"]
    calls:
      - [set_debug, ["%debug_mode%"]]
```

2. **Use the container** in your application:

```python
import ioc

# Build container from configuration
container = ioc.build(['services.yml'])

# Get your services - dependencies are automatically resolved!
user_service = container.get('user_service')

# Your service is ready to use with all dependencies injected
users = user_service.get_all_users()
```

## 🏗️ Perfect for Python Projects

This library follows Python best practices:

- **Configuration over code** - Define dependencies in YAML, not scattered across your codebase
- **Explicit dependencies** - See exactly what each service needs at a glance
- **No magic** - Simple, predictable behavior that follows Python conventions
- **Framework agnostic** - Works with Flask, Django, FastAPI, or pure Python

## 📚 Advanced Features

### Service Definitions

```yaml
services:
  # Constructor injection
  email_service:
    class: myapp.EmailService
    arguments: ["@mailer", "%sender_email%"]
  
  # Method calls after construction
  logger:
    class: logging.Logger
    arguments: ["myapp"]
    calls:
      - [setLevel, ["INFO"]]
      - [addHandler, ["@file_handler"]]
  
  # Weak references (lazy loading)
  cache_service:
    class: myapp.CacheService
    arguments: ["#@redis_client"]  # Only loaded when needed
```

### Parameters and Environment

```yaml
parameters:
  # String interpolation
  log_file: "/var/log/%app_name%.log"
  
  # Environment variables
  secret_key: "%env(SECRET_KEY)%"
  
  # Default values
  redis_url: "%env(REDIS_URL):redis://localhost:6379%"
```

## 🧪 Testing Made Easy

With dependency injection, testing becomes straightforward:

```python
import unittest
from unittest.mock import Mock

class TestUserService(unittest.TestCase):
    def test_create_user(self):
        # Mock the repository
        mock_repo = Mock()
        mock_repo.save.return_value = True
        
        # Inject the mock
        user_service = UserService(mock_repo)
        
        # Test with confidence
        result = user_service.create_user("john@example.com")
        self.assertTrue(result)
        mock_repo.save.assert_called_once()
```

## 📖 Learn More

- [Documentation](https://github.com/rande/python-simple-ioc/wiki)
- [Examples](examples/)
- [API Reference](docs/)

## 🤝 Contributing

Contributions are welcome! This project follows Python community standards:

- PEP 8 code style
- Type hints for better IDE support
- Comprehensive tests
- Clear documentation

## 📄 License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

---

*"Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex."* - The Zen of Python

This library embodies these principles while providing the power and flexibility needed for serious Python applications.
