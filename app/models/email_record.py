
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class EmailRecord(Base):

    __tablename__ = "email_records"

    id = Column(Integer, primary_key=True, index=True)

    gmail_message_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    sender = Column(String(255), nullable=True)
    subject = Column(String(500), nullable=True)

    received_at = Column(DateTime(timezone=True), nullable=True)

    body_text = Column(Text, nullable=True)

    processing_status = Column(
        String(30),
        default="pending",
        nullable=False
    )

    transactions = relationship(
        "Transaction",
        back_populates="email_record"
    )
