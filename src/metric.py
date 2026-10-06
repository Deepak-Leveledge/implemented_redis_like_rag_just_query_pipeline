# ==========================================
# Simple Cache Metrics
# ==========================================


metrics = {
    "exact_hits": 0,
    "exact_misses": 0,
    "semantic_hits": 0,
    "semantic_misses": 0,
}


def record_exact_hit():
    metrics["exact_hits"]+=  1

def record_exact_miss():
    metrics["exact_misses"]+= 1

def record_semantic_hit():
    metrics["semantic_hits"]+=  1

def record_semantic_miss():
    metrics["semantic_misses"]+= 1



def get_metrics():

    #adding up both cache

    exact_total = (
        metrics["exact_hits"]
        + metrics["exact_misses"]
    )

    semantic_total = (
        metrics["semantic_hits"]
        + metrics["semantic_misses"]
    )

    exact_hit_rate = (
        metrics["exact_hits"] / exact_total * 100
        if exact_total
        else 0
    )

    semantic_hit_rate = (
        metrics["semantic_hits"] / semantic_total * 100
        if semantic_total
        else 0
    )


    return {
        "exact_hits": metrics["exact_hits"],
        "exact_misses": metrics["exact_misses"],
        "exact_hit_rate": round(
            exact_hit_rate, 2
        ),

        "semantic_hits": metrics["semantic_hits"],
        "semantic_misses": metrics["semantic_misses"],
        "semantic_hit_rate": round(
            semantic_hit_rate, 2
        ),
    }


def print_metrics():


    data = get_metrics()

    print("\n")
    print("=" * 60)
    print("CACHE METRICS")
    print("=" * 60)

    print(
        "Exact Hits:",
        data["exact_hits"]
    )

    print(
        "Exact Misses:",
        data["exact_misses"]
    )

    print(
        "Exact Hit Rate:",
        f"{data['exact_hit_rate']}%"
    )

    print()

    print(
        "Semantic Hits:",
        data["semantic_hits"]
    )

    print(
        "Semantic Misses:",
        data["semantic_misses"]
    )

    print(
        "Semantic Hit Rate:",
        f"{data['semantic_hit_rate']}%"
    )