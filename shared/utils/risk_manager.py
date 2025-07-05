def check_clean_displacement(ob, df):
    #  Complex logic here...
    print("Check displacement: Passed")
    return 1

def check_unmitigated(ob, history):
    # Complex logic here...
    print("Checking mitigation: Passed")
    return 1

def check_liquidity_sweep(ob, df):
    # Complex logic here...
    print("Checking liquidity sweep: Failed")
    return 0 # This rule fails

def check_fibonacci_zone(ob, df):
    print("Checking fibonacci zone: Passed")
    return 1

def check_clean_structure(ob, df):
    print("Checking structure: Passed")
    return 1

def check_bos_impulse(ob, bos_level):
    # Complex logic here...
    print("Checking BOS impulse: Passed")
    return 1

PERFECT_OB_RULES = [
    check_clean_displacement,
    check_unmitigated,
    check_bos_impulse,
    check_fibonacci_zone,
    check_clean_structure,
    check_bos_impulse
]

def calculate_lot_size(balance, risk_percent, sl_pips, symbol):
    risk_amount = balance * (risk_percent / 100)

    # Get symbol info for contract size and tick value
    symbol_info = None # symbol info comes from function call
    if symbol_info is None:
        return 0.01 # Default small lot size
    
    # For synthetics like Step Index, point value calculation might be different 
    # Let's assume a direct pip value for simplicity
    # 1 pip for Step Index = 0.1
    pip_value = 0.1
    sl_monetary = sl_pips * pip_value

    lot_size = risk_amount / (sl_monetary) * symbol_info.volume_step 
    lot_size = round(lot_size / symbol_info.volume_step) * symbol_info.volume_step 

    return max(lot_size, symbol_info.volume_min)


def is_perfect_ob(df, ob, bos_type, bos_level):
    """
    Evaluates an Order Block by running it through a list of rule functions.
    """
    if ob is None:
        return False
    
    # Dummy data for the example
    ob_data = {"price": 123}
    df_data = {}

    # Use a generator expression with sum() for a concise, efficient calculation
    score = sum(rule(ob_data, df_data) for rule in PERFECT_OB_RULES)S

    print(f"\nFinal Score: {score}/{len(PERFECT_OB_RULES)}") 

    acceptance_threshold = 5
    if score >= acceptance_threshold:
        print("✅ OB is PERFECT. Trade accepted.")
        return True
    else:
        print("❌ OB is weak. Trade rejected.")
        return False
