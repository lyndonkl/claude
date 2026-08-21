# US industry-average multiples and companion variables

**Core idea:** Applying any multiple needs two numbers from the peer universe: the typical multiple, and the typical value of its companion variable. Damodaran's annual US industry-averages dataset supplies both in one place. For each of 94 industries plus two market aggregates it reports the pricing multiples (EV/Sales, EV/EBITDA, EV/EBIT, Price/Book, Trailing PE) next to the fundamentals that justify them (margins, ROC, ROE, revenue growth, capital turnover, tax rate, beta, cost of capital, payout, reinvestment). That pairing is the point. A sector multiple read without its companion variable is a number with no meaning. The version reproduced here is the January 2022 US dataset.

**Formulas:** none of its own. It feeds the intrinsic and regression formulas in the other concepts:
- Justified EV/Sales = ATOM × (1 − RIR)/(WACC − g) — check the industry's operating margin.
- Justified PBV = (ROE − g)/(r − g) — check the industry's ROE.
- Justified EV/IC = (ROC − g)/(WACC − g) — check the industry's after-tax ROC.
- Justified EV/EBITDA falls with the tax rate and with CapEx/EBITDA — check the industry's reinvestment.

**Procedure:**
1. Identify the company's industry, using the business it actually operates in rather than its listing classification.
2. Read the industry's multiple *and* its companion variable from the table.
3. Compare the company's own companion variable with the industry average. A company with a higher margin, ROE or ROC than its industry deserves a higher multiple than the industry average, and the reverse.
4. Scale the industry multiple by that gap, or use the regional regressions for a formal control ([[cross-market-multiple-regressions]]).
5. Sanity-check the industry multiple against the current cross-sectional distribution ([[multiple-distribution-statistics]]) — these are averages, and averages of multiples are pulled up by outliers.
6. Skip earnings multiples where the industry average is NA or absurd. Banks and insurers have no meaningful EV/EBITDA, since debt is raw material rather than financing; use equity multiples for them.
7. For a business with several divisions, price each division against its own industry row and add the pieces.

**Reference data — US industry averages, January 2022.** Columns: number of firms; pricing multiples; then the companion variables (pre-tax operating margin, after-tax return on capital, ROE, five-year average annual revenue growth, sales/capital, effective tax rate, unlevered beta, cost of capital, dividend payout ratio). The full source table also carries equity beta, cost of equity, standard deviation in stock prices, pre-tax cost of debt, market debt/capital, non-cash working capital as a percent of revenues, CapEx and net CapEx as a percent of revenues, reinvestment rate, equity reinvestment rate, and a lease- and R&D-adjusted operating margin.

