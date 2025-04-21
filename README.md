# 🏗️ **Terraform Code Generator**  
> Aplikacja webowa do generowania i wdrażania kodu Terraform, wykorzystująca **LangChain** i **Flask**  

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)  
![Terraform](https://img.shields.io/badge/Terraform-623CE4?style=for-the-badge&logo=terraform&logoColor=white)  
![LangChain](https://img.shields.io/badge/LangChain-FFD43B?style=for-the-badge)  

---

## 📌 **Opis projektu**  
Snippet aplikacji, która umożliwia użytkownikom generowanie kodu Terraform na podstawie poleceń tekstowych oraz automatyczne jego wdrażanie. Korzysta z modelu GPT do generowania kodu i wykonuje operacje Terraform w środowisku lokalnym.  

## ✨ **Technologie**  
🔹 **Backend:** Python, Flask, LangChain  
🔹 **Infrastruktura:** Terraform   
---

## 🚀 **Funkcjonalności**  
✅ **Generowanie kodu Terraform** na podstawie podanego polecenia  
✅ **Automatyczne zapisywanie kodu do pliku** (`main.tf`)  
✅ **Uruchamianie komend Terraform** (`init`, `plan`, `apply`)  
✅ **Interfejs webowy oparty na Flask**  
✅ **Obsługa API REST** do komunikacji z użytkownikiem  

---

## 🔧 **Uruchamianie projektu**  
Aby uruchomić aplikację lokalnie, wykonaj poniższe kroki:  

1️⃣ **Sklonuj repozytorium**  
   ```bash
   git clone https://github.com/Pioter54/PROJ1
   cd PROJ1
   ```  
2️⃣ **Zainstaluj zależności**  
   ```bash
   pip install -r requirements.txt
   ```  
3️⃣ **Ustaw zmienne środowiskowe**  
   Stwórz plik `.env` i dodaj do niego wymagane klucze API do LangChain.  
   ```env
   OPENAI_API_KEY=twoj_klucz_api
   ```  
4️⃣ **Uruchom aplikację**  
   ```bash
   python main.py
   ```  
5️⃣ **Otwórz aplikację w przeglądarce**  
   ```
   http://localhost:5000
   ```  