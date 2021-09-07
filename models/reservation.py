from sqlmodel import Field, SQLModel


# TODO: E-mail validation, sqlalchemy probably supports it
# and there is no doc in SQLModel as of yet, so will check on backend-side before writing into db
# but the hard constraint should be added in future as SQLModel matures
class Reservation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
