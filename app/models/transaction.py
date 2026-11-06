from sqlalchemy import(
    Column , 
    Integer , 
    String ,
    Numeric , 
    DateTime , 
    ForeignKey , 
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from app.core.database import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True , index=True)


    # linking transactions table to email_records table
    email_record_id = Column(
        Integer,
        ForeignKey("email_records.id"),
        nullable = False , 
        index=True
    )

    payee = Column(String(255) , nullable=False)
    amount = Column(Numeric(12 , 2) , nullable=False)
    currency = Column(String(3) , default="INR" , nullable=False)
    channel = Column(String(30),nullable=True)
    transaction_id = Column(String(100) , nullable=False)
    status = Column(String(30) , nullable=False)

    email_record = relationship(
        "EmailRecord" , 
        back_populates="transactions"
    )

    #prevventing Duplicatess

    __table_args__ = (

        UniqueConstraint(
            "transaction_id",
            name="uq_transaction_id"
        ),
    )