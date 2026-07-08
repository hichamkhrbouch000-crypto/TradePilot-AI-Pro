# داخل دالة run_trading_engine، بدلاً من الطباعة فقط:
decision = {
    "timestamp": datetime.datetime.now().isoformat(),
    "price": price,
    "rsi": rsi,
    "risk_decision": risk_data['is_valid'],
    "rejection_reason": reason if not is_valid else "None",
    "rr_ratio": risk_data.get('rr_ratio', 0),
    "volatility_atr": atr # سنضيف حساب ATR هنا لاحقاً
}
log_decision(decision)