| Industry | # firms | EV/Sales | EV/EBITDA | EV/EBIT | P/BV | Trailing PE | Pre-tax op margin | After-tax ROC | ROE | Rev growth 5y | Sales/Cap | Eff tax rate | Unlev beta | Cost of capital | Payout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 47 | 1.94 | 9.20 | 15.12 | 5.98 | 23.77 | 12.07% | 63.51% | 26.08% | 18.98% | 5.43 | 24.14% | 0.93 | 6.35% | 101.33% |
| Aerospace/Defense | 77 | 2.27 | 14.94 | 19.77 | 6.09 | 44.26 | 11.37% | 33.93% | 31.42% | 3.53% | 3.15 | 19.06% | 1.08 | 7.18% | 44.14% |
| Air Transport | 18 | 1.34 | 6.54 | 12.00 | 2.34 | 10.55 | 11.60% | 13.69% | 28.20% | 4.84% | 1.50 | 23.04% | 0.84 | 5.86% | 15.08% |
| Apparel | 51 | 1.89 | 10.93 | 17.56 | 3.73 | 54.57 | 10.58% | 16.34% | 16.72% | -2.56% | 1.72 | 15.61% | 0.83 | 6.04% | 43.05% |
| Auto & Truck | 13 | 1.26 | 14.39 | 36.55 | 1.82 | 16.76 | 3.41% | 2.89% | 12.43% | 14.31% | 0.87 | 5.54% | 0.53 | 4.40% | 51.58% |
| Auto Parts | 46 | 0.75 | 6.38 | 10.18 | 1.95 | 17.58 | 7.24% | 17.00% | 12.56% | 4.98% | 2.46 | 18.52% | 0.95 | 6.37% | 26.31% |
| Bank (Money Center) | 7 | 7.28 | NA | NA | 1.27 | 10.23 | 0.00% | -0.03% | 12.80% | 2.11% | 0.20 | 17.74% | 0.56 | 3.87% | 27.40% |
| Banks (Regional) | 611 | 5.95 | NA | NA | 1.37 | 15.41 | 0.00% | -0.06% | 12.05% | 10.13% | 0.26 | 20.33% | 0.43 | 3.78% | 29.77% |
| Beverage (Alcoholic) | 21 | 4.62 | 16.32 | 20.87 | 2.99 | 38.69 | 22.11% | 14.95% | 6.88% | 10.77% | 0.72 | 18.39% | 0.92 | 6.58% | 67.00% |
| Beverage (Soft) | 34 | 4.88 | 19.92 | 23.73 | 8.05 | 39.87 | 20.40% | 26.21% | 40.25% | 30.75% | 1.33 | 9.76% | 1.09 | 7.37% | 57.44% |
| Broadcasting | 27 | 2.72 | 9.06 | 12.44 | 2.08 | 8.56 | 21.99% | 21.47% | 93.39% | 9.54% | 1.13 | 7.24% | 0.73 | 5.36% | 38.15% |
| Brokerage & Investment Banking | 39 | 6.17 | NA | NA | 1.27 | 18.05 | 0.55% | 0.04% | 14.06% | 6.66% | 0.20 | 19.96% | 0.57 | 4.37% | 22.21% |
| Building Materials | 42 | 1.60 | 12.28 | 17.36 | 3.99 | 25.42 | 9.01% | 18.65% | 14.05% | 12.31% | 2.42 | 24.83% | 1.02 | 6.90% | 26.75% |
| Business & Consumer Services | 165 | 2.39 | 14.00 | 22.57 | 5.00 | 47.54 | 10.19% | 21.94% | 10.24% | 9.57% | 2.28 | 20.24% | 0.89 | 6.37% | 73.82% |
| Cable TV | 14 | 3.44 | 10.12 | 18.55 | 2.61 | 80.57 | 17.95% | 12.15% | 11.76% | 3.78% | 0.79 | 21.22% | 0.78 | 5.74% | 23.15% |
| Chemical (Basic) | 43 | 1.30 | 8.24 | 15.40 | 2.12 | 16.11 | 8.30% | 11.68% | 9.16% | 6.78% | 1.50 | 25.88% | 0.99 | 6.65% | 90.86% |
| Chemical (Diversified) | 6 | 1.35 | 7.94 | 12.53 | 1.89 | 10.48 | 10.75% | 11.78% | 10.07% | -4.80% | 1.24 | 23.10% | 1.21 | 7.55% | 62.72% |
| Chemical (Specialty) | 94 | 2.09 | 10.56 | 16.38 | 2.61 | 25.34 | 12.57% | 12.93% | 5.68% | 6.78% | 1.13 | 25.43% | 0.96 | 6.70% | 63.99% |
| Coal & Related Energy | 22 | 0.62 | 2.25 | 6.33 | 0.86 | 10.30 | 6.63% | 12.70% | 11.59% | -11.69% | 1.86 | 2.65% | 1.05 | 6.33% | 16.81% |
| Computer Services | 106 | 1.28 | 10.36 | 15.92 | 3.81 | 29.13 | 7.65% | 24.89% | 17.29% | 15.83% | 3.37 | 24.76% | 0.95 | 6.50% | 52.14% |
| Computers/Peripherals | 48 | 3.23 | 15.13 | 20.80 | 11.03 | 28.92 | 15.51% | 22.64% | 39.99% | -1.92% | 1.52 | 15.80% | 1.64 | 9.90% | 26.84% |
| Construction Supplies | 44 | 1.68 | 10.50 | 13.98 | 3.41 | 39.58 | 11.93% | 15.98% | 24.78% | 4.33% | 1.57 | 22.15% | 1.10 | 7.13% | 28.55% |
| Diversified | 23 | 2.45 | 12.92 | 17.84 | 1.93 | 22.78 | 13.72% | 11.55% | 7.86% | 15.16% | 0.91 | 17.90% | 1.25 | 7.60% | 18.22% |
| Drugs (Biotechnology) | 503 | 7.33 | 13.29 | 45.77 | 7.08 | 77.56 | 11.25% | 8.64% | -0.94% | 31.89% | 0.43 | 14.88% | 1.39 | 8.60% | 0.10% |
| Drugs (Pharmaceutical) | 267 | 5.44 | 14.57 | 21.08 | 6.33 | 58.18 | 24.85% | 18.29% | 21.51% | 31.72% | 0.76 | 13.19% | 1.29 | 8.51% | 61.39% |
| Education | 35 | 2.59 | 14.46 | 29.27 | 2.51 | 22.20 | 8.75% | 10.85% | 12.90% | 2.76% | 1.31 | 28.48% | 1.36 | 8.30% | 4.56% |
| Electrical Equipment | 113 | 2.56 | 12.82 | 17.79 | 4.85 | 29.85 | 13.61% | 25.60% | 20.08% | 9.12% | 1.90 | 18.09% | 1.31 | 8.27% | 36.80% |
| Electronics (Consumer & Office) | 20 | 0.91 | 15.65 | NA | 2.76 | 64.24 | -1.27% | -2.12% | -10.11% | 5.86% | 1.87 | 62.78% | 1.25 | 7.56% | 0.00% |
| Electronics (General) | 153 | 1.99 | 13.07 | 21.69 | 3.27 | 125.82 | 8.87% | 13.97% | 11.29% | 7.86% | 1.63 | 18.68% | 1.07 | 7.11% | 24.67% |
| Engineering/Construction | 54 | 0.70 | 9.75 | 16.43 | 1.87 | 18.71 | 3.89% | 14.55% | 3.43% | 8.43% | 3.92 | 24.51% | 1.33 | 8.03% | 36.86% |
| Entertainment | 107 | 4.72 | 21.85 | 34.91 | 3.70 | 47.68 | 13.52% | 18.57% | 17.66% | 8.05% | 1.41 | 20.41% | 1.20 | 7.83% | 22.14% |
| Environmental & Waste Services | 82 | 3.08 | 13.93 | 24.91 | 4.29 | 735.05 | 12.10% | 20.00% | 10.68% | 21.03% | 1.69 | 20.97% | 1.05 | 7.13% | 53.46% |
| Farming/Agriculture | 31 | 1.08 | 13.92 | 23.76 | 2.55 | 73.19 | 4.02% | 6.27% | 9.14% | 0.02% | 1.59 | 21.18% | 0.63 | 5.10% | 56.24% |
| Financial Svcs. (Non-bank & Insurance) | 232 | 30.15 | NA | NA | 2.22 | 83.00 | 7.51% | 0.23% | 0.07% | 10.87% | 0.04 | 19.83% | 0.10 | 2.79% | 15.96% |
| Food Processing | 88 | 2.30 | 14.26 | 18.84 | 2.58 | 42.25 | 12.00% | 15.55% | 1.90% | 4.24% | 1.36 | 14.82% | 0.70 | 5.38% | 303.82% |
| Food Wholesalers | 17 | 0.60 | 13.95 | 22.22 | 5.93 | 47.98 | 2.72% | 16.82% | 15.51% | 22.86% | 6.78 | 19.17% | 0.66 | 5.22% | 50.64% |
| Furn/Home Furnishings | 35 | 1.11 | 9.27 | 14.80 | 2.21 | 14.79 | 7.09% | 13.36% | 16.97% | 9.71% | 1.96 | 22.03% | 0.82 | 5.96% | 24.22% |
| Green & Renewable Energy | 22 | 9.94 | 17.15 | 123.23 | 1.68 | 26.23 | 11.82% | 1.39% | -5.80% | 19.48% | 0.16 | 32.66% | 0.59 | 4.98% | 0.12% |
| Healthcare Products | 242 | 5.94 | 22.67 | 37.55 | 5.13 | 84.43 | 15.00% | 15.87% | 9.78% | 13.40% | 1.03 | 12.50% | 0.98 | 6.81% | 30.27% |
| Healthcare Support Services | 128 | 0.69 | 11.74 | 16.05 | 2.86 | 51.64 | 4.37% | 37.91% | 13.16% | 18.44% | 9.69 | 23.60% | 0.95 | 6.51% | 38.37% |
| Heathcare Information and Technology | 129 | 5.41 | 23.49 | 40.46 | 5.28 | 99.81 | 12.58% | 14.40% | 11.17% | 18.17% | 1.14 | 13.30% | 1.15 | 7.67% | 8.54% |
| Homebuilding | 32 | 1.21 | 10.95 | 11.89 | 1.63 | 16.26 | 10.15% | 11.25% | 15.26% | 33.64% | 1.33 | 23.56% | 0.66 | 5.07% | 7.26% |
| Hospitals/Healthcare Facilities | 36 | 1.63 | 9.37 | 15.60 | 6.32 | 38.94 | 10.76% | 15.31% | 62.13% | 5.20% | 1.59 | 21.48% | 0.63 | 5.15% | 23.62% |
| Hotel/Gaming | 65 | 3.78 | 12.74 | 20.31 | 3.85 | 134.20 | 19.22% | 11.64% | 16.23% | 8.35% | 0.72 | 17.42% | 0.91 | 6.31% | 54.30% |
| Household Products | 127 | 3.74 | 16.57 | 21.32 | 8.20 | 33.23 | 17.43% | 28.18% | 10.59% | 17.42% | 1.71 | 26.92% | 0.94 | 6.61% | 152.58% |
| Information Services | 69 | 9.17 | 26.35 | 32.25 | 6.58 | 46.23 | 28.28% | 41.52% | 30.52% | 13.12% | 1.59 | 18.86% | 1.03 | 7.06% | 24.91% |
| Insurance (General) | 19 | 1.95 | 10.27 | 15.89 | 1.48 | 67.57 | 12.18% | 9.61% | 7.42% | 7.80% | 0.93 | 21.42% | 0.59 | 4.81% | 42.05% |
| Insurance (Life) | 24 | 1.36 | 9.53 | 10.23 | 0.71 | 21.05 | 13.29% | 8.20% | 10.44% | 1.50% | 0.72 | 19.82% | 0.73 | 5.02% | 26.07% |
| Insurance (Prop/Cas.) | 51 | 1.49 | 11.40 | 13.80 | 1.53 | 29.60 | 10.67% | 10.48% | 10.58% | 7.05% | 1.14 | 19.78% | 0.59 | 4.74% | 35.82% |
| Investments & Asset Management | 192 | 4.58 | 21.98 | 25.79 | 1.68 | 79.94 | 17.46% | 7.31% | 13.31% | 0.90% | 0.46 | 17.26% | 0.86 | 5.57% | 49.33% |
| Machinery | 120 | 2.58 | 13.88 | 18.35 | 4.09 | 36.10 | 13.84% | 24.49% | 20.03% | 3.50% | 1.98 | 22.33% | 1.10 | 7.26% | 28.00% |
| Metals & Mining | 92 | 2.04 | 9.58 | 17.43 | 1.86 | 727.10 | 11.28% | 11.26% | 3.27% | 14.84% | 1.01 | 53.29% | 1.09 | 7.24% | 202.98% |
| Office Equipment & Services | 22 | 1.20 | 8.77 | 13.29 | 2.96 | 34.53 | 8.85% | 17.48% | 18.22% | 3.74% | 2.25 | 22.94% | 1.24 | 7.63% | 38.57% |
| Oil/Gas (Integrated) | 4 | 1.61 | 9.17 | 21.74 | 1.41 | 22.67 | 7.33% | 5.36% | 7.85% | -6.48% | 0.96 | 30.25% | 1.12 | 7.37% | 89.07% |
| Oil/Gas (Production and Exploration) | 269 | 2.71 | 4.89 | 13.29 | 1.19 | 8.66 | 19.87% | 9.03% | 6.36% | -3.73% | 0.46 | 19.37% | 1.08 | 7.14% | 27.36% |
| Oil/Gas Distribution | 24 | 4.44 | 12.87 | 20.68 | 1.58 | 69.41 | 20.90% | 7.99% | 3.91% | 14.94% | 0.40 | 22.34% | 0.62 | 4.96% | 303.21% |
| Oilfield Svcs/Equip. | 136 | 0.74 | 8.58 | 16.78 | 1.47 | 25.44 | 4.16% | 11.59% | -8.40% | 1.49% | 2.79 | 20.96% | 1.22 | 7.72% | 0.32% |
| Packaging & Container | 24 | 1.59 | 9.51 | 15.32 | 3.10 | 20.61 | 10.14% | 16.83% | 15.96% | 5.52% | 1.85 | 21.71% | 0.68 | 5.24% | 44.97% |
| Paper/Forest Products | 15 | 0.77 | 7.53 | 14.03 | 1.59 | 24.92 | 5.40% | 9.37% | 2.05% | 18.88% | 1.91 | 19.62% | 1.25 | 7.80% | 179.43% |
| Power | 52 | 4.11 | 12.03 | 22.73 | 2.01 | 23.74 | 18.32% | 6.48% | 5.71% | 3.50% | 0.41 | 17.05% | 0.38 | 3.71% | 97.59% |
| Precious Metals | 83 | 5.05 | 13.65 | 34.17 | 1.74 | 76.84 | 14.51% | 8.07% | 12.90% | 14.08% | 0.57 | 27.18% | 1.33 | 8.73% | 20.77% |
| Publishing & Newspapers | 31 | 1.07 | 9.18 | 19.77 | 1.59 | 28.05 | 5.43% | 10.47% | -3.79% | 0.13% | 2.14 | 25.95% | 0.76 | 5.45% | 0.80% |
| R.E.I.T. | 234 | 13.48 | 22.64 | 51.01 | 2.26 | 48.00 | 27.15% | 2.92% | 5.49% | 10.67% | 0.13 | 2.18% | 0.43 | 3.90% | 192.44% |
| Real Estate (Development) | 20 | 5.37 | 26.11 | 68.34 | 1.58 | 48.49 | 10.28% | 2.08% | 3.37% | -2.50% | 0.28 | 22.53% | 0.89 | 6.04% | 0.05% |
| Real Estate (General/Diversified) | 12 | 6.57 | 7.68 | 13.48 | 0.88 | 110.21 | 29.91% | 7.41% | 5.71% | 2.41% | 0.27 | 16.33% | 1.50 | 7.80% | 22.05% |
| Real Estate (Operations & Services) | 57 | 1.39 | 12.60 | 22.98 | 2.58 | 32.46 | 5.75% | 11.47% | 11.92% | 3.48% | 2.11 | 22.27% | 0.68 | 5.17% | 19.23% |
| Recreation | 63 | 2.35 | 13.31 | 23.24 | 6.04 | 30.51 | 9.58% | 14.08% | 4.27% | 5.47% | 1.63 | 23.58% | 0.75 | 5.64% | 264.95% |
| Reinsurance | 2 | 1.12 | 14.91 | 17.19 | 1.06 | 57.40 | 6.61% | 5.90% | 5.00% | 6.64% | 1.09 | 21.03% | 0.77 | 5.25% | 18.26% |
| Restaurant/Dining | 77 | 4.26 | 16.88 | 31.84 | NA | 38.00 | 15.69% | 19.08% | NA | 7.92% | 1.53 | 20.49% | 0.75 | 5.65% | 53.91% |
| Retail (Automotive) | 26 | 1.19 | 13.90 | 23.64 | 6.45 | 16.62 | 5.63% | 9.48% | 34.60% | 4.70% | 2.26 | 23.49% | 0.87 | 6.15% | 4.42% |
| Retail (Building Supply) | 17 | 2.03 | 13.60 | 18.57 | 43.05 | 238.80 | 11.20% | 28.83% | 94.81% | 6.34% | 3.10 | 25.15% | 1.15 | 7.71% | 53.71% |
| Retail (Distributors) | 80 | 1.40 | 12.66 | 16.14 | 2.96 | 897.32 | 8.35% | 13.57% | 16.47% | 7.23% | 1.79 | 23.22% | 0.89 | 6.37% | 28.91% |
| Retail (General) | 18 | 0.88 | 12.21 | 22.57 | 4.84 | 18.64 | 4.18% | 13.82% | 18.14% | 1.51% | 4.20 | 24.94% | 0.95 | 6.62% | 44.44% |
| Retail (Grocery and Food) | 13 | 0.49 | 8.93 | 25.37 | 2.69 | 395.14 | 2.29% | 7.13% | 18.11% | 5.57% | 4.26 | 24.14% | 0.35 | 3.74% | 34.19% |
| Retail (Online) | 70 | 3.42 | 22.82 | 53.48 | 13.50 | 243.82 | 6.71% | 9.99% | 22.41% | 18.27% | 1.65 | 14.32% | 1.16 | 7.68% | 3.60% |
| Retail (Special Lines) | 89 | 1.19 | 9.72 | 21.29 | 4.57 | 23.79 | 5.76% | 12.04% | 19.92% | 7.65% | 2.45 | 22.33% | 0.69 | 5.41% | 40.09% |
| Rubber& Tires | 4 | 0.74 | 5.93 | 12.44 | 0.80 | 21.55 | 5.51% | 6.12% | 3.70% | -6.17% | 1.29 | 41.97% | 0.45 | 4.29% | 76.43% |
| Semiconductor | 72 | 5.38 | 13.71 | 21.66 | 5.01 | 97.09 | 24.62% | 17.00% | 20.29% | 8.35% | 0.71 | 14.08% | 1.24 | 7.99% | 43.91% |
| Semiconductor Equip | 39 | 4.00 | 15.71 | 20.43 | 5.85 | 39.73 | 19.22% | 22.14% | 27.65% | 5.31% | 1.23 | 13.52% | 1.25 | 7.94% | 29.20% |
| Shipbuilding & Marine | 10 | 1.98 | 11.32 | 23.31 | 1.34 | 25.13 | 7.41% | 6.02% | 2.69% | 9.78% | 0.76 | 22.82% | 1.57 | 9.37% | 32.11% |
| Shoe | 11 | 3.55 | 22.08 | 29.03 | 12.21 | 23.09 | 12.47% | 30.57% | 40.16% | 3.12% | 2.91 | 15.30% | 0.83 | 6.11% | 26.78% |
| Software (Entertainment) | 86 | 6.76 | 20.60 | 30.27 | 5.12 | 33.98 | 22.64% | 17.01% | 18.49% | 13.53% | 0.71 | 18.77% | 1.29 | 8.40% | 0.00% |
| Software (Internet) | 30 | 7.64 | 20.23 | 58.76 | 9.39 | 66.75 | 9.15% | 11.12% | 6.14% | 30.92% | 1.02 | 15.35% | 1.50 | 9.29% | 2.58% |
| Software (System & Application) | 363 | 8.77 | 24.00 | 35.62 | 9.92 | 110.90 | 22.25% | 20.03% | 27.91% | 15.04% | 0.85 | 11.24% | 1.15 | 7.67% | 30.55% |
| Steel | 32 | 0.70 | 6.24 | 8.90 | 1.44 | 14.34 | 7.75% | 16.31% | 18.41% | 2.29% | 2.29 | 18.28% | 1.29 | 7.82% | 19.66% |
| Telecom (Wireless) | 18 | 2.43 | 6.64 | 23.87 | 1.54 | 25.66 | 10.39% | 5.65% | 1.15% | 3.48% | 0.59 | 25.25% | 0.60 | 4.96% | 13.80% |
| Telecom. Equipment | 91 | 3.50 | 13.42 | 17.72 | 5.00 | 57.04 | 19.28% | 20.70% | 17.58% | 4.86% | 1.06 | 21.98% | 0.84 | 6.01% | 53.31% |
| Telecom. Services | 67 | 2.85 | 7.93 | 15.74 | 2.13 | 742.09 | 18.29% | 13.05% | 5.67% | 10.08% | 0.76 | 18.21% | 0.67 | 5.33% | 170.56% |
| Tobacco | 17 | 5.19 | 12.30 | 13.16 | 89.12 | 24.30 | 39.34% | 54.11% | -0.05% | 3.84% | 1.55 | 29.89% | 1.43 | 8.83% | 143.69% |
| Transportation | 18 | 1.35 | 12.39 | 27.53 | 4.93 | 58.53 | 5.04% | 10.45% | 21.61% | 14.35% | 2.45 | 21.53% | 0.96 | 6.51% | 59.98% |
| Transportation (Railroads) | 8 | 6.32 | 12.56 | 16.55 | 4.91 | 20.48 | 38.69% | 15.44% | 23.44% | 0.08% | 0.46 | 23.38% | 1.89 | 11.17% | 33.86% |
| Trucking | 33 | 1.93 | 9.08 | NA | 2.81 | 18.36 | -4.62% | 0.33% | -32.07% | 12.98% | 1.14 | 26.64% | 1.04 | 6.74% | 0.14% |
| Utility (General) | 16 | 4.26 | 14.13 | 24.65 | 2.11 | 23.72 | 17.45% | 6.63% | 11.07% | 2.27% | 0.44 | 14.43% | 0.19 | 2.85% | 75.43% |
| Utility (Water) | 17 | 8.83 | 19.02 | 29.10 | 3.34 | 48.13 | 30.26% | 7.87% | 13.63% | 7.54% | 0.29 | 22.26% | 0.57 | 4.57% | 66.60% |
| Total Market | 7053 | 3.16 | 17.54 | 28.99 | 3.21 | 70.85 | 10.70% | 7.31% | 13.63% | 10.15% | 0.73 | 18.57% | 0.83 | 5.94% | 45.97% |
| Total Market (without financials) | 5878 | 2.62 | 13.75 | 22.97 | 3.89 | 76.83 | 11.15% | 12.96% | 13.30% | 10.53% | 1.22 | 18.43% | 1.01 | 6.90% | 52.42% |
**Worked example:** A specialty chemicals company earns a pre-tax operating margin of 18% against the industry's 12.57%, with an after-tax ROC of 20% against the industry's 12.93%. The industry trades at EV/EBITDA 10.56 and EV/Sales 2.09. Both of the firm's companion variables beat the industry by roughly 40-55%, so pricing it at the industry average would understate it. The EV/Sales route makes the adjustment transparent: EV/Sales scales roughly with the after-tax operating margin, so a firm with a margin 43% above its industry supports something closer to 2.09 × 1.43 ≈ 3.0 times sales, before controlling for growth and reinvestment differences.

