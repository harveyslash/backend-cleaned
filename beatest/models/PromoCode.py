from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm.exc import NoResultFound

from Sugar import Dictifiable
from extensions import db
from sqlalchemy import and_
from sqlalchemy.orm import relationship, contains_eager


class PromoCode(Dictifiable, db.Model):
    __tablename__ = 'promo_code'

    id = Column(Integer, Sequence('promoCode_id_seq'), primary_key=True)
    promo_code = Column(String(50), unique=True)
    promo_value = Column(Integer)
    promo_used = Column(Integer)
    promo_max_usage = Column(Integer)
    promo_valid = Column(Integer)
    promo_multiple_use = Column(Integer)

    orders = relationship('Order', back_populates='promo_code')

    @staticmethod
    def consume_promo_code(promo_code: str, user_id: int,
                           should_flush: bool = True):
        """
        Consume a promo code.

        A promo code is consumable iff :
            * promo_valid = True
            * In case of single usage,it is not already used
            * In case of multi usage, it hasnt reached max_usage

        If any of these conditions fail, this function raises a
        ValueError

        If no errors were encountered , this updates
        the promocode promo_used = True & increments the promo_usage by 1.

        It then optionally performs a flush to the database.

        :param promo_code:
        :param should_flush: If true, db flush will be performed, else it wont
                             be
        :return: a tuple with (promo code value & promo code id)
        """
        from models import Order
        from models.Order import OrderStatusTypes
        try:
            p_c = (PromoCode.query
                   .outerjoin(Order, and_(Order.promo_code_id ==
                                          PromoCode.id,
                                          Order.user_id == user_id,
                                          Order.status != OrderStatusTypes.cancelled))
                   .options(contains_eager(PromoCode.orders))
                   .filter(PromoCode.promo_code == promo_code)
                   .one())

            if not p_c.promo_valid:
                raise ValueError("Promo code not valid")

            if p_c.promo_used:
                if p_c.promo_multiple_use:

                    # if promo code has reached max usage
                    if p_c.promo_used >= p_c.promo_max_usage:
                        raise ValueError("Promo Max usage reached")
                else:  # if promo code is not multi usage, and already used
                    raise ValueError("Promo Already used and not multi usage")

            # uncomment below if a single user can use same promo code just
            # once
            # if len(p_c.orders) > 0:
            #     raise ValueError("PromoCode Already Consumed by User")

            p_c.promo_used += 1

            if should_flush:
                db.session.flush()

            return p_c.promo_value, p_c.id
        except NoResultFound:
            raise ValueError("PromoCode doesnt exist")
