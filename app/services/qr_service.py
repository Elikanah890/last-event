import qrcode
import io
import base64
from app.models.invitation_model import Invitation

class QRService:
    @staticmethod
    def generate_qr_code(data: str) -> str:
        """
        Generate a QR code and return as base64 string
        """
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{qr_base64}"

    @staticmethod
    def validate_qr(invitation: Invitation, token: str) -> bool:
        """
        Simple validation for production:
        - check token matches
        - check invitation is not already scanned (logic in attendance service)
        """
        return invitation.guest.unique_token == token
