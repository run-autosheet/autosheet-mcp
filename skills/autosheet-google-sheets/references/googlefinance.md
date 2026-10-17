# GOOGLEFINANCE reference

How to ask the Autosheet agent for market data with =GOOGLEFINANCE(), and how to read the results. The agent writes and checks the formulas, so use this reference to give it the exact ticker and attribute, and to interpret what it reports.

## When to use the function

- The user wants a live or historical market value in the spreadsheet: a price, a market cap, an exchange rate, a P/E ratio, a 52-week high, or a series of closing prices.
- The value should keep updating on its own after the conversation ends.

Do not leave the formula in place when the user wants a fixed snapshot for a report. Instead, ask the agent to write the number as a plain value (see "Snapshots" under "Asking the agent").

Do not use the function for data it cannot return: dividend history, adjusted close, intraday bars, options, bonds, or earnings dates. Tell the user and offer the nearest attribute.

## Syntax

```text
=GOOGLEFINANCE(ticker, [attribute], [start_date], [end_date|num_days], [interval])

```

| Argument | Meaning |
| --- | --- |
| ticker | Text. Prefer "EXCHANGE:SYMBOL", for example "NASDAQ:GOOG". A bare "GOOG" works, but Google picks the exchange, which is sometimes the wrong listing. |
| attribute | Text, case-insensitive. Defaults to "price". See the attribute tables below. |
| start_date | Date. Supplying it switches the call to historical mode, and the result becomes a table. |
| end_date or num_days | Date, or a number of days counted from start_date. Omit it to get a single day. |
| interval | "DAILY" or "WEEKLY" (also accepted as 1 or 7). Historical mode only. |

Only the first argument is required. Arguments are positional, so when giving dates, also give the attribute, for example "price" or "close".

## Ticker formats

| Asset | Ticker | Example |
| --- | --- | --- |
| Stock / ETF | EXCHANGE:SYMBOL | "NASDAQ:AAPL", "NYSE:BRK.B", "NYSEARCA:SPY", "LON:VOD", "EPA:MC", "ETR:SAP", "TYO:7203", "TSE:SHOP" (Toronto), "HKG:0700", "ASX:BHP", "NSE:RELIANCE" |
| Index | INDEX…:.SYMBOL | "INDEXSP:.INX" (S&P 500), "INDEXDJX:.DJI", "INDEXNASDAQ:.IXIC" |
| Currency pair | CURRENCY:FROMTO | "CURRENCY:USDEUR" (how many EUR one USD buys) |
| Crypto | CURRENCY:COINFIAT | "CURRENCY:BTCUSD", "CURRENCY:ETHEUR" (coverage is partial) |

