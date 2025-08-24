from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from db import DB


class CreateTableInput(BaseModel):
    database: dict
    new_table_name: str
    attrs: list[str]


class CreateNoteInput(BaseModel):
    database: dict
    table_name: str
    new_note_name: str
    note_content: dict


class DeleteTableInput(BaseModel):
    database: dict
    table_name: str


class DeleteNoteInput(BaseModel):
    database: dict
    table_name: str
    note_name: str


class SaveTreeInput(BaseModel):
    database: dict
    filename: Optional[str] = 'db.json'


class FileNameModel(BaseModel):
    filename: str


class DBModel(BaseModel):
    database: dict


app = FastAPI(
    name='Data Base Manipulator',
    version='1.0'
)


@app.get('/health')
async def health():
    return {'status': 200}


@app.post('/create-database', response_model=DBModel)
async def create_database():
    """
    Initialising a new database

    :return: DBModel
    """
    try:
        db = DB()
        return DBModel(database=db.to_dict(db.tree.root))

    except HTTPException as e:
        print('Server error occurred: ', e)
    except Exception as e:
        print('Error occurred: ', e)


@app.post('/create-table', response_model=DBModel)
async def create_table(request: CreateTableInput):
    """
    Creates Table in retrieved database instance

    :param request: CreateTableInput, database, new_table_name, attrs
    :return: DBModel, database
    """
    try:
        database = DB(DB.dict_to_tree(request.database))
        database.insert_table(request.new_table_name, request.attrs)
        return DBModel(database=database.to_dict(database.tree.root))

    except HTTPException as e:
        print('Server error occurred: ', e)
    except Exception as e:
        print('Error occurred: ', e)


@app.post('/create-note', response_model=DBModel)
async def create_note(request: CreateNoteInput):
    """
    Creates new Table Note in retrieved database instance

    :param request: CreateNoteInput, database, table_name, new_note_name, note_content
    :return: DBModel, database
    """
    try:
        database = DB(DB.dict_to_tree(request.database))
        table = database.get_table(request.table_name)
        table.insert(request.new_note_name, request.note_content)
        return DBModel(database=database.to_dict(database.tree.root))

    except HTTPException as e:
        print('Server error occurred: ', e)
    except Exception as e:
        print('Error occurred: ', e)


@app.post('/delete-table', response_model=DBModel)
async def delete_table(request: DeleteTableInput):
    """
    Deleting new Table in retrieved database instance

    :param request: DeleteTableInput, database, table_name
    :return: DBModel, database
    """
    try:
        database = DB(DB.dict_to_tree(request.database))
        database.delete_table(request.table_name)
        return DBModel(database=database.to_dict(database.tree.root))

    except HTTPException as e:
        print('Server error occurred: ', e)
    except Exception as e:
        print('Error occurred: ', e)


@app.post('/delete-note', response_model=DBModel)
async def delete_note(request: DeleteNoteInput):
    """
    Deleting new Table Note in retrieved database instance

    :param request: DeleteNoteInput, database, table_name, note_name
    :return: DBModel, database
    """
    try:
        database = DB(DB.dict_to_tree(request.database))
        table = database.get_table(request.table_name)
        table.delete(request.note_name)
        return DBModel(database=database.to_dict(database.tree.root))

    except HTTPException as e:
        print('Server error occurred: ', e)
    except Exception as e:
        print('Error occurred: ', e)


@app.post('/save-tree-json', response_model=FileNameModel)
async def save_tree_json(request: SaveTreeInput):
    """
    Save retrieved database instance in JSON file

    :param request: SaveTreeInput, database, filename
    :return: FileNameModel, filename
    """
    try:
        database = DB(DB.dict_to_tree(request.database))
        database.to_json(request.filename)
        return FileNameModel(filename=request.filename)

    except HTTPException as e:
        print('Server error occurred: ', e)
    except Exception as e:
        print('Error occurred: ', e)


@app.post('/upload-tree-json', response_model=DBModel)
async def upload_tree_json(request: FileNameModel):
    """
    Save retrieved database instance in JSON file

    :param request: DBModel, filename
    :return: DBModel, database
    """
    try:
        db = DB.read_json(request.filename)
        return DBModel(database=db.to_dict(db.tree.root))

    except HTTPException as e:
        print('Server error occurred: ', e)
    except Exception as e:
        print('Error occurred: ', e)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app, host='0.0.0.0', port=8000
    )