# тут прописуємо функції, які використовуються в роутах у файлі src/routes/contacts.py
from datetime import date, timedelta
from typing import List

from sqlalchemy import extract
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactResponse, ContactUpdate


async def get_all_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]: 
    return db.query(Contact).filter(Contact.owner_id == user.id).offset(skip).limit(limit).all()


async def read_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    return db.query(Contact).filter(and_(Contact.owner_id == user.id, Contact.id == contact_id)).first()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact: 
    new_contact = Contact(first_name=body.first_name, 
                      last_name=body.last_name, 
                      email=body.email,
                      phone=body.phone,
                      birthday=body.birthday,
                      additional_info=body.additional_info,
                      owner_id=user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return ContactResponse.from_orm(new_contact)


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.owner_id == user.id, Contact.id == contact_id)).first()

    if contact:    
        if body.first_name is not None:
            contact.first_name = body.first_name
        if body.last_name is not None:
            contact.last_name = body.last_name
        if body.email is not None:
            contact.email = body.email
        if body.phone is not None:
            contact.phone = body.phone
        if body.birthday is not None:
            contact.birthday = body.birthday
        if body.additional_info is not None:
            contact.additional_info = body.additional_info
        
        db.commit()
        db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.owner_id == user.id, Contact.id == contact_id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


# async def get_upcoming_birthdays(user: User, db: Session):
#     today = date.today()
#     upcoming = today + timedelta(days=7)
#     # Порівнюємо лише місяць і день, бо рік народження не має значення для майбутнього ДН
#     contacts = db.query(Contact).filter(
#         Contact.owner_id == user.id,  # Фільтруємо за власником
#         (# Перевіряємо ДН, коли обидві дати знаходяться в межах одного року
#             (extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day) 
#         ) | (
#             (extract('month', Contact.birthday) == upcoming.month) & (extract('day', Contact.birthday) <= upcoming.day)
#         ) | (# Враховуємо перехід через НР (грудень-січень)
#             (extract('month', Contact.birthday) > today.month) & (extract('month', Contact.birthday) <= upcoming.month)
#         )
#     ).all()

#     # Фільтруємо контакти, ДН яких у минулому ( в тч і сьогодні)
#     future_birthdays = []
#     for contact in contacts:
#         if contact.birthday >= today:
#             future_birthdays.append(contact)
#         else:
#             print(f"BD for {contact.birthday, contact.email} already passed.")
#             continue
#     return future_birthdays


async def get_upcoming_birthdays(user: User, db: Session):
    today = date.today()
    upcoming = today + timedelta(days=7)
    
    # Отримуємо всі контакти користувача
    contacts = db.query(Contact).filter(Contact.owner_id == user.id).all()
    
    future_birthdays = []
    for contact in contacts:
        # Створюємо "поточний" ДН цього контакту в поточному році
        birthday_this_year = contact.birthday.replace(year=today.year)
        
        # Якщо ДН в цьому році вже минув, то переносимо його на наступний рік
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
        
        # Перевіряємо, чи потрапляє ДН в наступні 7 днів
        if today <= birthday_this_year <= upcoming:
            future_birthdays.append(contact)
        else:
            print(f"BD for {contact.birthday, contact.email} is not within the upcoming week.")
    
    return future_birthdays


async def get_contacts(db: Session, user: User, first_name: str = None, last_name: str = None, email: str = None): # вивести список всіх контактів чи для пошуку за іменем, прізвищем чи ємейлом
    # Додаємо фільтрацію за owner_id
    query = db.query(Contact).filter(Contact.owner_id == user.id)
    # query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()