If the exchange is uncertain, check it on Google Finance (https://www.google.com/finance), or ask the agent to: The URL of a quote page ends in SYMBOL:EXCHANGE, so flip it. London (LON:) prices are quoted in pence (GBX). Divide by 100 for pounds.

## Real-time attributes

These return a single value. Quotes are delayed up to 20 minutes and are not available for every market. The datadelay attribute gives the delay for a symbol.

| Attribute | Returns |
| --- | --- |
| price | Last trade price (default) |
| priceopen | Opening price for the current session |
| high, low | Session high / low |
| volume | Shares traded this session |
| volumeavg | Average daily volume |
| marketcap | Market capitalization, in the listing currency |
| pe | Price / earnings ratio |
| eps | Earnings per share |
| high52, low52 | 52-week high / low |
| change, changepct | Change since previous close, absolute / percent |
| closeyest | Previous close |
| beta | Beta |
| shares | Shares outstanding |
| currency | Currency the security is priced in (text, for example USD) |
| tradetime | Timestamp of the last trade |
| datadelay | Quote delay in minutes |

Not every attribute exists for every symbol. Indices have no marketcap, pe, eps, or shares. For currency pairs, use price for exchange rates. Google documents open, low, high, and volume as unsupported for currencies; do not request those attributes. A missing attribute returns #N/A.

## Historical attributes

These are available once start_date is set. The result is a spilled table with a header row: Date in the first column, followed by the requested columns. Only trading days appear.

| Attribute | Columns returned |
| --- | --- |
| open, close, high, low, volume | Date, then that one series |
| price | Same as close in historical mode |
| all | Date, Open, High, Low, Close, Volume |

```text
=GOOGLEFINANCE("NASDAQ:GOOG", "close", DATE(2025,1,2), DATE(2025,3,31), "DAILY")
=GOOGLEFINANCE("NASDAQ:GOOG", "all",   TODAY()-365, TODAY(), "WEEKLY")
=GOOGLEFINANCE("NASDAQ:GOOG", "close", DATE(2025,1,2), 30)
=GOOGLEFINANCE("CURRENCY:USDEUR", "price", DATE(2025,1,1), DATE(2025,1,31))

```

The third example covers 30 days from the start date.

A single-day request still returns a two-row table (header plus one row). If that day was not a trading day, it returns #N/A. Ask for a wider range and the last row instead.

## Mutual funds

Google's [GOOGLEFINANCE documentation](https://support.google.com/docs/answer/3093281) states that mutual fund attributes are currently unsupported in Google Sheets. Do not generate mutual fund attribute formulas. Explain the limitation and use another source, such as the fund provider's published data or data supplied by the user, for fund returns, yields, fees, and similar values.

## Recipes

When the user wants one of these, include the formula in your prompt to the agent.

Single value without the header row:

```text
=INDEX(GOOGLEFINANCE("NASDAQ:GOOG", "close", DATE(2025,1,2)), 2, 2)

```

Most recent close before today (skips weekends and holidays):

```text
=INDEX(GOOGLEFINANCE("NASDAQ:GOOG", "close", TODAY()-7, TODAY()), ROWS(GOOGLEFINANCE("NASDAQ:GOOG", "close", TODAY()-7, TODAY())), 2)

```

Convert an amount using a live rate, with the source currency code in B2 (for example "USD") and the target currency code in C2 (for example "EUR"):

```text
=A2 * GOOGLEFINANCE("CURRENCY:" & B2 & C2)

```

Sparkline of the trading days within the last 30 calendar days:

```text
=SPARKLINE(INDEX(GOOGLEFINANCE("NASDAQ:GOOG", "price", TODAY()-30, TODAY()), 0, 2))

```

Average close over a period:

```text
=AVERAGE(INDEX(GOOGLEFINANCE("NASDAQ:GOOG", "close", TODAY()-90, TODAY()), 0, 2))

```

Watchlist: Ask the agent to put tickers in column A and fill one formula per row.

```text
A         B                          C                                D
Ticker    Price                      Change %                         Market cap
NASDAQ:AAPL  =GOOGLEFINANCE(A2,"price")  =GOOGLEFINANCE(A2,"changepct")/100  =GOOGLEFINANCE(A2,"marketcap")

```

changepct is already a percentage number (1.5 means 1.5%), so divide it by 100 if the column uses a percent number format.

## Asking the agent

- Give the exact ticker. Use an explicit exchange prefix. If the user gives only a bare symbol and the company has several listings, ask the user which one they mean, or ask the agent to look it up.
- Use only the attributes listed above. If the user asks for something outside them, such as dividend yield for a stock, an earnings date, or a sector, explain the limitation instead of asking for a formula that will return #N/A.
- One formula per ticker. GOOGLEFINANCE does not accept a range of tickers, and wrapping it in ARRAYFORMULA does not help. Ask the agent to write one formula per ticker and fill down.
- Keep historical tables isolated. A historical result needs empty cells below and to the right, or it shows #REF! ("Array result was not expanded"). Ask the agent to put it on its own sheet or below all other data, and not to write anything into the area it spills into. To get a single value, ask for INDEX (see "Recipes").
- Compute from historical data in the spreadsheet. Ask for formulas such as INDEX, AVERAGE, QUERY, or SPARKLINE on top of the historical table, not for the agent to read the table and calculate from it. The agent cannot read historical results (see "Reading the agent's report").
- Put formulas where the data is needed. Pulling cells with GOOGLEFINANCE formulas into another spreadsheet with IMPORTRANGE is unreliable, for the same reason that historical results show as #N/A to the agent (see "Reading the agent's report"). Ask the agent to put the formula in the destination spreadsheet instead.
- Snapshots. If the user needs values that must not change, such as for invoices or month-end reports, ask the agent to write plain numbers instead of formulas. For historical data, the agent may not be able to do this, because it cannot read those results. In that case, tell the user to copy the cells and paste them as values.
- Formatting. Ask for a currency number format on price columns, a percent format on changepct/100, and a date-time format on tradetime.

## Reading the agent's report

- Historical results show as #N/A to the agent. Google documents that historical GOOGLEFINANCE results cannot be read through the Sheets API or Apps Script, so the agent sees #N/A even when the values display correctly in the spreadsheet. Treat this as expected, not as a broken formula, and ask the user to confirm that the spreadsheet shows the values. Real-time attributes read back normally.
- #N/A on a real-time value means the request is wrong. The ticker or exchange prefix is wrong, the symbol was delisted or renamed, or the attribute is not available for that symbol. Correct the ticker or attribute and ask the agent to change the formula. Do not ask it to retry the same formula.
- Loading... or blank cells right after writing. Google Sheets is still fetching the data, which usually takes a few seconds. Ask the agent to check again before concluding anything.
- Values do not update on request. Real-time values recalculate on Google's schedule, roughly every 20 minutes while the spreadsheet is open. Neither you nor the agent can force a refresh, and the spreadsheet's recalculation setting does not apply to this function.
- Historical prices are not adjusted for splits or dividends.
- Currency follows the listing exchange, not the user's locale. When mixing exchanges, ask for the currency attribute or a conversion with a CURRENCY: pair.
- Tell the user about the delay. When presenting prices, mention that quotes are delayed up to 20 minutes. Do not describe them as real-time.
