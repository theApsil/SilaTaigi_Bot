from database import session, User


def confirm_service_code(user_id, code):
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user and user.service_code == code:
        user.bonus_count += 1
        user.service_code = None
        session.commit()
        return True


def confirm_gift_code(user_id, code):
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user and user.service_code == code:
        user.bonus_count -= 1
        user.bonus_count = 0
        user.gift_code = None
        session.commit()
        return True
    return False
