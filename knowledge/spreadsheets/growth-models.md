# Damodaran growth-model spreadsheets

Source files (2020 vintage, .xls — computed values only; all computation logic below was reconstructed from labels, layout, and numeric verification unless marked "verbatim"). Every reconstructed formula was checked numerically against the values in the sheet to at least 5 significant digits.

---

### growthbreakdown.xls

**Purpose:** Decomposes a firm's market value into (a) value of assets in place — a no-growth perpetuity of current after-tax operating income — and (b) value added by future growth. It then compares the *price* the market is paying for growth against the *intrinsic value* of that growth. It also splits common multiples (P/E, P/BV, EV/Sales, EV/Invested Capital) into assets-in-place and growth components, both at market prices and at intrinsic value. Damodaran uses it in "big-picture" lectures to show how much of a high-flyer's price is growth, and (via Goal Seek) to back out the growth rate implied by the current market cap. Sheets: `Input page` (the model), `Industry averages` (reference data), `Cost of capital worksheet` (standalone helper).

**Inputs (`Input page` sheet):**

| Label | Cell | Example value |
|---|---|---|
| Market Capitalization | B3 | 70000 |
| Book value of equity — this year / last year | B5 / C5 | 5228 / 4162 |
| Total Debt Outstanding — this year / last year | B6 / C6 | 1215 / 1317 |
| Cash & Marketable Securities — this year / last year | B7 / C7 | 1512 / 1785 |
| Revenues — this year / last year | B9 / C9 | 3711 / 1974 |
| Operating income (EBIT) — this year / last year | B10 / C10 | 1695 / 1032 |
| Effective tax rate | B11 | 0.40 |
| Net Income | B12 | 900 |
| Expected growth rate in operating income | B14 | 0.1142 |
| Return on Invested capital on growth | B15 | 0.275311 (defaults to computed ROIC in E5) |
| Length of growth period (years, max 10 for the detail table) | B16 | 10 |
| Cost of equity | B18 | 0.125 |
| Cost of capital | B19 | 0.1142 |
| Riskfree rate | B20 | 0.02 |

Instructions embedded in sheet (D14:D18, verbatim): to find the market-implied growth rate, use Excel Goal Seek to set B24 (value added by growth) equal to B28 (price paid for growth) by changing B14 (expected growth). In the current state B14 has already been goal-seeked (that is why cost of capital 0.1142 == growth rate 0.1142 is coincidental-looking; B19 is an independent input).

**Inputs (`Cost of capital worksheet` — standalone helper, NOT linked to the Input page in this saved copy; its numbers are a leftover example):**

| Label | Cell | Example |
|---|---|---|
| Number of Shares outstanding | B4 | 2333.903 |
| Current Market Price per share | B5 | 38 |
| Unlevered beta (from industry-average sheet col G) | B7 | 1.52 |
| Riskfree Rate | B8 | 0.02 |
| Equity Risk Premium | B9 | 0.06 |
| Book Value of Straight Debt | B12 | 272 |
| Interest Expense on Debt | B13 | 10 |
| Average Maturity | B14 | 0 |
| Pre-tax Cost of Debt | B15 | 0.0365 |
| Tax Rate | B16 | 0.35 |
| Book Value / Interest Expense / Maturity / Market Value of Convertible Debt | B18–B21 | all 0 |
| Debt value of operating leases | B23 | 816.9073 |
| Number of Preferred Shares / Price / Annual Dividend per Share | B26–B28 | 0 / 70 / 5 |

**Logic (`Input page`):**

Derived diagnostics (all inferred, numerically verified):
- `ROE (E4) = Net Income / BV equity_last_year` = 900/4162 = 0.216242
- Invested capital (last year) `IC_last = BVE_last + Debt_last − Cash_last` = 4162+1317−1785 = 3694; this-year `IC = 5228+1215−1512 = 4931`
- After-tax operating income `EBIT(1−t) = 1695×(1−0.40) = 1017`
- `ROIC (E5) = EBIT(1−t) / IC_last` = 1017/3694 = 0.275311
- `Net margin (E6) = NI/Revenues` = 0.242522
- `"Pre-tax operating margin" (E7)` — despite the label, it is computed **after-tax**: `EBIT(1−t)/Revenues` = 1017/3711 = 0.274050
- `D/E book (E8) = Debt/BVE` = 0.232402; `D/E market (E9) = Debt/MktCap` = 0.017357
- Revenue growth (E10) = 3711/1974 − 1 = 0.879939; EBIT growth (E11) = 1695/1032 − 1 = 0.642442

No-growth scenario (rows 40–50, inferred):
- Reinvestment rate = 0; FCFF_t = EBIT(1−t) = 1017 every year, forever.
- `Value of assets in place (B23) = EBIT(1−t) / cost_of_capital` = 1017/0.1142 = 8905.429. (The detail table computes the same thing as 10 years of flat 1017 discounted at WACC plus terminal value 1017/0.1142 in year 10 — identical result.)

Growth scenario (rows 52–62, inferred, all verified):
- High-growth reinvestment rate `RR_hg (B53) = g / ROIC_growth` = 0.1142/0.275311 = 0.414803 (sheet comment verbatim: "Expected growth rate in high growth rate/ Return on Invested capital in high growth")
- Stable reinvestment rate `RR_st (B54) = g_stable / ROC_stable = riskfree_rate / cost_of_capital` = 0.02/0.1142 = 0.175131 (sheet comment verbatim: "Assume stable growth rate = riskfree rate; return on capital in stable growth = cost of capital")
- Year 0: AT operating income = 1017; Reinvestment_0 = 1017 × RR_hg = 421.855; FCFF_0 = **−421.855** (the firm must reinvest immediately to generate the growth; this year-0 outflow is included UNDISCOUNTED in the value)
- Years t = 1..n−1: `ATOI_t = ATOI_0 × (1+g)^t`; `Reinv_t = ATOI_t × RR_hg`; `FCFF_t = ATOI_t − Reinv_t`
- Year n (=10): `Reinv_n = ATOI_n × RR_st` (switches to the stable rate in the final high-growth year); FCFF_n = ATOI_n × (1 − RR_st)
- Terminal year: `ATOI_{n+1} = ATOI_n × (1+rf)` = 2998.834×1.02 = 3058.811; `FCFF_{n+1} = ATOI_{n+1} × (1 − RR_st)` = 2523.117
- `Terminal Value (B61) = FCFF_{n+1} / (WACC − rf)` = 2523.117/(0.1142−0.02) = 26784.686
- `Value today (B62) = FCFF_0 + Σ_{t=1..n} FCFF_t/(1+WACC)^t + TV/(1+WACC)^n` = −421.855 + 15278.736 = 14856.881

Value decomposition:
- `Value added by future growth (B24) = B62 − B50` = 14856.881 − 8905.429 = 5951.452 (also shown in B65)
- `Intrinsic enterprise value (B25) = B23 + B24`; `Intrinsic equity value (B26) = B25 + Cash − Debt` = 14856.881+1512−1215 = 15153.881
- `Market enterprise value (E24) = MktCap + Debt − Cash` = 70000+1215−1512 = 69703
- `Price you are paying for growth (B28) = E24 − B23` = 69703 − 8905.429 = 60797.571
- `Price of growth / Value of growth (B30) = B28/B24` = 10.2156

Breakdown of multiples (rows 34–37; each row has Actual{Total, Assets-in-place, Growth} and Intrinsic{Total, Assets-in-place, Growth}). Let `EquityAIP = B23 + Cash − Debt` = 9202.429 (equity value if no growth) — inferred, verified:
- P/E: Actual total = MktCap/NI = 77.778; AIP = EquityAIP/NI = 10.2249; Growth = Total − AIP. Intrinsic total = B26/NI = 16.8376; intrinsic AIP = same 10.2249; intrinsic growth = B24/NI = 6.6127
- P/BV: same numerators divided by BVE (5228): 13.3894 / 1.76022 / 11.6292 and 2.8986 / 1.76022 / 1.13838
- EV/Sales: Actual total uses **market equity, not EV** (quirk): MktCap/Revenues = 18.8628; AIP = B23/Revenues = 2.39974; Intrinsic total = B25/Revenues = 4.00347; intrinsic growth = B24/Revenues = 1.60373
- EV/Invested Capital: divide the same by IC = 4931: Actual total = MktCap/IC = 14.1959 (again market equity); AIP = B23/IC = 1.80601; Intrinsic total = B25/IC = 3.01295; growth = B24/IC = 1.20695

**Logic (`Cost of capital worksheet`, inferred, verified):**
- MV equity = shares × price = 2333.903×38 = 88688.314
- MV straight debt = `Interest × [1−(1+kd)^−M]/kd + BV/(1+kd)^M`; with M=0 this returns BV = 272
- Straight-debt value in convertible = same bond-pricing formula on convertible coupon/BV (0 here); equity in convertible = market value of convertible − straight-debt value
- Total debt D = straight + straight-in-convertible + operating-lease debt = 272+0+816.907 = 1088.907
- Preferred = shares × price = 0
- `Levered beta (C35) = unlevered_beta × (1 + (1−tax) × D/E)` = 1.52×(1+0.65×1088.907/88688.314) = 1.532131
- Cost of equity = rf + levered_beta × ERP = 0.02+1.532131×0.06 = 0.111928; after-tax cost of debt = 0.0365×(1−0.35) = 0.023725; cost of preferred = dividend/price = 5/70 = 0.071429
- `WACC (E40) = Σ weight_i × cost_i` (market-value weights of equity, debt, preferred) = 0.110858

**Reference data (`Industry averages` sheet, 100 industries, verbatim):** This is pure lookup data. The user sources inputs from it (unlevered beta, margins, ROC). Nothing on the Input page references it by formula in this copy. Full table below; floats rounded to 4 decimals. Column headers are copied verbatim from row 1.


| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 31 | 0.1676 | 0.1027 | 0.1054 | 0.1073 | 1.7499 | 2.0229 | 0.1409 | 1.0129 | 0.0587 | 0.3020 | 0.1090 | 1.4200 | 1.1385 | 7.8995 | 11.0854 | 1.8328 | 27.3934 |
| Aerospace/Defense | 64 | 0.0941 | 0.1016 | 0.1853 | 0.2072 | 1.0324 | 1.0953 | 0.0849 | 0.6132 | 0.0337 | 0.2042 | 0.0717 | 2.5300 | 0.9281 | 7.4053 | 9.1378 | 2.7526 | 34.3997 |
| Air Transport | 36 | 0.0877 | 0.0878 | 0.1645 | 0.2054 | 1.1020 | 1.2148 | 0.0921 | 0.6480 | 0.0337 | 0.1956 | 0.0780 | 2.4000 | 1.7758 | 12.9087 | 20.2206 | 8.2394 | 156.1358 |
| Apparel | 57 | 0.0583 | 0.1097 | 0.1402 | 0.1608 | 1.2214 | 1.2986 | 0.0971 | 0.8882 | 0.0437 | 0.1553 | 0.0861 | 1.8500 | 1.1882 | 8.6547 | 10.8320 | 2.4572 | 20.5636 |
| Auto Parts | 51 | 0.2394 | 0.0649 | 0.1582 | 0.1899 | 1.5857 | 1.6989 | 0.1213 | 0.8058 | 0.0437 | 0.2166 | 0.1007 | 3.1800 | 0.5872 | 6.1924 | 9.0527 | 2.0753 | 15.8271 |
| Automotive | 12 | 0.0166 | 0.0699 | 0.0696 | 0.2407 | 0.9557 | 1.5888 | 0.1147 | 0.6891 | 0.0387 | 0.5737 | 0.0622 | 1.4100 | 0.7269 | 5.8127 | 10.3972 | 1.0466 | 10.8441 |
| Bank | 426 | 0 | NA | NA | 0.1597 | 0.3756 | 0.7692 | 0.0652 | 0.6115 | 0.0337 | 0.6095 | 0.0378 | NA | NA | 4.3690 | 4.3690 | 0.8514 | 16.6871 |
| Bank (Midwest) | 45 | 0 | NA | NA | 0.1777 | 0.7294 | 0.9329 | 0.0750 | 0.5560 | 0.0337 | 0.3731 | 0.0546 | NA | NA | 4.5685 | 4.5685 | 1.2936 | 34.1336 |
| Beverage | 34 | -0.0059 | 0.2045 | 0.1295 | 0.1914 | 0.7659 | 0.8828 | 0.0720 | 0.6605 | 0.0387 | 0.2096 | 0.0618 | 0.8300 | 3.0267 | 12.0355 | 14.8010 | 3.6117 | 22.5081 |
| Biotechnology | 158 | 0.2694 | -0.0779 | -0.1333 | 0.0249 | 1.1585 | 1.0296 | 0.0809 | 1.1311 | 0.0587 | 0.1188 | 0.0755 | 0.9700 | 4.4910 | NA | NA | 3.1946 | 18.8722 |
| Building Materials | 45 | 0.0282 | 0.0417 | 0.0258 | 0.1117 | 0.8873 | 1.5044 | 0.1096 | 0.7882 | 0.0387 | 0.4854 | 0.0677 | 0.8200 | 1.2195 | 10.9865 | 29.2252 | 0.9934 | 265.1483 |
| Cable TV | 21 | 0.0153 | 0.1958 | 0.0880 | 0.2735 | 0.9770 | 1.3707 | 0.1015 | 0.5077 | 0.0337 | 0.4050 | 0.0686 | 0.7100 | 2.2058 | 6.2491 | 11.2673 | 2.3090 | 12.6627 |
| Chemical (Basic) | 16 | 0.3340 | 0.1209 | 0.1366 | 0.2090 | 1.2377 | 1.3600 | 0.1008 | 0.4927 | 0.0287 | 0.2147 | 0.0829 | 1.4300 | 1.5233 | 8.8968 | 12.5983 | 2.6447 | 12.1664 |
| Chemical (Diversified) | 31 | 0.0921 | 0.1320 | 0.1381 | 0.2173 | 1.3919 | 1.5142 | 0.1102 | 0.5631 | 0.0337 | 0.1828 | 0.0937 | 1.4800 | 1.6215 | 8.9486 | 12.2837 | 2.9609 | 12.9402 |
| Chemical (Specialty) | 70 | 0.2569 | 0.1110 | 0.1225 | 0.1758 | 1.1467 | 1.2755 | 0.0957 | 0.7160 | 0.0387 | 0.1746 | 0.0831 | 1.5600 | 1.5604 | 9.8374 | 14.0554 | 3.0762 | 15.6341 |
| Coal | 20 | 0.1691 | 0.1594 | 0.1526 | 0.1275 | 1.3190 | 1.5250 | 0.1108 | 0.5552 | 0.0337 | 0.2242 | 0.0905 | 1.2200 | 1.7754 | 7.3394 | 11.1395 | 2.7733 | 12.0893 |
| Computer Software | 184 | 0.1488 | 0.3135 | 0.4506 | 0.1227 | 1.1821 | 1.0436 | 0.0817 | 0.8203 | 0.0437 | 0.0697 | 0.0779 | 1.8300 | 3.0743 | 8.6352 | 9.8064 | 3.7355 | 68.5636 |
| Computers/Peripherals | 87 | 0.1093 | 0.1415 | 0.3209 | 0.1177 | 1.3325 | 1.2976 | 0.0971 | 0.9769 | 0.0487 | 0.0928 | 0.0908 | 2.9600 | 1.3943 | 8.1143 | 9.8532 | 3.9424 | 38.6556 |
| Diversified Co. | 107 | 0.1724 | 0.1409 | 0.0801 | 0.1555 | 0.7140 | 1.1403 | 0.0876 | 0.7500 | 0.0387 | 0.5055 | 0.0550 | 0.6800 | 2.1114 | 11.3736 | 14.9902 | 2.1157 | 17.9359 |
| Drug | 279 | 0.3497 | 0.2191 | 0.1502 | 0.0536 | 1.0757 | 1.1199 | 0.0863 | 1.0344 | 0.0587 | 0.1339 | 0.0795 | 0.8900 | 2.8522 | 9.3482 | 13.0162 | 2.7281 | 25.4459 |
| E-Commerce | 57 | 0.2187 | 0.1439 | 0.1308 | 0.1233 | 1.0849 | 1.0287 | 0.0808 | 0.8813 | 0.0437 | 0.0602 | 0.0775 | 1.2000 | 4.5465 | 22.0811 | 31.5988 | 4.5530 | 192.9064 |
| Educational Services | 34 | 0.1727 | 0.2080 | 0.3434 | 0.2517 | 0.9158 | 0.8347 | 0.0691 | 0.7824 | 0.0387 | 0.1097 | 0.0641 | 2.6600 | 1.1379 | 4.6186 | 5.4700 | 2.6860 | 13.8253 |
| Electric Util. (Central) | 21 | 0.0481 | 0.1772 | 0.0638 | 0.3182 | 0.4822 | 0.7524 | 0.0641 | 0.2337 | 0.0237 | 0.4628 | 0.0410 | 0.5500 | 2.2612 | 7.8797 | 12.7581 | 1.5651 | 16.4564 |
| Electric Utility (East) | 21 | -0.0329 | 0.1913 | 0.0689 | 0.3314 | 0.4940 | 0.6976 | 0.0608 | 0.1830 | 0.0237 | 0.3982 | 0.0423 | 0.5400 | 2.5129 | 8.5628 | 13.1357 | 1.7769 | 20.6105 |
| Electric Utility (West) | 14 | 0.0124 | 0.1679 | 0.0611 | 0.3130 | 0.4870 | 0.7500 | 0.0640 | 0.1985 | 0.0237 | 0.4581 | 0.0412 | 0.5400 | 2.1878 | 7.5645 | 13.0291 | 1.3645 | 15.5404 |
| Electrical Equipment | 68 | 0.2514 | 0.1319 | 0.1503 | 0.1702 | 1.3546 | 1.3275 | 0.0989 | 0.6776 | 0.0387 | 0.1124 | 0.0904 | 1.5100 | 1.5416 | 9.1219 | 11.6840 | 2.3252 | 24.0958 |
| Electronics | 139 | 0.1250 | 0.0599 | 0.1572 | 0.1036 | 1.0813 | 1.0670 | 0.0831 | 0.8993 | 0.0437 | 0.1825 | 0.0728 | 3.5100 | 0.4699 | 5.8173 | 7.8385 | 1.6546 | 14.1916 |
| Engineering & Const | 25 | 0.0458 | 0.0472 | 0.1358 | 0.2626 | 1.3876 | 1.2229 | 0.0926 | 0.6503 | 0.0387 | 0.1071 | 0.0851 | 4.0500 | 0.4611 | 7.3624 | 9.7593 | 1.7273 | 15.9467 |
| Entertainment | 77 | 0.1049 | 0.1772 | 0.0945 | 0.1538 | 1.3145 | 1.6312 | 0.1172 | 1.0837 | 0.0587 | 0.2907 | 0.0934 | 0.7800 | 1.8917 | 8.0312 | 10.6748 | 1.7089 | 15.4245 |
| Entertainment Tech | 40 | 0.1478 | 0.1048 | 0.1169 | 0.1159 | 1.4807 | 1.2331 | 0.0932 | 0.7691 | 0.0387 | 0.0889 | 0.0870 | 1.2900 | 1.8672 | 11.6339 | 17.8116 | 1.9725 | 23.9311 |
| Environmental | 82 | 0.0990 | 0.1522 | 0.0756 | 0.1171 | 0.5981 | 0.8051 | 0.0673 | 0.9214 | 0.0487 | 0.3041 | 0.0557 | 0.8000 | 2.0672 | 8.7726 | 13.5845 | 2.2180 | 30.2060 |
| Financial Svcs. (Div.) | 225 | 0.1451 | 0.4349 | 0.0595 | 0.1918 | 0.5034 | 1.3059 | 0.0976 | 0.8227 | 0.0437 | 0.7155 | 0.0465 | 0.1800 | 6.6656 | 14.3615 | 15.3269 | 1.7888 | 21.1449 |
| Food Processing | 112 | 0.0948 | 0.0908 | 0.1188 | 0.2000 | 0.7698 | 0.9133 | 0.0739 | 0.6068 | 0.0337 | 0.2280 | 0.0616 | 1.8200 | 1.0833 | 9.5371 | 11.9307 | 2.5827 | 20.1372 |
| Foreign Electronics | 9 | 0.1751 | 0.0527 | 0.0783 | 0.3512 | 1.2404 | 1.0925 | 0.0847 | 0.3540 | 0.0287 | 0.2962 | 0.0647 | 2.4300 | 0.3704 | 3.4783 | 7.0275 | 0.9003 | 16.6640 |
| Funeral Services | 6 | 0.0109 | 0.1564 | 0.0781 | 0.3084 | 0.8548 | 1.1360 | 0.0873 | 0.3935 | 0.0287 | 0.3614 | 0.0620 | 0.7900 | 1.8552 | 9.1309 | 11.8599 | 1.9284 | 13.9784 |
| Furn/Home Furnishings | 35 | 0.0189 | 0.0643 | 0.0950 | 0.2043 | 1.6528 | 1.8114 | 0.1281 | 0.8090 | 0.0437 | 0.1961 | 0.1081 | 2.0800 | 0.9203 | 9.6767 | 14.3106 | 2.1927 | 21.0763 |
| Healthcare Information | 25 | 0.1171 | 0.1211 | 0.0945 | 0.2219 | 1.2005 | 1.1722 | 0.0895 | 0.6579 | 0.0387 | 0.0597 | 0.0855 | 1.2400 | 3.8198 | 20.7710 | 31.5481 | 4.5466 | 59.7125 |
| Heavy Truck & Equip | 21 | 0.0738 | 0.0913 | 0.1088 | 0.2062 | 1.4790 | 1.8030 | 0.1276 | 0.6992 | 0.0387 | 0.3039 | 0.0959 | 1.6400 | 1.3380 | 10.5443 | 14.6511 | 3.4158 | 22.6346 |
| Homebuilding | 23 | -0.0929 | -0.0156 | -0.0209 | 0.0512 | 1.0174 | 1.4495 | 0.1062 | 0.7000 | 0.0387 | 0.5007 | 0.0647 | 1 | 1.2324 | NA | NA | 1.3799 | 33.2690 |
| Hotel/Gaming | 51 | 0.0752 | 0.1261 | 0.0695 | 0.1453 | 1.2838 | 1.7377 | 0.1237 | 0.7909 | 0.0387 | 0.3424 | 0.0893 | 0.6900 | 2.5848 | 12.4644 | 20.5050 | 2.6368 | 45.8387 |
| Household Products | 26 | 0.1613 | 0.1738 | 0.1452 | 0.2512 | 0.9550 | 1.0686 | 0.0832 | 0.6224 | 0.0337 | 0.1596 | 0.0732 | 1.1300 | 2.2053 | 10.7185 | 12.6909 | 3.3327 | 17.5711 |
| Human Resources | 23 | 0.0001 | 0.0191 | 0.0767 | 0.2535 | 1.3995 | 1.2360 | 0.0934 | 0.7827 | 0.0387 | 0.0935 | 0.0868 | 6.4800 | 0.2857 | 9.9752 | 14.9234 | 1.7122 | 57.0157 |
| Industrial Services | 137 | 0.0839 | -0.2140 | -0.5350 | 0.1903 | 0.8098 | 0.9342 | 0.0751 | 0.7443 | 0.0387 | 0.2465 | 0.0623 | 2.2600 | 0.8529 | NA | NA | 2.3957 | 22.0453 |
| Information Services | 27 | 0.1656 | 0.1933 | 0.1083 | 0.1893 | 0.8932 | 1.0733 | 0.0835 | 0.4810 | 0.0287 | 0.2320 | 0.0681 | 0.7200 | 2.9431 | 10.5490 | 15.2284 | 2.9673 | 25.5627 |
| Insurance (Life) | 30 | 0 | NA | NA | 0.2804 | 1.5360 | 1.5834 | 0.1143 | 0.5335 | 0.0337 | 0.3908 | 0.0776 | NA | NA | 1.3249 | 1.3249 | 0.7029 | 18.6132 |
| Insurance (Prop/Cas.) | 49 | 0.1700 | NA | NA | 0.1936 | 1.0081 | 0.9102 | 0.0737 | 0.3788 | 0.0287 | 0.1910 | 0.0629 | NA | NA | 95.5613 | 96.0146 | 1.0023 | 35.0241 |
| Internet | 186 | 0.1244 | 0.1825 | 0.3275 | 0.0687 | 1.2359 | 1.0886 | 0.0845 | 1.1709 | 0.0587 | 0.0263 | 0.0832 | 2.2500 | 3.9076 | 17.0574 | 21.4116 | 4.5855 | 36.1598 |
| IT Services | 60 | 0.0721 | 0.1443 | 0.2695 | 0.1915 | 1.1400 | 1.0562 | 0.0825 | 0.6945 | 0.0387 | 0.0574 | 0.0791 | 2.6100 | 1.7531 | 9.7487 | 12.1520 | 3.7339 | 21.1775 |
| Machinery | 100 | 0.1357 | 0.1105 | 0.1260 | 0.2215 | 1.1418 | 1.1998 | 0.0912 | 0.5721 | 0.0337 | 0.1605 | 0.0798 | 1.5300 | 1.3714 | 9.0803 | 12.4143 | 2.3340 | 21.5140 |
| Maritime | 52 | 0.0593 | 0.1481 | 0.0476 | 0.0555 | 0.5791 | 1.3959 | 0.1030 | 0.6919 | 0.0387 | 0.6301 | 0.0527 | 0.3500 | 2.6855 | 9.6305 | 18.1384 | 0.8497 | 31.3422 |
| Med Supp Invasive | 83 | 0.0653 | 0.2222 | 0.1588 | 0.1186 | 0.8004 | 0.8481 | 0.0699 | 0.7918 | 0.0387 | 0.1385 | 0.0635 | 0.9200 | 2.5242 | 9.0608 | 11.3608 | 2.5818 | 43.8361 |
| Med Supp Non-Invasive | 146 | 0.0718 | 0.0648 | 0.1924 | 0.1273 | 1.0670 | 1.0301 | 0.0809 | 0.8489 | 0.0437 | 0.1152 | 0.0746 | 4 | 0.7345 | 9.2251 | 11.3395 | 2.8239 | 37.0372 |
| Medical Services | 122 | 0.0492 | 0.1111 | 0.1855 | 0.1993 | 0.7816 | 0.9132 | 0.0739 | 0.7626 | 0.0387 | 0.3309 | 0.0571 | 2.5100 | 0.6830 | 5.1641 | 6.1465 | 2.0877 | 16.4655 |
| Metal Fabricating | 24 | 0.1076 | 0.1507 | 0.1478 | 0.2655 | 1.6276 | 1.5912 | 0.1148 | 0.6898 | 0.0387 | 0.1341 | 0.1025 | 1.3600 | 1.6676 | 8.9144 | 11.0623 | 2.3034 | 18.0063 |
| Metals & Mining (Div.) | 73 | 0.3159 | 0.3157 | 0.1948 | 0.1104 | 1.2760 | 1.3270 | 0.0989 | 1.0438 | 0.0587 | 0.1236 | 0.0910 | 0.8900 | 2.4715 | 6.3518 | 7.8282 | 2.3544 | 31.3154 |
| Natural Gas (Div.) | 29 | 0.0890 | 0.2894 | 0.0710 | 0.2198 | 1.0640 | 1.3250 | 0.0987 | 0.4877 | 0.0287 | 0.2704 | 0.0767 | 0.4100 | 3.3663 | 6.2670 | 11.6304 | 1.5501 | 54.7554 |
| Natural Gas Utility | 22 | -0.0095 | 0.1280 | 0.0809 | 0.3016 | 0.4551 | 0.6591 | 0.0585 | 0.2490 | 0.0237 | 0.4026 | 0.0407 | 0.9400 | 1.4533 | 8.0640 | 11.3551 | 1.8086 | 15.8625 |
| Newspaper | 13 | -0.0501 | 0.1459 | 0.1105 | 0.2513 | 1.4198 | 1.7645 | 0.1253 | 0.9074 | 0.0487 | 0.3167 | 0.0949 | 1.2300 | 1.3113 | 6.5038 | 8.9869 | 2.0423 | 40.8857 |
| Office Equip/Supplies | 24 | 0.1081 | 0.0665 | 0.1036 | 0.2105 | 1.0406 | 1.3750 | 0.1018 | 0.6426 | 0.0337 | 0.3866 | 0.0702 | 2.2600 | 0.5487 | 5.7068 | 8.2541 | 1.3847 | 16.8490 |
| Oil/Gas Distribution | 13 | 0.1265 | 0.1845 | 0.0683 | 0.1370 | 0.6479 | 0.9625 | 0.0768 | 0.5661 | 0.0337 | 0.3683 | 0.0560 | 0.4700 | 3.5562 | 12.5861 | 19.2767 | 2.7279 | 43.3031 |
| Oilfield Svcs/Equip. | 93 | 0.1702 | 0.1511 | 0.0854 | 0.1739 | 1.3871 | 1.5509 | 0.1124 | 0.6237 | 0.0337 | 0.1864 | 0.0952 | 0.7600 | 2.3836 | 9.8684 | 15.7798 | 2.0639 | 27.5817 |
| Packaging & Container | 26 | 0.0909 | 0.1012 | 0.1040 | 0.2423 | 0.8833 | 1.1575 | 0.0886 | 0.4159 | 0.0287 | 0.3413 | 0.0642 | 1.4800 | 1.0637 | 7.1757 | 10.5061 | 2.0939 | 13.1368 |
| Paper/Forest Products | 32 | 0.1088 | 0.1201 | 0.1101 | 0.1061 | 0.9632 | 1.3596 | 0.1008 | 0.9384 | 0.0487 | 0.3745 | 0.0740 | 1.1200 | 1.0612 | 5.4566 | 8.8338 | 1.3021 | 26.2368 |
| Petroleum (Integrated) | 20 | 0.2081 | 0.0976 | 0.1008 | 0.2741 | 1.1188 | 1.1816 | 0.0901 | 0.3899 | 0.0287 | 0.1610 | 0.0783 | 1.7800 | 0.8657 | 5.8899 | 8.8719 | 1.6379 | 58.8684 |
| Petroleum (Producing) | 176 | 0.3222 | 0.2574 | 0.1350 | 0.1114 | 1.1324 | 1.3413 | 0.0997 | 0.8811 | 0.0437 | 0.1992 | 0.0851 | 0.7100 | 2.1964 | 5.5845 | 8.5323 | 1.7574 | 38.3443 |
| Pharmacy Services | 19 | 0.1195 | 0.0511 | 0.1118 | 0.2467 | 1.0001 | 1.1200 | 0.0863 | 0.5943 | 0.0337 | 0.1700 | 0.0751 | 3.5600 | 0.5251 | 8.1981 | 10.2761 | 2.1925 | 12.9696 |
| Pipeline MLPs | 27 | 0.2283 | 0.0895 | 0.0860 | 0.0637 | 0.7172 | 0.9841 | 0.0781 | 0.3490 | 0.0287 | 0.2906 | 0.0604 | 0.9900 | 1.9660 | 15.0333 | 21.9559 | 3.1246 | 27.5521 |
| Power | 93 | 0.4306 | 0.1454 | 0.0756 | 0.0866 | 0.6470 | 1.3518 | 0.1003 | 0.9719 | 0.0487 | 0.5981 | 0.0578 | 0.6900 | 1.4784 | 6.6252 | 10.1702 | 1.0622 | 17.9179 |
| Precious Metals | 84 | 0.3231 | 0.3330 | 0.0957 | 0.0751 | 1.1414 | 1.1464 | 0.0879 | 0.9087 | 0.0487 | 0.0757 | 0.0835 | 0.4000 | 5.3281 | 11.5154 | 15.9999 | 2.1471 | 90.3920 |
| Precision Instrument | 77 | 0.2336 | 0.1074 | 0.1210 | 0.1394 | 1.3279 | 1.2752 | 0.0957 | 0.6533 | 0.0387 | 0.1375 | 0.0858 | 1.3800 | 1.6436 | 10.2513 | 15.3026 | 2.2026 | 32.8644 |
| Property Management | 31 | 0.1980 | 0.1563 | 0.0518 | 0.1859 | 0.5874 | 1.1345 | 0.0872 | 0.8221 | 0.0437 | 0.5844 | 0.0516 | 0.4000 | 2.8465 | 12.9982 | 18.2124 | 1.3566 | 48.1975 |
| Public/Private Equity | 11 | 0.3994 | -0.0258 | -0.0014 | 0.0379 | 1.6238 | 2.1750 | 0.1501 | 0.7754 | 0.0387 | 0.3745 | 0.1026 | 0.3000 | 3.4254 | NA | NA | 1.0170 | 8.9194 |
| Publishing | 24 | -0.0693 | 0.1210 | 0.1138 | 0.1855 | 0.8914 | 1.2467 | 0.0940 | 0.6498 | 0.0337 | 0.3876 | 0.0654 | 1.3700 | 1.1464 | 6.4409 | 9.4714 | 2.1967 | 104.1850 |
| R.E.I.T. | 5 | 0.0001 | 1.2907 | 0.1407 | 0.0104 | 1.1463 | 1.4675 | 0.1073 | 0.4960 | 0.0287 | 0.2577 | 0.0841 | 0.1100 | 14.1290 | 9.5361 | 10.9466 | 1.8862 | 16.9836 |
| Railroad | 12 | 0.1229 | 0.2843 | 0.1110 | 0.2374 | 1.2400 | 1.4391 | 0.1056 | 0.4295 | 0.0287 | 0.2009 | 0.0879 | 0.6000 | 3.4356 | 9.1892 | 12.0856 | 2.6684 | 37.9601 |
| Recreation | 56 | 0.0656 | 0.1151 | 0.0826 | 0.1737 | 1.1064 | 1.4491 | 0.1062 | 0.7055 | 0.0387 | 0.3275 | 0.0790 | 0.8900 | 1.6019 | 9.1086 | 13.9168 | 1.7133 | 40.2136 |
| Reinsurance | 13 | 0 | NA | NA | 0.0722 | 1.0543 | 0.9269 | 0.0747 | 0.3040 | 0.0287 | 0.1906 | 0.0637 | NA | NA | 22.4735 | 22.4735 | 0.7128 | 47.4683 |
| Restaurant | 63 | 0.0245 | 0.1582 | 0.2032 | 0.2157 | 1.1925 | 1.2672 | 0.0952 | 0.6837 | 0.0387 | 0.1132 | 0.0871 | 1.8200 | 2.5022 | 12.1659 | 15.8193 | 6.6636 | 20.0274 |
| Retail (Hardlines) | 75 | 0.0383 | 0.0750 | 0.1499 | 0.2304 | 1.6539 | 1.7716 | 0.1257 | 0.9279 | 0.0487 | 0.1957 | 0.1068 | 3 | 0.8292 | 7.7289 | 11.0604 | 3.0412 | 36.5229 |
| Retail (Softlines) | 47 | 0.0618 | 0.0939 | 0.2874 | 0.2464 | 1.5740 | 1.4372 | 0.1055 | 0.6090 | 0.0337 | 0.0532 | 0.1010 | 4.9400 | 0.8730 | 6.8399 | 9.2982 | 3.4570 | 45.4478 |
| Retail Automotive | 20 | 0.1109 | 0.0688 | 0.0989 | 0.3443 | 1.1221 | 1.3681 | 0.1013 | 0.5202 | 0.0337 | 0.2759 | 0.0790 | 2.2200 | 0.9216 | 10.7579 | 13.3996 | 3.2128 | 16.2185 |
| Retail Building Supply | 8 | 0.1538 | 0.0813 | 0.1218 | 0.3139 | 0.9682 | 1.0443 | 0.0818 | 0.3761 | 0.0287 | 0.1233 | 0.0738 | 2.3700 | 1.0439 | 9.7406 | 12.8466 | 3.0237 | 22.7848 |
| Retail Store | 37 | 0.0885 | 0.0584 | 0.1360 | 0.2502 | 1.1448 | 1.2866 | 0.0964 | 0.6771 | 0.0387 | 0.2037 | 0.0815 | 3.5500 | 0.5897 | 7.4508 | 10.1030 | 2.6203 | 18.7849 |
| Retail/Wholesale Food | 30 | 0.0823 | 0.0318 | 0.1038 | 0.3121 | 0.6354 | 0.7482 | 0.0639 | 0.4002 | 0.0287 | 0.2925 | 0.0502 | 5.0200 | 0.3465 | 6.7252 | 10.9088 | 2.2260 | 36.6603 |
| Securities Brokerage | 28 | 0.0459 | 0.4878 | 0.1039 | 0.2622 | 0.4268 | 1.1980 | 0.0911 | 0.4431 | 0.0287 | 0.8115 | 0.0311 | 0.2900 | 3.0845 | 5.9679 | 6.3237 | 0.7186 | 24.7673 |
| Semiconductor | 141 | 0.4130 | 0.2276 | 0.2841 | 0.1101 | 1.6886 | 1.5010 | 0.1094 | 0.7052 | 0.0387 | 0.0770 | 0.1027 | 1.5700 | 2.0563 | 6.1928 | 9.0340 | 2.6201 | 20.9049 |
| Semiconductor Equip | 12 | 0.5588 | 0.2165 | 0.4044 | 0.1517 | 2.4210 | 1.7933 | 0.1270 | 0.6870 | 0.0387 | 0.1320 | 0.1133 | 2.2100 | 0.9742 | 3.7750 | 4.4995 | 1.6803 | 10.8272 |
| Shoe | 19 | 0.0350 | 0.1134 | 0.2741 | 0.2431 | 1.3786 | 1.2511 | 0.0943 | 0.5552 | 0.0337 | 0.0213 | 0.0927 | 3.3300 | 1.5207 | 11.6356 | 13.4061 | 3.7360 | 14.0978 |
| Steel | 32 | 0.3089 | 0.0583 | 0.0594 | 0.2103 | 1.4007 | 1.6825 | 0.1203 | 0.5694 | 0.0337 | 0.3169 | 0.0886 | 1.2100 | 0.7752 | 7.0759 | 13.2954 | 0.9234 | 16.4575 |
| Telecom. Equipment | 99 | 0.0418 | 0.1087 | 0.2330 | 0.1316 | 1.2810 | 1.0153 | 0.0800 | 0.8777 | 0.0437 | 0.1148 | 0.0738 | 2.7300 | 1.2502 | 8.4579 | 11.4999 | 2.3210 | 18.3200 |
| Telecom. Services | 74 | 0.1495 | 0.2274 | 0.1370 | 0.1422 | 0.8232 | 0.9785 | 0.0778 | 0.6858 | 0.0387 | 0.2542 | 0.0639 | 0.8300 | 1.8502 | 4.7974 | 8.1367 | 1.7463 | 16.9748 |
| Telecom. Utility | 25 | -0.0690 | 0.1583 | 0.0834 | 0.2942 | 0.5394 | 0.8763 | 0.0716 | 0.6039 | 0.0337 | 0.4902 | 0.0464 | 0.7400 | 1.7488 | 5.3263 | 11.0492 | 1.7860 | 132.3530 |
| Thrift | 148 | 0 | NA | NA | 0.1243 | 0.7480 | 0.7113 | 0.0617 | 0.5393 | 0.0337 | 0.2268 | 0.0523 | NA | NA | 3.6719 | 3.6719 | 0.9374 | 36.3996 |
| Tobacco | 11 | 0.0661 | 0.2061 | 0.2798 | 0.3103 | 0.7806 | 0.8538 | 0.0703 | 0.4153 | 0.0287 | 0.1576 | 0.0619 | 1.8400 | 2.3570 | 10.3614 | 11.4362 | 8.6319 | 14.8843 |
| Toiletries/Cosmetics | 15 | 0.0256 | 0.1085 | 0.1954 | 0.2030 | 1.1960 | 1.3014 | 0.0973 | 0.6034 | 0.0337 | 0.1711 | 0.0841 | 2.7000 | 1.4837 | 11.0453 | 13.6747 | 6.4860 | 35.5015 |
| Trucking | 36 | 0.0952 | 0.0637 | 0.0907 | 0.2548 | 1.0805 | 1.2441 | 0.0938 | 0.5988 | 0.0337 | 0.2173 | 0.0778 | 2.1600 | 1.2764 | 10.1291 | 20.0528 | 4.4857 | 30.7780 |
| Utility (Foreign) | 4 | 0.0492 | 0.1160 | 0.0456 | 0.2607 | 0.4801 | 0.9625 | 0.0768 | 0.3268 | 0.0287 | 0.6079 | 0.0406 | 0.5800 | 1.3861 | 5.4702 | 11.9501 | 0.6390 | 1687.0174 |
| Water Utility | 11 | 0.0543 | 0.2661 | 0.0542 | 0.3522 | 0.4331 | 0.6591 | 0.0585 | 0.1889 | 0.0237 | 0.4488 | 0.0386 | 0.3000 | 4.3852 | 11.1284 | 16.4818 | 1.7669 | 22.3512 |
| Wireless Networking | 57 | 0.1071 | -0.1147 | -0.1821 | 0.1212 | 1.1201 | 1.2695 | 0.0954 | 0.7503 | 0.0387 | 0.2130 | 0.0800 | 1.1400 | 1.9150 | NA | NA | 2.7204 | 38.6809 |
| Total Market | 5891 | 0.1480 | 0.1724 | 0.1221 | 0.1548 | 0.9244 | 1.1492 | 0.0881 | 0.7508 | 0.0387 | 0.3181 | 0.0675 | 0.9700 | 1.6725 | 7.3726 | 9.7037 | 1.9983 | 33.6702 |

