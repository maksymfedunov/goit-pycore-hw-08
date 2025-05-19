from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Имя - обязательное поле")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("В номере телефона должно содержаться 10 цифр")   
        super().__init__(value)
        
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Неправильный формат даты. Используйте дд.мм.гггг")           

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_phone(self, phone):
        if type(phone) == str:
            phone = Phone(phone)
        self.phones.append(phone)
        
    def remove_phone(self, phone):
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete:
            self.phones.remove(phone_to_delete)
        else:
            raise ValueError("Номер не найден")    
            
    def edit_phone(self, old_phone, new_phone):
        if type(new_phone) == str:
                new_phone = Phone(new_phone)
        phone_to_change = self.find_phone(old_phone)
        if phone_to_change:
            self.add_phone(new_phone)
            self.remove_phone(old_phone) 
        else:
            raise ValueError("Этого номера нет в телефонной книге")
        
    def find_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                return el
        return None           
    
    def add_birthday(self, birthday):
        if type(birthday) == str:
            birthday = Birthday(birthday)
        self.birthday = birthday    
        
    def __str__(self):
        birthday_string = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "не указан"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday:{birthday_string}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Контакт не найден")    
    
    def get_upcoming_birthdays(self, days = 7):
        upcoming_birthdays = []
        today = date.today() 
        
        for record in self.data.values():
            if record.birthday is None:
                continue
            
            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday.replace(year = today.year)
            
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year = today.year + 1)
                
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self.adjust_for_weekend(birthday_this_year)
                congratulation_date = birthday_this_year.strftime("%d-%m-%Y")
                upcoming_birthdays.append({"name": record.name.value, "birthday": congratulation_date})
        return upcoming_birthdays
            
    @staticmethod
    def find_next_weekday(birthday, weekday):
        days_ahead = weekday - birthday.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return birthday + timedelta(days=days_ahead)
    
    @staticmethod
    def adjust_for_weekend(birthday):
        if birthday.weekday() >= 5:
            return AddressBook.find_next_weekday(birthday, 0)
        return birthday
    
    def __str__(self):
        return "\n".join(f"{name}: {record}" for name, record in self.data.items()) 
    
                    