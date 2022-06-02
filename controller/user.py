from fastapi import APIRouter
from repository.user_requests import *
from models.user import User
from db.database import Database
from repository.response import Response
from sqlalchemy import and_, desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()

@router.get("/")
# async def read_user():
#     return {"name": "John", "email": "john@example.com"}
async def get_all_users(page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(User).filter(
        and_(User.deleted == False)
        ).limit(page_size).offset((page-1)*page_size).all()
    return Response(data, 200, "Users retrieved successfully.", False)

@router.post("/add", response_description="User data added into the database")
async def add_user(user_req: UserRequest): 
    new_user = User()
    new_user.first_name = user_req.first_name
    new_user.last_name = user_req.last_name
    new_user.created_by = user_req.created_by

    session = database.get_db_session(engine)
    session.add(new_user)
    session.flush()

    # get id of the inserted user
    session.refresh(new_user, attribute_names=['id'])
    data = {"user_id": new_user.id}
    session.commit()
    session.close()
    return Response(data, 200, "User added successfully.", False)

@router.get("/{user_id}")
async def read_user_by_id(user_id: str):
    session = database.get_db_session(engine)
    response_message = "User retrieved successfully"
    data = None
    try:
        data = session.query(User).filter(
            and_(User.id == user_id, User.deleted == False)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "User Not found"
    error = False
    return Response(data, 200, response_message, error)

@router.put("/update")
async def update_user(user_update_req: UserUpdateRequest):
    user_id = user_update_req.user_id
    session = database.get_db_session(engine)

    try:
        is_user_update = session.query(User).filter(User.id == user_id).update({
            User.first_name: user_update_req.first_name,
            User.last_name: user_update_req.last_name,
            User.updated_by: user_update_req.updated_by,
        }, synchronize_session=False)
        
        session.flush()
        session.commit()
        response_msg = "User updated successfully"
        response_code = 200
        error = False
        if is_user_update == 1:
            # After successful update, retrieve updated data from db
            data = session.query(User).filter(
                User.id == user_id).one()

        elif is_user_update == 0:
            response_msg = "User not updated. No User found with this id :" + \
                str(user_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error in update_user ", str(ex))



