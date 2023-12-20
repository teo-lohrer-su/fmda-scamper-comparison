from multiprocessing import Pool
from pathlib import Path
import json
import random
from typing import Optional
import networkx as nx
from dataclasses import dataclass
from functools import cache, partial
from collections.abc import Iterator
from tqdm.autonotebook import tqdm


class ScanType:
    SCAMPER = "scamper"
    FMDA = "fmda"


@dataclass
class Scan:
    scan_id: str
    type: ScanType
    source: str
    destination: str
    data: dict
    graph: nx.DiGraph

    def nodes(self) -> set[str]:
        return set(n for n in self.graph.nodes if not n.startswith("*"))

    def all_nodes(self) -> set[str]:
        return set(self.graph.nodes)


@cache
def scan_from_file(file: Path, type: ScanType) -> Scan:
    scan_id = file.stem
    data = []

    with file.open() as f:
        for line in f:
            if line.startswith("{"):
                data.append(json.loads(line))

    g = nx.DiGraph()

    trace = data[1]
    source = trace["src"]
    destination = trace["dst"]
    edges = []

    for node in trace["nodes"]:
        start = node["addr"]
        for link in node["links"]:
            for l in link:
                if l["addr"] != "*":
                    end = l["addr"]
                else:
                    end = f"*_{random.randint(0, 100000000)}"
                edges.append((start, end))

    g.add_edges_from(edges)
    return Scan(scan_id, type, source, destination, trace, g)


def try_scan_from_file(file: Path, type: ScanType) -> Optional[Scan]:
    try:
        return scan_from_file(file, type)
    except Exception as e:
        # print(file, e)
        return None


def load_files(files: Iterator[str], type: ScanType) -> Iterator[Scan]:
    with Pool() as p:
        res = list(tqdm(
            p.imap(
                partial(try_scan_from_file, type=type),
                map(Path, files)
            ),
            total=len(files)
        ))
    return filter(None, res)
