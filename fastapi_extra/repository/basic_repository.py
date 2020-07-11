from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel

from mongoengine import Document

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    createSchemaType: Type[Union[CreateSchemaType, Dict[str, Any]]]
    updateSchemaType: Type[Union[UpdateSchemaType, Dict[str, Any]]]

    def __init__(self, document: Type[ModelType],
                 createSchemaType: Type[Union[CreateSchemaType, Dict[str, Any]]] = Dict[str, Any],
                 updateSchemaType: Type[Union[UpdateSchemaType, Dict[str, Any]]] = Dict[str, Any]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `document`: A mongoengine Document class
        * `schema`: A Pydantic model (schema) class
        """
        self.document = document

        self.createSchemaType = createSchemaType
        self.updateSchemaType = updateSchemaType

    def getById(self, _id: str) -> Optional[ModelType]:
        return self.document.objects(id=_id).get()

    def getByIds(self, _ids: List[str]):
        return self.document.objects(id__in=_ids)

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return self.document.objects[skip:limit]

    def create(self, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        db_obj = self.document(**obj_in)  # type: ignore
        db_obj.save()
        return db_obj

    def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if not isinstance(db_obj, self.document):
            raise Exception("object to update have different type")

        db_obj.update(**obj_in)
        return db_obj

    def remove(self, _id: int) -> ModelType:
        obj: ModelType
        obj = self.document.objects(id=_id).get()
        obj.delete()
        return obj
