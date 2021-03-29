#! /usr/bin/env python3
import argparse
import requests

log_types = {
    "analytic": {
        "file_name": "./analytics.json",
        "tag": "goliath.production.events",
    },
    "client": {
        "file_name": "./client_logs.json",
        "tag": "goliath.production.errors",
    },
    "feature": {
        "file_name": "./features.json",
        "tag": "goliath.production.features",
    },
    "match": {
        "file_name": "./match_requests.json",
        "tag": "goliath.production.logs",
    },
    "offer": {
        "file_name": "./offers.json",
        "tag": "goliath.production.offers",
    },
    "offer_ev": {
        "file_name": "./offer_events.json",
        "tag": "goliath.production.offer_events",
    },
    "order": {
        "file_name": "./orders.json",
        "tag": "production.raw_orders",
    },
    "pi": {
        "file_name": "./product_interactions.json",
        "tag": "goliath.production.product_interactions",
    },
    "pred": {
        "file_name": "./predictions.json",
        "tag": "goliath.production.pred",
    },
    "recommendation": {
        "file_name": "./recommendations.json",
        "tag": "goliath.production.recommendations",
    },
    "session": {
        "file_name": "./sessions.json",
        "tag": "goliath.production.sessions",
    },
    "site_ev": {
        "file_name": "./site_events.json",
        "tag": "goliath.production.site_events",
    },
}

hostname = "localhost"
ports = [8888, 8889, 8890]

def post_logs(file_name, hostname, ports, tag):
    port_loop = looper(ports)
    with open(file_name) as log_file:
        for json in log_file:
            requests.post(endpoint(hostname, next(port_loop), tag), data = {'json':json} )

def endpoint(hostname, port, tag):
    return f"http://{hostname}:{port}/{tag}"

def looper(ports):
    port_idx = 0
    while True:
        yield ports[port_idx]
        port_idx = (port_idx + 1) % len(ports)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post some logs")
    parser.add_argument('log_type', metavar="log-type", type=str, help="type of log")
    args = parser.parse_args()
    if args.log_type not in log_types:
        print(f"Use a valid log type: {', '.join([lt for lt in log_types])}")
        quit()
    info = log_types.get(args.log_type)

    post_logs(info["file_name"], hostname, ports, info["tag"])
