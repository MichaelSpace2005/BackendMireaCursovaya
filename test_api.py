#!/usr/bin/env python3
"""
API Testing Examples
Примеры запросов для тестирования API
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000/api/v1"

class EvolutionTreeClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session = requests.Session()
    
    def register(self, username: str, email: str, password: str):
        """Регистрация нового пользователя"""
        url = f"{self.base_url}/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=data)
        print(f"[REGISTER] Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.json()
    
    def verify_email(self, token: str):
        """Верификация email"""
        url = f"{self.base_url}/auth/verify-email"
        data = {"token": token}
        response = self.session.post(url, json=data)
        print(f"[VERIFY] Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.json()
    
    def login(self, email: str, password: str):
        """Вход в систему"""
        url = f"{self.base_url}/auth/login"
        data = {
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=data)
        print(f"[LOGIN] Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}\n")
        
        if response.status_code == 200:
            self.token = result['access_token']
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
        return result
    
    def get_current_user(self):
        """Получить текущего пользователя"""
        url = f"{self.base_url}/auth/me"
        response = self.session.get(url)
        print(f"[GET_ME] Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.json()
    
    def create_mechanic(self, name: str, description: str = None, year: int = None):
        """Создать механику"""
        url = f"{self.base_url}/mechanics/"
        data = {
            "name": name,
            "description": description,
            "year": year
        }
        response = self.session.post(url, json=data)
        print(f"[CREATE_MECHANIC] Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.json()
    
    def list_mechanics(self):
        """Список всех механик"""
        url = f"{self.base_url}/mechanics/"
        response = self.session.get(url)
        print(f"[LIST_MECHANICS] Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}\n")
        return result
    
    def create_link(self, from_id: int, to_id: int, link_type: str):
        """Создать связь между механиками"""
        url = f"{self.base_url}/mechanics/links"
        data = {
            "from_id": from_id,
            "to_id": to_id,
            "type": link_type
        }
        response = self.session.post(url, json=data)
        print(f"[CREATE_LINK] Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.json()
    
    def list_links(self):
        """Список всех связей"""
        url = f"{self.base_url}/mechanics/links"
        response = self.session.get(url)
        print(f"[LIST_LINKS] Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}\n")
        return result
    
    def get_tree(self, mechanic_id: int):
        """Получить дерево эволюции механики"""
        url = f"{self.base_url}/mechanics/{mechanic_id}/tree"
        response = self.session.get(url)
        print(f"[GET_TREE] Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}\n")
        return result


def test_workflow():
    """Тестовый workflow"""
    client = EvolutionTreeClient()
    
    print("=" * 50)
    print("EVOLUTION TREE API TEST")
    print("=" * 50)
    print()
    
    # 1. Регистрация
    print("1. РЕГИСТРАЦИЯ")
    print("-" * 50)
    reg_response = client.register(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    # Получить токен верификации из ответа
    # В реальном приложении токен будет отправлен на email
    verification_token = input("Введите токен верификации из консоли сервера: ").strip()
    
    if verification_token:
        print("\n2. ВЕРИФИКАЦИЯ EMAIL")
        print("-" * 50)
        client.verify_email(verification_token)
    
    # 2. Логин
    print("3. ЛОГИН")
    print("-" * 50)
    client.login(
        email="test@example.com",
        password="password123"
    )
    
    # 3. Получить текущего пользователя
    print("4. ПОЛУЧИТЬ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ")
    print("-" * 50)
    client.get_current_user()
    
    # 4. Создать механики
    print("5. СОЗДАНИЕ МЕХАНИК")
    print("-" * 50)
    mechanics = [
        ("Jump", "Basic jump mechanic", 1980),
        ("Run", "Running mechanic", 1982),
        ("Dash", "Quick movement", 2000),
        ("Double Jump", "Jump twice in air", 2005),
    ]
    
    mechanic_ids = []
    for name, desc, year in mechanics:
        result = client.create_mechanic(name, desc, year)
        if 'id' in result:
            mechanic_ids.append(result['id'])
    
    # 5. Список механик
    print("6. СПИСОК ВСЕХ МЕХАНИК")
    print("-" * 50)
    client.list_mechanics()
    
    # 6. Создать связи
    if len(mechanic_ids) >= 2:
        print("7. СОЗДАНИЕ СВЯЗЕЙ")
        print("-" * 50)
        client.create_link(mechanic_ids[0], mechanic_ids[1], "inspired_by")
        client.create_link(mechanic_ids[1], mechanic_ids[2], "direct_descendant")
        client.create_link(mechanic_ids[0], mechanic_ids[3], "variant")
    
    # 7. Список связей
    print("8. СПИСОК ВСЕХ СВЯЗЕЙ")
    print("-" * 50)
    client.list_links()
    
    # 8. Получить дерево
    if mechanic_ids:
        print("9. ПОЛУЧИТЬ ДЕРЕВО ЭВОЛЮЦИИ")
        print("-" * 50)
        client.get_tree(mechanic_ids[0])
    
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 50)


if __name__ == "__main__":
    test_workflow()
