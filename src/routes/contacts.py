from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactBase, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=["contacts"]) # до цього apі-роутера будемо звертатися далі для створення роутів


@router.get("/birthdays", response_model=list[ContactResponse]) # для пошуку днів народж. у найбл. 7 днів. Цю функцію слід ставити перед ф-цією пошуку контакту за {contact_id}, інакше фаст-апі проводить пошук саме за {contact_id}, а не днем народження
async def get_upcoming_birthdays(db: Session = Depends(get_db), 
                                 current_user: User = Depends(auth_service.get_current_user)):
    print(f"searching upcoming BD for user {current_user.email}")
    bd_contacts = await repository_contacts.get_upcoming_birthdays(current_user, db)
    if not bd_contacts:
        raise HTTPException(status_code=404, detail="No upcoming birthdays")
    return bd_contacts


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user),
                       first_name: str | None = Query(None), 
                       last_name: str | None = Query(None),
                       email: str | None = Query(None)):
    print(f"Searching for contacts: current_user={current_user.email} first_name={first_name}, last_name={last_name}, email={email}")
    # Використовуємо або пошук, або просто повертаємо контакти
    contacts = await repository_contacts.get_contacts(db, current_user, first_name, last_name, email)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.read_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact {contact_id} not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             responses={201: {"description": "Contact created", "model": ContactResponse}})
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    # return await repository_contacts.create_contact(body, current_user, db)
    new_contact = await repository_contacts.create_contact(body, current_user, db)
    return ContactResponse.from_orm(new_contact)


@router.put("/{contact_id}", response_model=ContactResponse) # для редагування контактів, потрібно вносити дані в УСІ поля
async def update_contact(contact_id: int, body: ContactUpdate, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_note(note_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(note_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return contact




