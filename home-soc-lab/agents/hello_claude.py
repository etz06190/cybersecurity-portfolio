"""
hello_claude.py — verify the Anthropic API key works.

Day 3 of Week 1 sanity check.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python hello_claude.py

Expected output:
    A brief greeting from Claude confirming the API is responsive.

If you get an authentication error: check that ANTHROPIC_API_KEY is
exported and not just set in the current shell. Run `echo $ANTHROPIC_API_KEY`
to verify.

If you get a rate limit error: you may have hit the spending limit.
Check console.anthropic.com → Settings → Billing.
"""

import os
import sys

try:
    from anthropic import Anthropic
except ImportError:
    print("Install the SDK first:  pip install anthropic")
    sys.exit(1)

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("ANTHROPIC_API_KEY is not set. Export it first:")
    print('    export ANTHROPIC_API_KEY="sk-ant-..."')
    sys.exit(1)

client = Anthropic()  # reads ANTHROPIC_API_KEY automatically

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "Hello, are you working? Respond in one sentence."}
    ],
)

print("Response from Claude:")
print(response.content[0].text)
print()
print(f"Input tokens:  {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
