# Multi-Agent System

A supervisor-routed LangGraph multi-agent system.

## Structure

```
multi_agent_system/
├── config.py            # LLM setup (reads OPENAI_API_KEY / OPENAI_API_BASE)
├── tools/
│   ├── gold.py           # get_gold_price
│   ├── news.py           # get_usa_news
│   ├── weather.py        # get_weather  
│   └── crypto.py         # get_crypto_price
├── agents_pkg/
│   └── __init__.py       # AGENT_SPECS registry + build_agents()
├── supervisor.py         # Routing node, prompt built from AGENT_SPECS
├── graph.py               # Builds the LangGraph StateGraph
├── main.py                # CLI entrypoint
└── README.md
```

## Run it

```bash
export OPENAI_API_KEY="your-key"          # required
export OPENAI_API_BASE="https://opencode.ai/zen/go/v1"  # optional, has a default
python main.py
```

## Agents included

| Agent | Tool | Notes |
|---|---|---|
| Gold_Agent | `get_gold_price` | goldprice.org, no key needed |
| News_Agent | `get_usa_news` | Google News RSS, no key needed |
| Weather_Agent | `get_weather(city)` | Open-Meteo, no key needed |
| Crypto_Agent | `get_crypto_price(coin)` | CoinGecko, no key needed |

## How to add another agent

1. Create `tools/<name>.py` with an `@tool`-decorated function, and export
   it from `tools/__init__.py`.
2. Add one entry to `AGENT_SPECS` in `agents_pkg/__init__.py`:

```python
{
    "name": "Stock",
    "tools": [get_stock_price],
    "system_prompt": "You are a stock market specialist. ...",
},
```

That's it — the supervisor's routing prompt and the graph's nodes/edges
are generated from `AGENT_SPECS` automatically. No changes needed in
`supervisor.py`, `graph.py`, or `main.py`.

