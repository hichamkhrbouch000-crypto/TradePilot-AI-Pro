import pandas as pd

def generate_report(file_path='trade_analytics.csv'):
    try:
        df = pd.read_csv(file_path)
        
        # 1. إحصائيات عامة
        total_signals = len(df)
        approved = df[df['risk_decision'] == True]
        rejected = df[df['risk_decision'] == False]
        
        print("--- تقرير الأداء التحليلي ---")
        print(f"إجمالي الإشارات: {total_signals}")
        print(f"الإشارات المقبولة: {len(approved)} ({len(approved)/total_signals*100:.1f}%)")
        print(f"الإشارات المرفوضة: {len(rejected)} ({len(rejected)/total_signals*100:.1f}%)")
        
        # 2. تحليل أسباب الرفض
        print("\n--- أسباب الرفض الأكثر تكراراً ---")
        print(rejected['rejection_reason'].value_counts())
        
        # 3. تحليل جودة الصفقات
        if not approved.empty:
            print("\n--- تحليل جودة الصفقات المقبولة ---")
            print(f"متوسط نسبة المخاطرة للعائد (RR): {approved['rr_ratio'].mean():.2f}")
            
    except Exception as e:
        print(f"لا توجد بيانات كافية للتحليل حالياً: {e}")

if __name__ == "__main__":
    generate_report()

