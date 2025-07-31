#!/usr/bin/env python3
def fix_bot_text():
    with open('bulletproof_usdc_bot.py', 'r') as f:
        content = f.read()
    
    replacements = {
        "'vip_membership_choose text'": "'VIP MEMBERSHIP - CHOOSE YOUR PLAN'",
        "'available_packages text'": "'Available Packages:'",
        "'weekly_vip_plan text'": "'Weekly VIP - $25 USDC (7 days)'",
        "'basic_trading_signals text'": "'Basic trading signals'",
        "'market_updates text'": "'Market updates'",
        "'weekly_group_access text'": "'Weekly group access'",
        "'monthly_vip_plan text'": "'Monthly VIP - $80 USDC (30 days)'",
        "'monthly_group_access text'": "'Monthly group access'",
        "'quarterly_vip_plan text'": "'Quarterly VIP - $200 USDC (90 days)'",
        "'elite_signals_analysis text'": "'Elite signals & analysis'",
        "'all_plans_include text'": "'All Plans Include:'"
    }
    
    for old_text, new_text in replacements.items():
        if old_text in content:
            content = content.replace(old_text, new_text)
            print(f"Fixed: {old_text}")
    
    with open('bulletproof_usdc_bot.py', 'w') as f:
        f.write(content)
    
    print("All fixes applied!")

if __name__ == "__main__":
    fix_bot_text()
