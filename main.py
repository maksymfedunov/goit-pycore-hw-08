from classes import *
from save_book import *

def input_error(func):
    def inner(*args, **kwargs):
        if not args :
            return "Please check the presence of the arguments"

        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter user name"
        except IndexError:
            return "Please check the arguments"
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    message = "Contact updated." 
    record.edit_phone(old_phone, new_phone)  
    return message

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    phones = ', '.join(p.value for p in record.phones)
    return f"{name}: {phones}"
        
@input_error
def all_contacts(book):
    if not book.data:
        return "No contacts"
    return str(book)

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if birthday:
        record.add_birthday(birthday)
    return f"For {name} add birthday {birthday}"
    
@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record.birthday:
        birthday = record.birthday.value
    return f"{name}: {birthday}"
    
@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days"
    return "\n".join(f"{el['name']} : {el['birthday']}" for el in upcoming)

        
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))                      
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()