**Determinism:** DETERMINISTIC — every lookup, and every ratio computed from a company's financials for comparison against the industry row. Scaling a sector multiple by a companion-variable ratio is mechanical once the rule is fixed. JUDGMENT — assigning a company to an industry, deciding whether the industry average is contaminated by outliers or NA entries, deciding whether the firm's own margin/ROE is sustainable, and choosing which multiple to lead with.

**Pitfalls:**
- These are averages, not medians. Multiples are right-skewed, so several trailing PE entries are wildly inflated by a handful of near-zero-earnings firms. Environmental & Waste Services shows 735, Retail (Distributors) 897, Telecom Services 742, Metals & Mining 727. Do not use those as sector anchors.
- NA entries are informative. Banks, brokerages and non-bank financials have no meaningful EV/EBITDA or reinvestment rate.
- Negative or near-zero companion variables (Trucking's negative pre-tax operating margin, Electronics Consumer & Office's negative ROE) reflect a bad year, not the long-run economics. Normalize first.
- Reading a multiple without its companion variable. That is the error the whole dataset exists to prevent.
- Using a single year's table for a cyclical industry near a peak or a trough.
- Mixing this US dataset with a non-US company. Use the regional regressions instead ([[cross-market-multiple-regressions]]).

**Sources:**
- tables (January 2022 US industry averages: all columns above)
- valpacket2spr21 p.13-19, p.51-54 (why sector multiples need companion variables)
- valpacket2spr20 p.13-19, p.51-54

**Related:** [[multiple-distribution-statistics]], [[comparable-selection-and-controls]], [[sector-regressions]], [[cross-market-multiple-regressions]], [[ev-ebitda-multiple]], [[ev-sales-and-brand-value]], [[book-value-multiples]], [[intrinsic-multiple-derivation]], [[sum-of-the-parts]]