**Outputs (`Input page`):**

| Cell | Meaning | Example |
|---|---|---|
| B23 | Value of assets in place (no-growth perpetuity) | 8905.429 |
| B24 | Value added by future growth (intrinsic) | 5951.452 |
| B25 / B26 | Intrinsic enterprise value / intrinsic equity value | 14856.881 / 15153.881 |
| E23 / E24 | Market equity value / market enterprise value | 70000 / 69703 |
| B28 | Price the market is paying for growth | 60797.571 |
| B30 | Price-of-growth divided by value-of-growth | 10.2156 |
| B34:G37 | Multiple decomposition grid (actual and intrinsic; total, assets-in-place, growth) | see Logic |

**Worked example (values in the saved sheet):** ATOI = 1695×0.6 = 1017. Assets in place = 1017/0.1142 = 8905.43. RR_hg = 0.1142/0.275311 = 0.41480, so FCFF_0 = −421.85 and FCFF_1 = 1017×1.1142×(1−0.41480) = 663.11. FCFF grows at 11.42% through year 9; year-10 FCFF = 2998.83×(1−0.17513) = 2473.64. TV = 3058.81×(1−0.17513)/(0.1142−0.02) = 26784.69. Value with growth = −421.85 + PV(10 yrs + TV) = 14856.88. Growth value = 14856.88 − 8905.43 = 5951.45. The market pays 69703 − 8905.43 = 60797.57 for that growth: 10.2x its intrinsic worth.

