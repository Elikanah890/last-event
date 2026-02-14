from app.models.guest_model import Guest
from app.models.invitation_model import Invitation
from app.database import SessionLocal
from app.services.qr_service import QRService
from app.core.config import get_settings
from sqlalchemy.orm import Session

settings = get_settings()

class InvitationService:
    @staticmethod
    def create_invitation(db: Session, guest: Guest) -> Invitation:
        """
        Create invitation card with QR code
        """
        # Generate QR code using the guest's unique token
        qr_data = guest.unique_token
        qr_code_base64 = QRService.generate_qr_code(qr_data)

        # Generate the invitation card link from environment variable
        card_link = f"{settings.INVITATION_BASE_URL}/{guest.unique_token}"

        # Create invitation record
        invitation = Invitation(
            guest_id=guest.id,
            card_link=card_link,
            qr_code_path=qr_code_base64,
            sent_status=False
        )
        db.add(invitation)
        db.commit()
        db.refresh(invitation)
        return invitation

    @staticmethod
    def mark_sent(db: Session, invitation: Invitation):
        """
        Mark invitation as sent after delivery (email/WhatsApp)
        """
        invitation.sent_status = True
        db.commit()
        db.refresh(invitation)
