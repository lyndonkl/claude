# The equity value bridge (from operating assets to value per share)

**Core idea:** A DCF gives you the value of operating assets. That is not the value of a share. Between the two lies a chain of adjustments, and each link hides a decision that can move value by double digits. You add what the cash flows did not capture: cash, cross holdings, other non-operating assets. You subtract every non-equity claim: debt, unfunded obligations, contingent liabilities, minority interests. You subtract the value of options on the equity. Only then do you divide, and only by *actual* shares outstanding. Damodaran's warning about this stage — "the trouble starts after you tell me you are done" — is literal. Most valuation disputes between competent analysts happen here, not in the cash-flow forecast.

**Formulas:**
```
  Value of operating assets            (DCF of FCFF at the cost of capital)
+ Cash and marketable securities
+ Value of cross holdings
+ Value of other non-operating assets
= Value of firm
− Value of debt                        (market value, not book)
− Other claims (pension underfunding, contingent liabilities, minority interests)
= Value of equity
− Value of equity options (employee options, warrants, conversion options)
= Value of common stock
÷ Number of shares outstanding         (actual, not diluted)
= Value per share
```

**Reference data — the open question at each link:**

| Step | Question you must answer |
|---|---|
| Value of operating assets | Should a real-option premium be added on top of the DCF? |
| + Cash | Is any of it operating cash? Discount or premium? → [[cash-in-valuation]], [[marginal-value-of-cash]] |
| + Cross holdings | How are they valued, and what if they are private? → [[cross-holdings]] |
| + Other assets | What other assets exist? How are under-utilized assets handled? → [[other-non-operating-assets]] |
| = Value of firm | Discount for opacity/complexity? Premium for synergy or brand? → [[complexity-discount]] |
| − Debt | What counts as debt? Book or market value? Pensions, health care, contingent liabilities, minority interests? → [[defining-debt-for-cost-of-capital]], [[debt-and-other-claims-in-the-bridge]] |
| = Value of equity | Control premium or discount? Distress discount? |
| − Equity options | Vested or non-vested? Valued how? → [[employee-option-per-share-approaches]], [[valuing-employee-options]] |
| ÷ Shares | Primary or diluted? |
| = Value per share | Illiquidity/marketability discount? Minority-interest discount? |

**Procedure:**
1. Confirm the DCF valued operating assets only. Interest income from cash must be out of the cash flows, and the beta must be an operating-asset beta.
2. Add the cash balance, adjusted for any discount or premium you can defend.
3. Value each cross holding and add the parent's proportional share. Remove any consolidated value that belongs to outside shareholders.
4. Add non-operating assets whose earnings are *not* already in the cash flows — never brand value, never goodwill.
5. Apply a complexity or opacity adjustment if warranted, in the cash flows, the discount rate, the growth assumptions, or as a final haircut. Pick one route; do not stack them.
6. Subtract the market value of all interest-bearing debt and leases.
7. Subtract other claims: pension and health-care underfunding, the expected value of contingent liabilities, and the value of minority interests in consolidated subsidiaries.
8. Subtract the value of employee options, warrants and conversion options.
9. Divide by actual shares outstanding. If you already subtracted option value, using diluted shares double-counts.
10. Apply per-share discounts (illiquidity, minority stake) last, and only when the buyer's position justifies them.

**Worked example (Heineken, September 2019, € millions):** the DCF produced a PV of ten years of cash flows of 15,300.85 plus a terminal-value PV of 36,390.85, so operating assets = **51,691.19**. The bridge then runs: − debt 19,709.52 − minority interests 1,069.00 + cash 1,751.60 + non-operating assets 1,401.00 = **equity 34,065.26**. Divided by 571.10 shares → **€59.65 per share**, against a market price of €93.25. The model value is only 56.33% of price. Note that two of the five bridge items (minority interests and non-operating assets) come from outside the DCF entirely.

**Determinism:**
- DETERMINISTIC: the arithmetic of the bridge once each component is estimated. Given operating-asset value, cash, holdings, debt, other claims, option value and share count, value per share computes exactly.
- JUDGMENT: every component estimate. Which cash is operating; what the holdings are worth; whether complexity deserves a discount; what counts as debt; the probability and size of contingent liabilities; option valuation inputs. Each requires reading the notes to the financial statements, not just the face of the balance sheet.

**Pitfalls:**
- Double-counting: subtracting option value *and* dividing by diluted shares; or adding brand value on top of cash flows that already reflect brand pricing power.
- Subtracting book debt from a market-based enterprise value.
- Forgetting minority interests in a consolidated firm value, which credits shareholders with 100% of a subsidiary they only partly own.
- Adding goodwill as an asset. It is an accounting residual, not an asset.
- Stacking adjustments for the same risk — a complexity discount in the discount rate *and* a haircut on the final value.

**Sources:**
- valpacket1spr21 p.218-219
- valpacket1spr20 p.214-215
- valpacket1spr21 p.203 (Heineken bridge to value per share)

**Related:** [[cash-in-valuation]], [[marginal-value-of-cash]], [[cross-holdings]], [[other-non-operating-assets]], [[complexity-discount]], [[defining-debt-for-cost-of-capital]], [[debt-and-other-claims-in-the-bridge]], [[employee-option-per-share-approaches]], [[dcf-model-choice-framework]], [[illiquidity-discount]], [[control-premium]]
