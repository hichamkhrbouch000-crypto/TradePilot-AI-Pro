# أضف هذه الدالة داخل strategy.py
def should_trade(signal, current_position):
    """يحدد ما إذا كان يجب الدخول في صفقة"""
    if signal == "BUY" and current_position == 0:
        return True
    elif signal == "SELL" and current_position > 0:
        return True
    return False
