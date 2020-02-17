#!/usr/bin/env python3
from urllib import request, error
from typing import Dict, List, Any
from datetime import datetime
import os
import json
import csv
import sys

import matplotlib.pyplot as plt  # type: ignore


def request_data() -> List[Dict[str, Any]]:

    url = "https://strims.gg/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    }

    try:
        response = request.urlopen(request.Request(url=url, data=None, headers=headers))
    except error.HTTPError as err:
        raise Exception(f"{err.code}: {err.reason}")

    data = json.loads(response.read()).get("stream_list")
    assert data, "failed to get stream_list"

    strims = [
        strim
        for strim in data
        if strim.get("hidden") == False
        and strim.get("afk") == False
        and strim.get("nsfw") == False
        and strim.get("service") == "angelthump"
    ]

    useless_filed = [
        "live",
        "nsfw",
        "hidden",
        "afk",
        "promoted",
        "service",
        "title",
        "thumbnail",
        "url",
    ]

    for strim in strims:
        for key in strim.copy():
            if key in useless_filed:
                strim.pop(key)

    return strims


def main(opt: str) -> None:
    if opt == "dl":
        exists = os.path.isfile("data.csv")
        with open("data.csv", "a+") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=["rustlers", "afk_rustlers", "channel", "viewers", "time"],
            )

            if exists is False:
                writer.writeheader()

            for row in request_data():
                row["time"] = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
                writer.writerow(row)
    elif opt == "plot":
        time: List = []
        viewers: List = []
        with open("data.csv", "r") as csvfile:
            plots = csv.reader(csvfile, delimiter=",")
            # build up data into lists

        plt.plot(time, viewers, label="test")
        plt.xlabel("time")
        plt.ylabel("viewers")
        plt.title("Viewer count over time")
        plt.legend()
        plt.show()
    else:
        print(f"{opt} is not recognized")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SyntaxError("not enough arguments supplied")

    main(sys.argv[1])
