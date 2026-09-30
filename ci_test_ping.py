#!/usr/bin/env python3
"""Send a test notification to each configured topic (CI helper).

Backs the "test_ping" input of .github/workflows/check.yml. It goes through the
same notify() path real alerts use, so a green run proves the whole chain --
secrets, per-target topic routing, and ntfy delivery -- rather than just proving
that curl can reach a URL.
"""

import os
import sys

import stock_notifier as core

SITE = "https://itzzedwin.github.io/card-stock-notifier/"
TOPICS = [("One Piece", "NTFY_TOPIC_ONEPIECE")]


def main():
    delivered, configured = [], 0
    for label, var in TOPICS:
        topic = (os.environ.get(var) or "").strip()
        if not topic:
            print(f"::warning::{var} is not set - {label} test skipped")
            continue
        configured += 1
        sent = core.notify(
            {"notifications": {}},
            {"name": f"Test - {label}", "url": SITE, "ntfy_topic": topic},
            title=f"Test - the cloud watcher can reach you ({label})",
            body=f"This came from GitHub's servers, so real {label} "
                 f"pings arrive the same way.")
        print(f"{label}: {'sent via ' + ', '.join(sent) if sent else 'DELIVERY FAILED'}")
        if sent:
            delivered.append(label)

    if not configured:
        sys.exit("NTFY_TOPIC_ONEPIECE is not set - add it under "
                 "Settings > Secrets and variables > Actions.")
    if not delivered:
        sys.exit("Every test notification failed to send - see the errors above.")
    print("delivered to:", ", ".join(delivered))


if __name__ == "__main__":
    main()
