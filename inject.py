import argparse
import json
from influxdb import InfluxDBClient
from datetime import datetime


def setupdb_send(payload):
    client = InfluxDBClient("localhost", 8086, "admin", "Password1", "db0")
    # client.create_database('result')
    # client.get_list_database()
    client.switch_database("result")
    client.write_points(payload)
    out = client.query("select * from patch;")
    return out


def frmt(data):
    json_payload = []
    for i in data:
        load = {
            "measurement": "patch",
            "tags": {"name": i["name"]},
            "time": datetime.now(),
            "fields": i,
        }
        json_payload.append(load)
    return json_payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonfile")
    args = parser.parse_args()
    with open(args.jsonfile, "r") as f:
        data = json.load(f)

    payload = frmt(data)
    put = setupdb_send(payload)
    print(put)


if __name__ == "__main__":
    main()