**Reimplementation notes:**
- Inputs: market_cap, bve_now, bve_prior, debt_now, debt_prior, cash_now, cash_prior, rev_now, rev_prior, ebit_now, ebit_prior, eff_tax_rate, net_income (all floats, currency in millions or any consistent unit); g_hg, roic_growth, n_years (int), cost_of_equity, wacc, rf (rates as decimals).
- Outputs: assets_in_place_value, growth_value, intrinsic_ev, intrinsic_equity, market_ev, price_of_growth, price_to_value_of_growth, plus the 4×6 multiple grid.
- Closed forms (no need for the year-by-year table): assets_in_place = ATOI/wacc. Growth value = FCFF_0 + Σ + TV as above; with constant g the sum is a geometric series but year n uses RR_st, so compute year-by-year for clarity. Support n other than 10 (the sheet's table caps at 10; a port should not).
- Implement the implied-growth solve (Goal Seek) as a root-find on g: growth_value(g) − (market_ev − assets_in_place) = 0. Use Brent's method over, say, g ∈ (−0.5, 2).
- Edge cases: negative EBIT makes ATOI and the perpetuity negative — the decomposition is meaningless; raise or warn. wacc ≤ rf makes TV negative/undefined — validate wacc > rf (stable g = rf by construction). roic_growth = 0 divides by zero in RR_hg. Denominators NI, BVE, revenues, IC may be ≤ 0 for the multiple grid — emit NaN per cell rather than failing. Note the two label quirks to preserve fidelity: E7 is after-tax margin despite its "pre-tax" label, and the "EV/..." actual-total multiples use market equity, not EV.
- Cost-of-capital helper: port the bond-pricing MV-of-debt formula with the M=0 → book-value branch, the levered-beta formula, and the three-component WACC. Keep it a separate function; the main model takes wacc directly.

---

### higrowth.xls

**Purpose:** Damodaran's flagship model for valuing young, high-growth firms with negative earnings (the Amazon-in-1999 workhorse). It values the firm with a 10-year FCFF model driven by revenue growth and a target operating margin that current (negative) margins converge to. It handles NOL carryforwards, capitalizes operating leases and R&D, ramps the debt ratio and beta toward stable-period targets over years 6–10, nets out employee options with a dilution-adjusted Black-Scholes, and cross-checks with a forward revenue multiple. The saved example is a specialty retailer: revenues 1246.3, EBIT −55, price 119.48.

**Inputs (`Input Sheet(assumtion)`):**

| Label | Cell | Example |
|---|---|---|
| Current EBIT | B4 | −55.0 |
| Current Interest Expense | B5 | 0.509 |
| Current Capital Spending | B6 | 459.271 |
| Current Depreciation and Amortization | B7 | 59.518 |
| Current Revenues | B8 | 1246.301 |
| Current Non-cash Working Capital — this / last period | B10 / C10 | 65 / 29 |
| Book Value of Debt — this / last period | B11 / C11 | 198.47 / 108.165 |
| Book Value of Equity — this / last period | B12 / C12 | 1513.042 / 1097.267 |
| Cash & Marketable Securities | B13 | 792.26 |
| Non-operating Assets | B14 | 194.479 |
| NOL carried forward | B16 | 1289 |
| Marginal tax rate | B17 | 0.375 |
| Do you have any operating leases? | D20 | Yes |
| Does your firm have R&D expenses? | D21 | No |
| Any other operating expenses to capitalize? | D22 | No |
| Current Beta | B25 | 1.369809 (computed off-sheet; treat as input) |
| Current Cost of Borrowing | B26 | 0.0591 |
| Current Market Value of Debt | B27 | 143.138 (= bond-pricing formula on book debt 198.47, interest 0.509, kd 0.0591, maturity ≈ 6 yrs — inferred; treat as input) |
| Enter growth rate in revenues each year? | E30 | Yes (→ uses `Revenue Growth Numbers` sheet) |
| If no: CAGR in revenues for next 10 years | E31 | 0.2854 |
| Use current working capital as % of revenues? | E32 | No |
| If not: future non-cash WC as % of revenues | E33 | 1.4077 |
| Capex estimation method (1/2/3) | E34 | 3 |
| If 3: sales-to-capital ratio maintained | E35 | 3.02 |
| Expected growth rate in perpetuity | C38 | 0.03 |
| Expected (target) operating margin | C39 | 0.141935 |
| Speed of convergence | D39 | 1.5 |
| Expected debt-to-capital (MV) ratio, stable | C40 | 0.4471 |
| Expected beta, stable | C41 | 1.1 |
| Expected cost of debt, stable | C42 | 0.072043 |
| Return on capital, stable | C43 | 0.26385 |
| Number of shares outstanding | D46 | 81.644 |
| Current stock price | D47 | 119.48 |
| Equity options outstanding? / number / avg strike / avg maturity / stock std dev | D48–D52 | Yes / 1.53631 / 251.31 / 9 / 0.611845 |
| Current long-term government bond rate | D55 | 0.0355 |
| Estimated market risk premium | D56 | 0.0456 |
| Relative valuation: year for multiple / Value-to-Sales multiple | C60 / C61 | 10 / 3.796507 |

Per-year revenue growth (`Revenue Growth Numbers` sheet, B3:B12): 0.55, 0.45, 0.40, 0.35, 0.30, 0.20, 0.15, 0.12, 0.08, 0.06 (compounded average shown: 0.256010).

Operating-lease inputs (`Operating Leases` sheet): current-year lease expense E3 = 43; commitments B6:B11 for years 1–5 = 9.383, 5.296, 4.85, 4.047, 3.916 and "6 and beyond" = 41.675; pre-tax cost of debt C14 = 0.0591; years embedded in the yr-6 lump D20 = 8. (Cells D17 = 438.339 "Reported EBIT" and D18 = 254.634 "Reported Debt" are stale leftovers, inconsistent with the input sheet.)

R&D inputs (`R&D` sheet): amortization years F6 = 3; current R&D F7 = 34.417; past R&D B11:B13 = 16.907 (yr −1), 7.261 (yr −2), 3.272 (yr −3). `Other Expenses to Capitalize` sheet: amortization years F6 = 10; current expense F7 = 206.537; past B11:B15 = 99.115, 45.073, 18.998, 10.212, 11.981. Both converters are populated but SWITCHED OFF for this valuation (D21/D22 = No); only the lease adjustment feeds the DCF.

**Logic — operating-lease converter (inferred, verified):**
1. PV each year-1..5 commitment at the pre-tax cost of debt: PV_t = C_t/(1+kd)^t.
2. The "6 and beyond" lump is spread into an annuity: annual = lump / years_embedded (41.675/8 = 5.209375). The sheet note says years_embedded is estimated as lump / average of the first five commitments, rounded (41.675/5.4984 ≈ 7.6 → 8); the cell itself is an input.
3. PV of the tail = annual × [1−(1+kd)^−years_embedded]/kd, discounted a further 5 years: ×(1+kd)^−5 → 24.3628.
4. Debt value of leases = ΣPV = 48.1814.
5. Straight-line depreciation on the lease asset = debt_value/(5+years_embedded) = 48.1814/13 = 3.70626.
6. Adjustment to operating earnings = debt_value × kd = 48.1814×0.0591 = 2.84752 (sheet comment verbatim: "PV of operating leases * Pre-tax cost of debt"). Add this to EBIT; add debt_value to total debt.

**Logic — R&D converter (and identical "other expenses" converter, inferred, verified):** with amortization life N (max 10):
- Unamortized fraction of the expense from k years ago = max(0, 1 − k/N); unamortized amount = expense_−k × fraction. Current-year expense is fully unamortized.
- Value of research asset = current expense + Σ_{k=1..N} unamortized amounts (34.417 + 16.907×2/3 + 7.261×1/3 + 3.272×0 = 48.1087).
- Amortization this year = Σ_{k=1..N} expense_−k / N = (16.907+7.261+3.272)/3 = 9.14667.
- Adjustment to operating income = current expense − amortization = 25.2703 (positive → add to reported EBIT). Tax effect of expensing = adjustment × marginal tax rate = 9.47638 (informational).
- The research-asset value would be added to book equity/capital. The other-expenses sheet: N = 10 gives asset 357.2152, amortization 18.5379, EBIT adjustment 187.9991, tax effect 70.4997.

**Logic — DCF (`DCFValuation` sheet, years 1..10 plus terminal; all inferred, all rows verified):**
1. **Base EBIT** = input EBIT + lease adjustment (if leases=Yes) + R&D adjustment (if R&D=Yes) + other-expense adjustment (if Yes). Here: −55 + 2.84752 = −52.15248. Base margin = −52.15248/1246.301 = −0.0418458.
2. **Revenues**: Rev_t = Rev_{t−1} × (1+g_t) with g_t from the per-year table (or the single CAGR if E30 = No). Terminal-year revenue = Rev_10 × (1+g_stable).
3. **Operating margin** converges from the current margin to the target with "speed of convergence" s: `margin_t = target − (target − margin_{t−1}) / (1 + 1/s)`. With s = 1.5 the margin deficit shrinks by the factor s/(1+s) = 0.6 each year. Terminal-year margin = target exactly. (Verified to 6+ digits for all 10 years.)
4. **EBIT_t** = Rev_t × margin_t.
5. **NOL and taxes**: NOL_0 = input NOL. If EBIT_t ≤ 0: tax = 0 and NOL_t = NOL_{t−1} + |EBIT_t| (loss adds to carryforward — inferred, no negative-EBIT year in the example). If EBIT_t > 0: taxable = max(0, EBIT_t − NOL_{t−1}); tax_t = taxable × marginal_rate; NOL_t = max(0, NOL_{t−1} − EBIT_t). Effective tax rate row = tax_t/EBIT_t (0 until the NOL runs out, partial in the crossover year — year 4 here at 0.0063946 — then the full marginal rate).
6. **EBIT(1−t)_t** = EBIT_t − tax_t.
7. **Depreciation**: grows each year at the revenue growth rate LAGGED 3 YEARS: dep growth in year t = g_{t+3}, using g_stable once t+3 > 10 (inferred from an exact fit on all 10 years: growth 0.35, 0.30, 0.20, 0.15, 0.12, 0.08, 0.06, 0.03, 0.03, 0.03; terminal-year dep = dep_10 × (1+g_stable)).
8. **Total reinvestment** (method 3): `Reinv_t = ΔRev_t / sales_to_capital` = ΔRev_t/3.02. (Method inferred for options 1–2; see notes.) Change in working capital: `ΔWC_t = ΔRev_t × wc_pct` where wc_pct = 1.4077 here (or current WC/Rev if E32 = Yes). Capex is the plug: `Capex_t = Reinv_t + Dep_t − ΔWC_t` (negative in this example, since ΔWC swamps the capital need). FCFF identity holds both ways: `FCFF_t = EBIT(1−t)_t + Dep_t − Capex_t − ΔWC_t = EBIT(1−t)_t − Reinv_t`.
9. **Terminal-year reinvestment** switches to the stable relation: `RR_terminal = g_stable / ROC_stable` = 0.03/0.26385 = 0.113701; Reinv_term = EBIT(1−t)_term × RR_terminal = 126.51.
10. **Discount rates**: cost of equity_t = rf + beta_t × ERP. Years 1–5 hold current values: beta = 1.369809, debt ratio = MV debt/(MV debt + MV equity) at input prices = 191.3198/(191.3198 + 81.644×119.48) = 0.0192356 (uses debt incl. leases and price×shares — inferred), kd = 0.0591. Years 6–10 converge to stable targets: beta linearly (`beta_t = beta_cur − (beta_cur − beta_stable)×(t−5)/5`); debt ratio and cost of debt by the schedule `x_t = x_cur + (x_stable − x_cur)/(11 − t)` for t = 6..10, i.e. fractions 1/5, 1/4, 1/3, 1/2, 1 of the total gap (verified exactly). After-tax kd_t = kd_t × (1 − effective_tax_rate_t). `WACC_t = ke_t×(1−DR_t) + kd_t×(1−tax_t)×DR_t`.
11. **Terminal value** = FCFF_terminal / (WACC_terminal − g_stable) = 986.150/(0.0674928−0.03) = 26302.380.
12. **Discounting** uses the cumulative product of year-specific WACCs: CumWACC_t = Π_{i=1..t}(1+WACC_i); PV(FCFF_t) = FCFF_t/CumWACC_t; PV(TV) = TV/CumWACC_10.
13. **Equity bridge**: Value of operating assets = ΣPV(FCFF) + PV(TV) = 1244.742 + 11234.522 = 12479.265. + Cash & non-operating assets (792.26+194.479 = 986.739) → firm value 13466.004. − MV of debt (143.138 + lease debt 48.181 = 191.320) → equity 13274.684. − value of equity options **after tax**: options_value × (1 − marginal_rate) = 152.070×0.625 = 95.044 → common equity 13179.640. ÷ shares → **161.428 per share**. Alternative "Treasury Stock Approach" cell: (equity_value + n_options × strike)/(shares + n_options) = (13274.684 + 386.090)/83.180 = 164.231.
14. Diagnostics: capital invested_t = capital_{t−1} + Reinv_t starting from BV debt + BV equity = 1711.512; ROC_t = EBIT(1−t)_t/capital_{t−1}; reinvestment rate_t = Reinv_t/EBIT(1−t)_t; ΔRev/ΔCapital ≈ sales-to-capital by construction.

**Logic — options (`Options` sheet, dilution-adjusted Black-Scholes, inferred, verified):** S = DCF value per share (161.428 — CIRCULAR with the DCF; Excel solves by iteration), K = 251.31, T = 9, σ = 0.611845 (variance 0.374355), r = 0.0355, dividend yield y = 0, n_w = 1.53631 warrants, n_s = 81.644 shares.
- Adjusted S = (S×n_s + W×n_w)/(n_s + n_w) where W is the option value itself (second circularity, iterated to a fixed point). Adjusted K = K.
- d1 = [ln(S_adj/K) + (r − y + σ²/2)T]/(σ√T) = 0.846782; d2 = d1 − σ√T = −0.988754.
- Value per option = S_adj×e^(−yT)×N(d1) − K×e^(−rT)×N(d2) = 98.984. Value of all options = ×n_w = 152.070. The DCF then subtracts 152.070×(1−0.375) = 95.044 (after-tax, since option exercise generates a tax deduction).

**Logic — relative valuation (`Relative Valuation` sheet):** Value in chosen year = Rev_year10 × VS multiple = 12177.399×3.796507 = 46231.582. Value today = that / CumWACC_10 = 19746.872. + cash 986.739 − debt 191.320 − options 95.044 → equity 20447.248; ÷ shares → 250.444 per share.

**Reference data 1 — R&D amortization-period lookup (`R&D` sheet rows 44–141, verbatim, 98 industries):** guideline block (verbatim): Non-technological Service = 2 years; Retail, Tech Service = 3 years; Light Manufacturing = 5 years; Heavy Manufacturing = 10 years; Research, with Patenting = 10 years; Long Gestation Period = 10 years.


| Industry Name | Amortization Period (years) |
|---|---|
| Advertising | 2 |
| Aerospace/Defense | 10 |
| Air Transport | 10 |
| Aluminum | 5 |
| Apparel | 3 |
| Auto & Truck | 10 |
| Auto Parts (OEM) | 5 |
| Auto Parts (Replacement) | 5 |
| Bank | 2 |
| Bank (Canadian) | 2 |
| Bank (Foreign) | 2 |
| Bank (Midwest) | 2 |
| Beverage (Alcoholic) | 3 |
| Beverage (Soft Drink) | 3 |
| Building Materials | 5 |
| Cable TV | 10 |
| Canadian Energy | 10 |
| Cement & Aggregates | 10 |
| Chemical (Basic) | 10 |
| Chemical (Diversified) | 10 |
| Chemical (Specialty) | 10 |
| Coal/Alternate Energy | 5 |
| Computer & Peripherals | 5 |
| Computer Software & Svcs | 3 |
| Copper | 5 |
| Diversified Co. | 5 |
| Drug | 10 |
| Drugstore | 3 |
| Educational Services | 3 |
| Electric Util. (Central) | 10 |
| Electric Utility (East) | 10 |
| Electric Utility (West) | 10 |
| Electrical Equipment | 10 |
| Electronics | 5 |
| Entertainment | 3 |
| Environmental | 5 |
| Financial Services | 2 |
| Food Processing | 3 |
| Food Wholesalers | 3 |
| Foreign Electron/Entertn | 5 |
| Foreign Telecom. | 10 |
| Furn./Home Furnishings | 3 |
| Gold/Silver Mining | 5 |
| Grocery | 2 |
| Healthcare Info Systems | 3 |
| Home Appliance | 5 |
| Homebuilding | 5 |
| Hotel/Gaming | 3 |
| Household Products | 3 |
| Industrial Services | 3 |
| Insurance (Diversified) | 3 |
| Insurance (Life) | 3 |
| Insurance (Prop/Casualty) | 3 |
| Internet | 3 |
| Investment Co. (Domestic) | 3 |
| Investment Co. (Foreign) | 3 |
| Investment Co. (Income) | 3 |
| Machinery | 10 |
| Manuf. Housing/Rec Veh | 5 |
| Maritime | 10 |
| Medical Services | 3 |
| Medical Supplies | 5 |
| Metal Fabricating | 10 |
| Metals & Mining (Div.) | 5 |
| Natural Gas (Distrib.) | 10 |
| Natural Gas (Diversified) | 10 |
| Newspaper | 3 |
| Office Equip & Supplies | 5 |
| Oilfield Services/Equip. | 5 |
| Packaging & Container | 5 |
| Paper & Forest Products | 10 |
| Petroleum (Integrated) | 5 |
| Petroleum (Producing) | 5 |
| Precision Instrument | 5 |
| Publishing | 3 |
| R.E.I.T. | 3 |
| Railroad | 5 |
| Recreation | 5 |
| Restaurant | 2 |
| Retail (Special Lines) | 2 |
| Retail Building Supply | 2 |
| Retail Store | 2 |
| Securities Brokerage | 2 |
| Semiconductor | 5 |
| Semiconductor Cap Equip | 5 |
| Shoe | 3 |
| Steel (General) | 5 |
| Steel (Integrated) | 5 |
| Telecom. Equipment | 10 |
| Telecom. Services | 5 |
| Textile | 5 |
| Thrift | 2 |
| Tire & Rubber | 5 |
| Tobacco | 5 |
| Toiletries/Cosmetics | 3 |
| Trucking/Transp. Leasing | 5 |
| Utility (Foreign) | 10 |
| Water Utility | 10 |

**Outputs (higrowth.xls):**

| Cell | Meaning | Example |
|---|---|---|
| DCFValuation D36 / D37 | PV of FCFF, high-growth phase / PV of terminal value | 1244.742 / 11234.522 |
| D38 | Value of operating assets | 12479.265 |
| D40 / D41 / D42 | Firm value / − debt / equity value | 13466.004 / 191.320 / 13274.684 |
| D43 / D44 | − after-tax option value / equity in common stock | 95.044 / 13179.640 |
| D45 | **Value of equity per share** | 161.428 |
| F45 | Per share, treasury-stock approach | 164.231 |
| Relative Valuation B13 | Per-share value from forward revenue multiple | 250.444 |
| Operating Leases C30 / F33 / F34 | Lease debt / lease-asset depreciation / EBIT adjustment | 48.181 / 3.706 / 2.848 |
| R&D D35 / D37 / D39 / D40 | Research asset / amortization / EBIT adjustment / tax effect | 48.109 / 9.147 / 25.270 / 9.476 |

**Worked example:** see the Logic section — every step above carries the example's numbers end-to-end (revenues 1246.301 → 12177.399 by year 10; margin −4.18% → +14.08%; taxes start in year 4 when the 1289 NOL is exhausted; WACC drifts from 9.72% to 6.75%; per-share value 161.43 vs market price 119.48).

**Reimplementation notes (higrowth):**
- Inputs: the full table above. Types: currency floats; rates as decimals; yes/no booleans; capex_method ∈ {1,2,3}; growth either a 10-vector or a scalar CAGR.
- The model is hard-wired to a 10-year high-growth phase with rate transition at year 6; parameterize n and the transition point but keep 10/6 as defaults.
- Circularity: per-share value depends on option value, which depends on per-share value (twice: via S and via the dilution-adjusted S). Solve by fixed-point iteration (initialize S at the no-option per-share value; converges in <20 iterations) or a 1-D root-find on S.
- Discounting must use the cumulative product of per-year WACCs, not a constant rate.
- Convergence schedules to implement exactly: margin deficit ×s/(1+s) per year; beta linear over years 6–10; debt ratio and kd jump by 1/(11−t) of the total gap (so the ratio path is convex, back-loaded).
- Branches: leases/R&D/other-capitalization toggles change base EBIT and debt; growth vector vs CAGR; WC%-of-revenue current vs override; capex method (only method 3, sales-to-capital, is exercised in this copy — implement 1 as "grow current capex and depreciation with revenue" and 2 as "capex as % of revenue" only if needed, and mark them unverified).
- Edge cases: negative EBIT years must add to the NOL, not create negative tax; the crossover year gets a partial tax; ΔWC can exceed capital needs making capex negative (allowed — it is a plug); WACC_terminal must exceed g_stable; sales_to_capital = 0 divides by zero; if revenue growth is negative, ΔRev < 0 gives negative reinvestment (allowed in the sheet's algebra); N(·) is the standard normal CDF; option maturity 0 or σ = 0 degenerate Black-Scholes.
- Units: shares/options in millions to match currency in millions.

**Reference data 2 — `Industry Averages` sheet in higrowth.xls (DIFFERENT columns from the growthbreakdown table; 100 industries, verbatim, floats rounded to 4 decimals).** Headers are verbatim from row 1 of the sheet. Full table:

| Industry Name | Number of firms | Levered Beta | Unlevered Beta | Std Dev: Equity | Market D/E | Market Debt/Capital | ROE | ROC | Effective Tax Rate | Pre-tax Operating Margin | After-tax Operating Margin | Net Margin | Cap Ex/ Depreciation | Non-cash WC/ Revenues | Payout Ratio | Reinvestment Rate | Sales/Capital | EV/Sales |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 31 | 2.0200 | 1.7500 | 1.0129 | 0.4326 | 0.3020 | 0.0889 | 0.1054 | 0.1073 | 0.1027 | 0.0744 | 0.0363 | 0.5418 | -0.1984 | 0.4375 | -0.4614 | 1.4200 | 1.1400 |
| Aerospace/Defense | 64 | 1.1000 | 1.0300 | 0.6132 | 0.2566 | 0.2042 | 0.3400 | 0.1853 | 0.2072 | 0.1016 | 0.0731 | 0.0678 | 1.2628 | 0.0289 | 0.2913 | 0.1477 | 2.5300 | 0.9300 |
| Air Transport | 36 | 1.2100 | 1.1000 | 0.6480 | 0.2432 | 0.1956 | 1.0890 | 0.1645 | 0.2054 | 0.0878 | 0.0686 | 0.0376 | 1.2222 | -0.0925 | 0.1891 | 0.0554 | 2.4000 | 1.7800 |
| Apparel | 57 | 1.3000 | 1.2200 | 0.8882 | 0.1838 | 0.1553 | 0.1734 | 0.1402 | 0.1608 | 0.1097 | 0.0760 | 0.0672 | 1.0324 | 0.1724 | 0.1885 | 0.2213 | 1.8500 | 1.1900 |
| Auto Parts | 51 | 1.7000 | 1.5900 | 0.8058 | 0.2765 | 0.2166 | 0.2259 | 0.1582 | 0.1899 | 0.0649 | 0.0498 | 0.0510 | 0.9608 | 0.0559 | 0.2374 | 0.1516 | 3.1800 | 0.5900 |
| Automotive | 12 | 1.5900 | 0.9600 | 0.6891 | 1.3457 | 0.5737 | 0.1846 | 0.0696 | 0.2407 | 0.0699 | 0.0494 | 0.0336 | 0.8704 | 0.1937 | 0.2224 | -0.2237 | 1.4100 | 0.7300 |
| Bank | 426 | 0.7700 | 0.3800 | 0.6115 | 1.5611 | 0.6095 | 0.0760 | NA | 0.1597 | NA | NA | NA | NA | NA | 0.3353 | 0 | NA | NA |
| Bank (Midwest) | 45 | 0.9300 | 0.7300 | 0.5560 | 0.5952 | 0.3731 | 0.0908 | NA | 0.1777 | NA | NA | NA | NA | NA | 0.3836 | 0 | NA | NA |
| Beverage | 34 | 0.8800 | 0.7700 | 0.6605 | 0.2652 | 0.2096 | 0.2458 | 0.1295 | 0.1914 | 0.2045 | 0.1560 | 0.1399 | 0.8724 | 0.0108 | 0.4635 | -0.0246 | 0.8300 | 3.0300 |
| Biotechnology | 158 | 1.0300 | 1.1600 | 1.1311 | 0.1348 | 0.1188 | 0.1515 | -0.1333 | 0.0249 | -0.0779 | -0.1373 | 0.0911 | 0.8442 | -0.0583 | 0.5934 | NA | 0.9700 | 4.4900 |
| Building Materials | 45 | 1.5000 | 0.8900 | 0.7883 | 0.9433 | 0.4854 | -0.0517 | 0.0258 | 0.1117 | 0.0417 | 0.0316 | -0.0401 | 0.4800 | 0.0766 | NA | -1.0683 | 0.8200 | 1.2200 |
| Cable TV | 21 | 1.3700 | 0.9800 | 0.5077 | 0.6806 | 0.4050 | 0.1613 | 0.0880 | 0.2735 | 0.1958 | 0.1243 | 0.0902 | 0.8532 | -0.0965 | 0.1803 | -0.3082 | 0.7100 | 2.2100 |
| Chemical (Basic) | 16 | 1.3600 | 1.2400 | 0.4927 | 0.2735 | 0.2147 | 0.2583 | 0.1366 | 0.2090 | 0.1209 | 0.0956 | 0.1246 | 1.2681 | 0.0968 | 0.3079 | 0.2924 | 1.4300 | 1.5200 |
| Chemical (Diversified) | 31 | 1.5100 | 1.3900 | 0.5631 | 0.2237 | 0.1828 | 0.1926 | 0.1381 | 0.2173 | 0.1320 | 0.0930 | 0.0879 | 1.0437 | 0.1558 | 0.3168 | 0.4792 | 1.4800 | 1.6200 |
| Chemical (Specialty) | 70 | 1.2800 | 1.1500 | 0.7160 | 0.2115 | 0.1746 | 0.1850 | 0.1225 | 0.1758 | 0.1110 | 0.0787 | 0.0804 | 0.9678 | 0.1260 | 0.4043 | 0.1299 | 1.5600 | 1.5600 |
| Coal | 20 | 1.5300 | 1.3200 | 0.5552 | 0.2890 | 0.2242 | 0.2424 | 0.1526 | 0.1275 | 0.1594 | 0.1253 | 0.1200 | 1.4173 | 0.0361 | 0.3378 | 0.3748 | 1.2200 | 1.7800 |
| Computer Software | 184 | 1.0400 | 1.1800 | 0.8203 | 0.0749 | 0.0697 | 0.7913 | 0.4506 | 0.1227 | 0.3135 | 0.2462 | 0.2478 | 0.6472 | -0.1116 | 0.2161 | -0.0905 | 1.8300 | 3.0700 |
| Computers/Peripherals | 87 | 1.3000 | 1.3300 | 0.9769 | 0.1023 | 0.0928 | 0.5252 | 0.3209 | 0.1177 | 0.1415 | 0.1083 | 0.1074 | 1.0358 | -0.0197 | 0.0861 | 0.0122 | 2.9600 | 1.3900 |
| Diversified Co. | 107 | 1.1400 | 0.7100 | 0.7500 | 1.0224 | 0.5055 | 0.3328 | 0.0801 | 0.1555 | 0.1409 | 0.1176 | 0.0921 | 0.8924 | 0.7165 | 0.3681 | 0.0167 | 0.6800 | 2.1100 |
| Drug | 279 | 1.1200 | 1.0800 | 1.0344 | 0.1546 | 0.1339 | 0.2264 | 0.1502 | 0.0536 | 0.2191 | 0.1696 | 0.1799 | 0.3739 | 0.0753 | 0.4912 | -0.2869 | 0.8900 | 2.8500 |
| E-Commerce | 57 | 1.0300 | 1.0800 | 0.8813 | 0.0640 | 0.0602 | 0.1647 | 0.1308 | 0.1233 | 0.1439 | 0.1087 | 0.1073 | 1.2844 | -0.1160 | 0.0189 | -0.0256 | 1.2000 | 4.5500 |
| Educational Services | 34 | 0.8300 | 0.9200 | 0.7824 | 0.1233 | 0.1097 | 0.5322 | 0.3434 | 0.2517 | 0.2080 | 0.1291 | 0.1186 | 1.3138 | -0.0782 | 0.0283 | 0.0807 | 2.6600 | 1.1400 |
| Electric Util. (Central) | 21 | 0.7500 | 0.4800 | 0.2337 | 0.8616 | 0.4628 | 0.1077 | 0.0638 | 0.3182 | 0.1772 | 0.1158 | 0.0889 | 1.5854 | 0.0898 | 0.6388 | 0.5689 | 0.5500 | 2.2600 |
| Electric Utility (East) | 21 | 0.7000 | 0.4900 | 0.1830 | 0.6616 | 0.3982 | 0.1191 | 0.0689 | 0.3314 | 0.1913 | 0.1266 | 0.0977 | 2.0107 | 0.0833 | 0.6622 | 0.8235 | 0.5400 | 2.5100 |
| Electric Utility (West) | 14 | 0.7500 | 0.4900 | 0.1985 | 0.8454 | 0.4581 | 0.0988 | 0.0611 | 0.3130 | 0.1679 | 0.1138 | 0.0853 | 2.1061 | -0.0059 | 0.5670 | 1.1743 | 0.5400 | 2.1900 |
| Electrical Equipment | 68 | 1.3300 | 1.3500 | 0.6776 | 0.1266 | 0.1124 | 0.2302 | 0.1503 | 0.1702 | 0.1319 | 0.0995 | 0.1212 | 0.8614 | 0.1228 | 0.2940 | 0.0917 | 1.5100 | 1.5400 |
| Electronics | 139 | 1.0700 | 1.0800 | 0.8993 | 0.2233 | 0.1825 | 0.2220 | 0.1572 | 0.1036 | 0.0599 | 0.0448 | 0.0463 | 1.0397 | 0.1063 | 0.1197 | 0.1861 | 3.5100 | 0.4700 |
| Engineering & Const | 25 | 1.2200 | 1.3900 | 0.6503 | 0.1199 | 0.1071 | 0.1544 | 0.1358 | 0.2626 | 0.0472 | 0.0335 | 0.0347 | 0.8423 | 0.0330 | 0.0631 | -0.0901 | 4.0500 | 0.4600 |
| Entertainment | 77 | 1.6300 | 1.3100 | 1.0837 | 0.4099 | 0.2907 | 0.1146 | 0.0945 | 0.1538 | 0.1772 | 0.1217 | 0.1012 | 0.7938 | 0.0172 | 0.2584 | -0.0930 | 0.7800 | 1.8900 |
| Entertainment Tech | 40 | 1.2300 | 1.4800 | 0.7691 | 0.0976 | 0.0889 | 0.1508 | 0.1169 | 0.1159 | 0.1048 | 0.0904 | 0.0962 | 0.7889 | -0.1791 | 0.1157 | -0.2503 | 1.2900 | 1.8700 |
| Environmental | 82 | 0.8100 | 0.6000 | 0.9214 | 0.4370 | 0.3041 | 0.1100 | 0.0756 | 0.1171 | 0.1522 | 0.0948 | 0.0753 | 0.9646 | 0.0048 | 0.4673 | -0.0026 | 0.8000 | 2.0700 |
| Financial Svcs. (Div.) | 225 | 1.3100 | 0.5000 | 0.8227 | 2.5149 | 0.7155 | -3.0309 | 0.0595 | 0.1918 | 0.4349 | 0.3384 | 0.0508 | 3.1233 | 0.1108 | NA | 0.1338 | 0.1800 | 6.6700 |
| Food Processing | 112 | 0.9100 | 0.7700 | 0.6068 | 0.2953 | 0.2280 | 0.1785 | 0.1188 | 0.2000 | 0.0908 | 0.0652 | 0.0536 | 1.3977 | 0.0801 | 0.4525 | 0.2588 | 1.8200 | 1.0800 |
| Foreign Electronics | 9 | 1.0900 | 1.2400 | 0.3540 | 0.4209 | 0.2962 | 0.0625 | 0.0783 | 0.3512 | 0.0527 | 0.0323 | 0.0183 | 0.7366 | 0.0147 | 0.5137 | -0.3915 | 2.4300 | 0.3700 |
| Funeral Services | 6 | 1.1400 | 0.8500 | 0.3935 | 0.5660 | 0.3614 | 0.1234 | 0.0781 | 0.3084 | 0.1564 | 0.0982 | 0.0748 | 0.7863 | 0.0376 | 0.4981 | -0.0351 | 0.7900 | 1.8600 |
| Furn/Home Furnishings | 35 | 1.8100 | 1.6500 | 0.8090 | 0.2439 | 0.1961 | 0.1166 | 0.0950 | 0.2043 | 0.0643 | 0.0458 | 0.0376 | 0.6582 | 0.1345 | 0.2783 | -0.1243 | 2.0800 | 0.9200 |
| Healthcare Information | 25 | 1.1700 | 1.2000 | 0.6579 | 0.0635 | 0.0597 | 0.1100 | 0.0945 | 0.2219 | 0.1211 | 0.0764 | 0.0881 | 0.5833 | 0.0200 | 0.1222 | -0.4014 | 1.2400 | 3.8200 |
| Heavy Truck & Equip | 21 | 1.8000 | 1.4800 | 0.6992 | 0.4366 | 0.3039 | 0.3024 | 0.1088 | 0.2062 | 0.0913 | 0.0664 | 0.0848 | 0.9981 | 0.2435 | 0.3422 | 0.9467 | 1.6400 | 1.3400 |
| Homebuilding | 23 | 1.4500 | 1.0200 | 0.7000 | 1.0028 | 0.5007 | -0.3582 | -0.0209 | 0.0512 | -0.0156 | -0.0209 | -0.0564 | 0.5980 | 0.7653 | NA | NA | 1 | 1.2300 |
| Hotel/Gaming | 51 | 1.7400 | 1.2800 | 0.7909 | 0.5207 | 0.3424 | 0.0564 | 0.0695 | 0.1453 | 0.1261 | 0.1013 | 0.0629 | 1.0945 | -0.0212 | 0.4037 | -0.0079 | 0.6900 | 2.5800 |
| Household Products | 26 | 1.0700 | 0.9500 | 0.6224 | 0.1899 | 0.1596 | 0.2180 | 0.1452 | 0.2512 | 0.1738 | 0.1279 | 0.1166 | 1.1715 | 0.0470 | 0.4897 | 0.0597 | 1.1300 | 2.2100 |
| Human Resources | 23 | 1.2400 | 1.4000 | 0.7827 | 0.1031 | 0.0935 | 0.0725 | 0.0767 | 0.2535 | 0.0191 | 0.0118 | 0.0166 | 0.6960 | 0.0481 | 0.5059 | 0.2753 | 6.4800 | 0.2900 |
| Industrial Services | 137 | 0.9300 | 0.8100 | 0.7443 | 0.3271 | 0.2465 | 0.1376 | -0.5350 | 0.1903 | -0.2140 | -0.2367 | 0.0326 | 1.2745 | 0.1025 | 0.2498 | NA | 2.2600 | 0.8500 |
| Information Services | 27 | 1.0700 | 0.8900 | 0.4810 | 0.3021 | 0.2320 | 0.1560 | 0.1083 | 0.1893 | 0.1933 | 0.1506 | 0.1194 | 0.6440 | -0.0161 | 0.3873 | -0.2397 | 0.7200 | 2.9400 |
| Insurance (Life) | 30 | 1.5800 | 1.5400 | 0.5335 | 0.6414 | 0.3908 | 0.1045 | NA | 0.2804 | NA | NA | NA | NA | NA | 0.2939 | 0.0024 | NA | NA |
| Insurance (Prop/Cas.) | 49 | 0.9100 | 1.0100 | 0.3788 | 0.2360 | 0.1910 | 0.1332 | NA | 0.1936 | NA | NA | NA | 98.1235 | NA | 0.2346 | 0.5773 | NA | NA |
| Internet | 186 | 1.0900 | 1.2400 | 1.1709 | 0.0271 | 0.0263 | 0.3973 | 0.3275 | 0.0687 | 0.1825 | 0.1458 | 0.1600 | 1.5437 | -0.0844 | 0.0066 | 0.0482 | 2.2500 | 3.9100 |
| IT Services | 60 | 1.0600 | 1.1400 | 0.6945 | 0.0609 | 0.0574 | 0.3611 | 0.2695 | 0.1915 | 0.1443 | 0.1032 | 0.1059 | 0.7610 | 0.0288 | 0.3287 | -0.0473 | 2.6100 | 1.7500 |
| Machinery | 100 | 1.2000 | 1.1400 | 0.5721 | 0.1912 | 0.1605 | 0.1459 | 0.1260 | 0.2215 | 0.1105 | 0.0822 | 0.0726 | 0.7532 | 0.1627 | 0.2538 | 0.0844 | 1.5300 | 1.3700 |
| Maritime | 52 | 1.4000 | 0.5800 | 0.6919 | 1.7038 | 0.6301 | 0.0488 | 0.0476 | 0.0555 | 0.1481 | 0.1369 | 0.0078 | 3.1685 | 0.0332 | 0.2525 | 2.1504 | 0.3500 | 2.6900 |
| Med Supp Invasive | 83 | 0.8500 | 0.8000 | 0.7918 | 0.1608 | 0.1385 | 0.2213 | 0.1588 | 0.1186 | 0.2222 | 0.1728 | 0.1664 | 0.8488 | 0.2214 | 0.2291 | 0.0150 | 0.9200 | 2.5200 |
| Med Supp Non-Invasive | 146 | 1.0300 | 1.0700 | 0.8489 | 0.1302 | 0.1152 | 0.2956 | 0.1924 | 0.1273 | 0.0648 | 0.0481 | 0.0489 | 0.7877 | 0.0304 | 0.3729 | -0.0321 | 4 | 0.7300 |
| Medical Services | 122 | 0.9100 | 0.7800 | 0.7626 | 0.4945 | 0.3309 | 0.3281 | 0.1855 | 0.1993 | 0.1111 | 0.0739 | 0.0484 | 0.9190 | -0.0559 | 0.0882 | -0.2553 | 2.5100 | 0.6800 |
| Metal Fabricating | 24 | 1.5900 | 1.6300 | 0.6898 | 0.1549 | 0.1341 | 0.1866 | 0.1478 | 0.2655 | 0.1507 | 0.1089 | 0.0784 | 1.5415 | 0.1802 | 0.2570 | 0.3262 | 1.3600 | 1.6700 |
| Metals & Mining (Div.) | 73 | 1.3300 | 1.2800 | 1.0438 | 0.1410 | 0.1236 | 0.2479 | 0.1948 | 0.1104 | 0.3157 | 0.2188 | 0.0736 | 1.5810 | 0.0622 | 0.3351 | 0.2326 | 0.8900 | 2.4700 |
| Natural Gas (Div.) | 29 | 1.3300 | 1.0600 | 0.4877 | 0.3707 | 0.2704 | 0.0904 | 0.0710 | 0.2198 | 0.2894 | 0.1750 | 0.1272 | 2.9708 | -0.0426 | 0.3381 | 2.7648 | 0.4100 | 3.3700 |
| Natural Gas Utility | 22 | 0.6600 | 0.4600 | 0.2490 | 0.6738 | 0.4026 | 0.1098 | 0.0809 | 0.3016 | 0.1280 | 0.0857 | 0.0510 | 1.8403 | 0.0553 | 0.6728 | 0.4996 | 0.9400 | 1.4500 |
| Newspaper | 13 | 1.7600 | 1.4200 | 0.9074 | 0.4635 | 0.3167 | 0.1673 | 0.1105 | 0.2513 | 0.1459 | 0.0902 | 0.0311 | 0.4560 | -0.0313 | 0.1456 | -0.3230 | 1.2300 | 1.3100 |
| Office Equip/Supplies | 24 | 1.3800 | 1.0400 | 0.6426 | 0.6303 | 0.3866 | 0.1805 | 0.1036 | 0.2105 | 0.0665 | 0.0459 | 0.0407 | 0.6117 | 0.0678 | 0.2806 | -0.2089 | 2.2600 | 0.5500 |
| Oil/Gas Distribution | 13 | 0.9600 | 0.6500 | 0.5661 | 0.5830 | 0.3683 | 0.1135 | 0.0683 | 0.1370 | 0.1845 | 0.1446 | 0.0980 | 2.8022 | -0.0001 | 0.7398 | 1.2400 | 0.4700 | 3.5600 |
| Oilfield Svcs/Equip. | 93 | 1.5500 | 1.3900 | 0.6237 | 0.2292 | 0.1864 | 0.1048 | 0.0854 | 0.1739 | 0.1511 | 0.1128 | 0.1072 | 1.4322 | 0.1689 | 0.4188 | 0.7061 | 0.7600 | 2.3800 |
| Packaging & Container | 26 | 1.1600 | 0.8800 | 0.4159 | 0.5182 | 0.3413 | 0.1752 | 0.1040 | 0.2423 | 0.1012 | 0.0702 | 0.1346 | 0.9261 | 0.0901 | 0.2438 | 1.0881 | 1.4800 | 1.0600 |
| Paper/Forest Products | 32 | 1.3600 | 0.9600 | 0.9384 | 0.5986 | 0.3745 | 0.0840 | 0.1101 | 0.1061 | 0.1201 | 0.0984 | 0.0463 | 0.5463 | 0.1019 | 0.4321 | -0.2689 | 1.1200 | 1.0600 |
| Petroleum (Integrated) | 20 | 1.1800 | 1.1200 | 0.3899 | 0.1919 | 0.1610 | 0.1476 | 0.1008 | 0.2741 | 0.0976 | 0.0565 | 0.0799 | 1.9287 | 0.0198 | 0.3899 | 0.8767 | 1.7800 | 0.8700 |
| Petroleum (Producing) | 176 | 1.3400 | 1.1300 | 0.8811 | 0.2488 | 0.1992 | 0.0946 | 0.1350 | 0.1114 | 0.2574 | 0.1910 | 0.1069 | 1.9231 | 0.0228 | 0.0950 | 0.6409 | 0.7100 | 2.2000 |
| Pharmacy Services | 19 | 1.1200 | 1 | 0.5943 | 0.2048 | 0.1700 | 0.1482 | 0.1118 | 0.2467 | 0.0511 | 0.0314 | 0.0291 | 0.9952 | 0.0368 | 0.2026 | 0.0555 | 3.5600 | 0.5300 |
| Pipeline MLPs | 27 | 0.9800 | 0.7200 | 0.3490 | 0.4097 | 0.2906 | 0.1271 | 0.0860 | 0.0637 | 0.0895 | 0.0868 | 0.0711 | 1.8461 | 0.0088 | 0.3353 | 0.4379 | 0.9900 | 1.9700 |
| Power | 93 | 1.3500 | 0.6500 | 0.9719 | 1.4882 | 0.5981 | 0.0695 | 0.0756 | 0.0866 | 0.1454 | 0.1088 | 0.0149 | 1.8113 | 0.1094 | 0.1375 | 0.6425 | 0.6900 | 1.4800 |
| Precious Metals | 84 | 1.1500 | 1.1400 | 0.9087 | 0.0820 | 0.0757 | 0.0909 | 0.0957 | 0.0751 | 0.3330 | 0.2402 | 0.3024 | 2.0300 | 0.0721 | 0.2671 | 0.6224 | 0.4000 | 5.3300 |
| Precision Instrument | 77 | 1.2800 | 1.3300 | 0.6533 | 0.1594 | 0.1375 | 0.1537 | 0.1210 | 0.1394 | 0.1074 | 0.0880 | 0.0957 | 0.4846 | 0.1514 | 0.1124 | 0.0204 | 1.3800 | 1.6400 |
| Property Management | 31 | 1.1300 | 0.5900 | 0.8221 | 1.4063 | 0.5844 | 0.1074 | 0.0518 | 0.1859 | 0.1563 | 0.1295 | 0.0918 | 2.2763 | -0.0302 | 0.2766 | 1.3737 | 0.4000 | 2.8500 |
| Public/Private Equity | 11 | 2.1800 | 1.6200 | 0.7754 | 0.5987 | 0.3745 | 0.3596 | -0.0014 | 0.0379 | -0.0258 | -0.0048 | 0.6230 | 5.5433 | 0.3162 | 0.1728 | NA | 0.3000 | 3.4300 |
| Publishing | 24 | 1.2500 | 0.8900 | 0.6498 | 0.6328 | 0.3876 | 0.3194 | 0.1138 | 0.1855 | 0.1210 | 0.0833 | 0.0622 | 0.7565 | 0.0081 | 0.2502 | -0.0851 | 1.3700 | 1.1500 |
| R.E.I.T. | 5 | 1.4700 | 1.1500 | 0.4961 | 0.3471 | 0.2577 | 0.1558 | 0.1407 | 0.0104 | 1.2907 | 1.2601 | 1.1355 | 0.8950 | -0.1012 | 0.9136 | -0.0196 | 0.1100 | 14.1300 |
| Railroad | 12 | 1.4400 | 1.2400 | 0.4295 | 0.2515 | 0.2009 | 0.1643 | 0.1110 | 0.2374 | 0.2843 | 0.1856 | 0.1786 | 1.7552 | -0.0176 | 0.3463 | 0.3617 | 0.6000 | 3.4400 |
| Recreation | 56 | 1.4500 | 1.1100 | 0.7055 | 0.4869 | 0.3275 | 0.1106 | 0.0826 | 0.1737 | 0.1151 | 0.0926 | 0.0728 | 1.7470 | -0.0096 | 0.4267 | 0.5056 | 0.8900 | 1.6000 |
| Reinsurance | 13 | 0.9300 | 1.0500 | 0.3040 | 0.2354 | 0.1906 | 0.1329 | NA | 0.0722 | NA | NA | NA | NA | NA | 0.1587 | 0.5050 | NA | NA |
| Restaurant | 63 | 1.2700 | 1.1900 | 0.6837 | 0.1277 | 0.1132 | 0.3825 | 0.2032 | 0.2157 | 0.1582 | 0.1117 | 0.1070 | 1.2428 | -0.0482 | 0.4673 | 0.0836 | 1.8200 | 2.5000 |
| Retail (Hardlines) | 75 | 1.7700 | 1.6500 | 0.9279 | 0.2433 | 0.1957 | 0.2291 | 0.1499 | 0.2304 | 0.0750 | 0.0499 | 0.0386 | 2.1962 | 0.0840 | 0.1962 | 0.8640 | 3 | 0.8300 |
| Retail (Softlines) | 47 | 1.4400 | 1.5700 | 0.6091 | 0.0561 | 0.0532 | 0.3627 | 0.2874 | 0.2464 | 0.0939 | 0.0582 | 0.0556 | 0.9655 | 0.0340 | 0.2108 | 0.0099 | 4.9400 | 0.8700 |
| Retail Automotive | 20 | 1.3700 | 1.1200 | 0.5202 | 0.3811 | 0.2759 | 0.2053 | 0.0989 | 0.3443 | 0.0688 | 0.0446 | 0.0435 | 1.4044 | 0.1356 | 0.0249 | 0.4076 | 2.2200 | 0.9200 |
| Retail Building Supply | 8 | 1.0400 | 0.9700 | 0.3761 | 0.1406 | 0.1233 | 0.1606 | 0.1218 | 0.3139 | 0.0813 | 0.0513 | 0.0514 | 0.7827 | 0.0588 | 0.4732 | -0.0628 | 2.3700 | 1.0400 |
| Retail Store | 37 | 1.2900 | 1.1400 | 0.6771 | 0.2558 | 0.2037 | 0.2101 | 0.1360 | 0.2502 | 0.0584 | 0.0383 | 0.0345 | 1.2902 | 0.0088 | 0.2916 | 0.1497 | 3.5500 | 0.5900 |
| Retail/Wholesale Food | 30 | 0.7500 | 0.6400 | 0.4002 | 0.4134 | 0.2925 | 0.1643 | 0.1038 | 0.3121 | 0.0318 | 0.0207 | 0.0416 | 1.2058 | -0.0001 | 0.2862 | 0.2306 | 5.0200 | 0.3500 |
| Securities Brokerage | 28 | 1.2000 | 0.4300 | 0.4431 | 4.3056 | 0.8115 | NA | 0.1039 | 0.2622 | 0.4878 | 0.3558 | 0.1145 | 0.8669 | 1.2316 | 0.1093 | -1.2666 | 0.2900 | 3.0800 |
| Semiconductor | 141 | 1.5000 | 1.6900 | 0.7052 | 0.0835 | 0.0770 | 0.3910 | 0.2841 | 0.1101 | 0.2276 | 0.1813 | 0.1782 | 1.0832 | 0.0693 | 0.3053 | 0.0583 | 1.5700 | 2.0600 |
| Semiconductor Equip | 12 | 1.7900 | 2.4200 | 0.6870 | 0.1520 | 0.1320 | 0.6576 | 0.4044 | 0.1517 | 0.2165 | 0.1830 | 0.1630 | 1.0587 | 0.1251 | 0.1130 | 0.0258 | 2.2100 | 0.9700 |
| Shoe | 19 | 1.2500 | 1.3800 | 0.5552 | 0.0218 | 0.0213 | 0.3049 | 0.2741 | 0.2431 | 0.1134 | 0.0822 | 0.0844 | 1.2384 | 0.1628 | 0.2589 | 0.1907 | 3.3300 | 1.5200 |
| Steel | 32 | 1.6800 | 1.4000 | 0.5694 | 0.4640 | 0.3169 | 0.0728 | 0.0594 | 0.2103 | 0.0583 | 0.0490 | 0.0352 | 0.6643 | 0.1141 | 0.3426 | -0.0639 | 1.2100 | 0.7800 |
| Telecom. Equipment | 99 | 1.0200 | 1.2800 | 0.8777 | 0.1296 | 0.1148 | 0.2993 | 0.2330 | 0.1316 | 0.1087 | 0.0853 | 0.0722 | 0.6098 | -0.0338 | 0.5372 | -0.2125 | 2.7300 | 1.2500 |
| Telecom. Services | 74 | 0.9800 | 0.8200 | 0.6858 | 0.3409 | 0.2542 | 0.1647 | 0.1370 | 0.1422 | 0.2274 | 0.1656 | 0.0511 | 0.9555 | -0.1238 | 0.4363 | -0.0554 | 0.8300 | 1.8500 |
| Telecom. Utility | 25 | 0.8800 | 0.5400 | 0.6040 | 0.9615 | 0.4902 | 0.1829 | 0.0834 | 0.2942 | 0.1583 | 0.1121 | 0.0850 | 0.7644 | -0.0776 | 0.8094 | -0.3732 | 0.7400 | 1.7500 |
| Thrift | 148 | 0.7100 | 0.7500 | 0.5393 | 0.2933 | 0.2268 | -0.0214 | NA | 0.1243 | NA | NA | NA | NA | NA | NA | 0 | NA | NA |
| Tobacco | 11 | 0.8500 | 0.7800 | 0.4153 | 0.1871 | 0.1576 | 0.7421 | 0.2798 | 0.3103 | 0.2061 | 0.1524 | 0.0846 | 0.6469 | -0.0244 | 0.6756 | -0.0420 | 1.8400 | 2.3600 |
| Toiletries/Cosmetics | 15 | 1.3000 | 1.2000 | 0.6034 | 0.2064 | 0.1711 | 0.6253 | 0.1954 | 0.2030 | 0.1085 | 0.0724 | 0.0737 | 1.1416 | 0.0855 | 0.2504 | 0.1339 | 2.7000 | 1.4800 |
| Trucking | 36 | 1.2400 | 1.0800 | 0.5988 | 0.2777 | 0.2173 | 0.0819 | 0.0907 | 0.2548 | 0.0637 | 0.0420 | 0.0274 | 1.5692 | 0.0503 | 0.4107 | 0.9407 | 2.1600 | 1.2800 |
| Utility (Foreign) | 4 | 0.9600 | 0.4800 | 0.3268 | 1.5503 | 0.6079 | 0.0312 | 0.0456 | 0.2607 | 0.1160 | 0.0781 | 0.0055 | 1.6469 | 0.0752 | 0.0032 | 1.3229 | 0.5800 | 1.3900 |
| Water Utility | 11 | 0.6600 | 0.4300 | 0.1889 | 0.8142 | 0.4488 | 0.0844 | 0.0542 | 0.3522 | 0.2661 | 0.1805 | 0.1225 | 2.5002 | 0.0751 | 0.4816 | 1.0715 | 0.3000 | 4.3900 |
| Wireless Networking | 57 | 1.2700 | 1.1200 | 0.7503 | 0.2706 | 0.2130 | 0.2134 | -0.1821 | 0.1212 | -0.1147 | -0.1591 | 0.0796 | 0.8553 | 0.0762 | 0.0913 | NA | 1.1400 | 1.9100 |
| Total Market | 5891 | 1.1500 | 0.9200 | 0.7508 | 0.4664 | 0.3181 | 0.1607 | 0.1221 | 0.1548 | 0.1724 | 0.1262 | 0.0832 | 1.2547 | 0.0701 | 0.3792 | 0.0865 | 0.9700 | 1.6700 |

---

### model.xls

**Purpose:** A questionnaire ("CHOOSING THE RIGHT VALUATION MODEL") that maps a firm's characteristics to the appropriate valuation approach: DCF vs option-pricing, current vs normalized earnings, dividends vs FCFE vs FCFF, length of the growth period, and stable vs 2-stage vs 3-stage growth pattern. Damodaran ships it as the front door to his model library. Single sheet; values only, so the decision rules below are (inferred) from his published decision tree and the one worked case in the file.

**Inputs:**

| Label | Cell | Example |
|---|---|---|
| Are your earnings positive? (Yes/No) | D8 | Yes |
| Expected inflation rate in the economy | E11 | 0.03 |
| Expected real growth rate in the economy | E12 | 0.02 |
| Expected near-term growth rate in earnings (revenues) for this firm | F14 | 0.15 |
| Significant and sustainable competitive advantage? (Yes/No) | F15 | Yes |
| If earnings negative: because cyclical? / one-time? / too much debt? / (if debt) bankruptcy likely? / just starting up? | G22–G26 area | blank (earnings positive) |
| Current debt ratio (market value) | F28 | 0.04 |
| Is the debt ratio expected to change significantly? (Yes/No) | F29 | Yes |
| Dividends paid in current year | F32 | 100 |
| Can you estimate capex and working-capital needs? (Yes/No) | F33 | Yes |
| Net Income / D&A / Capital Spending (incl. acquisitions) / Δ non-cash WC | E35–E38 | 200 / 50 / 100 / 25 |

**Logic:** Nominal economy growth = inflation + real growth = 5% (inferred benchmark). FCFE formula is printed verbatim on the sheet: `FCFE = NI − (Capital Spending − Depreciation)×(1 − Debt Ratio) − ΔWC×(1 − Debt Ratio)` = 200 − 50×0.96 − 25×0.96 = 128 (G40).

Decision rules (all inferred from Damodaran's published tree; only the Yes-path is confirmed by the file):
1. **Model type:** DCF, unless earnings are negative because of too much debt AND bankruptcy is likely → option-pricing model (value equity as a call on the firm's assets; the sheet note says: if option pricing, first do a DCF valuation).
2. **Earnings level:** positive → current earnings. Negative and cyclical/one-time/leverage-driven → normalized earnings. Negative because start-up → current earnings with a revenue-driven margin recovery (the higrowth model).
3. **Cash flow to discount:** cannot estimate capex/WC → dividends. Can estimate, debt ratio stable → FCFE. Debt ratio expected to change → FCFF (the example: change = Yes → "FCFF (Value firm)").
4. **Growth period:** firm growth > economy growth AND sustainable advantage → "10 or more years" (example). Advantage not sustainable → 5–10 years. Growth ≤ economy → less than 5 / none.
5. **Growth pattern:** growth ≤ economy → Stable. Moderately above → 2-stage. Far above (15% vs 5% here) with shifting leverage → "Three-stage Growth" (example). Sheet note verbatim: in an n-stage model you estimate target operating margins (firm valuation) or net margins (equity valuation) and revenue growth each year.

**Outputs:** F44 model type = "Discounted CF Model"; F45 earnings level = "Current Earnings"; F46 cash flow = "FCFF (Value firm)"; F47 growth period = "10 or more years"; F48 pattern = "Three-stage Growth"; G40 FCFE = 128.

**Worked example:** positive earnings, 15% growth vs 5% nominal economy, sustainable advantage, 4% debt ratio expected to change → DCF, current earnings, FCFF, 10+ years, three-stage. FCFE = 128 vs dividends of 100 (the FCFE-vs-dividends comparison flags that the firm pays out less than it could).

**Reimplementation:** a pure decision function. Inputs: earnings_positive (bool), inflation, real_growth, firm_growth (floats), sustainable_advantage (bool), negative_reason flags (cyclical, one_time, leverage, bankruptcy_likely, startup — bools), debt_ratio, debt_ratio_changing (bool), dividends, can_estimate_capex (bool), ni, dep, capex, delta_wc. Outputs: the five categorical outputs plus fcfe. Thresholds to parameterize: what counts as "moderately above" the economy for 2-stage vs 3-stage (the file does not pin it; Damodaran's rule of thumb is < ~2× the economy's nominal growth for 2-stage — mark configurable). Edge cases: contradictory flags (earnings positive but negative-reason flags set) → ignore the negative branch; missing capex data forces the dividends branch regardless of leverage answers.

---

### revgrowth.xls

**Purpose:** Estimates a young firm's revenue path top-down: start with the total market, grow it, and apply target market shares at years 5 and 10 ("Market Share approach"). It converts big-market/small-share stories into concrete revenue CAGRs to feed models like higrowth.xls. Sheets `Direct Inputs` and `Sheet3` are empty stubs (skipped).

**Inputs (`Market Share approach` sheet):**

| Label | Cell | Example |
|---|---|---|
| Revenues in current year | B2 | 100 |
| Size of overall market in current year | B3 | 100000 |
| Expected growth rate in overall market | B4 | 0.03 |
| Expected market share in 5 years | B5 | 0.025 |
| Expected market share in 10 years | B6 | 0.06 |

**Logic (inferred, verified):**
- Market_t = Market_0 × (1+g_mkt)^t
- Rev_5 (B9) = Market_0 × (1+g_mkt)^5 × share_5 = 100000×1.03^5×0.025 = 2898.185
- Rev_10 (B11) = Market_0 × (1+g_mkt)^10 × share_10 = 100000×1.03^10×0.06 = 8063.498
- CAGR yrs 1–5 (B10) = (Rev_5/Rev_0)^(1/5) − 1 = 0.960764
- CAGR yrs 6–10 (B12) = (Rev_10/Rev_5)^(1/5) − 1 = 0.227099
- CAGR yrs 1–10 (B13) = (Rev_10/Rev_0)^(1/10) − 1 = 0.551145

**Outputs:** B9, B11 (revenues at years 5 and 10); B10, B12, B13 (the three CAGRs).

**Worked example:** a firm with 100 in revenue (0.1% share of a 100,000 market growing 3%/yr) that reaches 2.5% share by year 5 and 6% by year 10 must grow revenue 96.1%/yr for five years, then 22.7%/yr — 55.1%/yr compounded over the decade.

**Reimplementation:** trivial closed-form function. Inputs: rev0, market0, g_mkt, share_5, share_10 (floats). Outputs: rev5, rev10, cagr_1_5, cagr_6_10, cagr_1_10. Edge cases: rev0 = 0 → CAGRs undefined (raise); shares outside (0,1] should warn; share_10 < share_5 is allowed (declining share still computes). Generalize to arbitrary (year, share) pairs: rev_t = market0×(1+g_mkt)^t×share_t, CAGR between consecutive milestones = (rev_b/rev_a)^(1/(b−a)) − 1.
