import timeit
import pandas as pd

# ---------------------------
# 1. Алгоритми пошуку підрядка
# ---------------------------

# Алгоритм Кнута-Морріса-Пратта (KMP)
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    
    # Префіксна функція
    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    # Основний пошук
    result = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            result.append(i - m + 1)
            j = lps[j - 1]
    return result

# Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern, base=256, mod=101):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    hpattern = 0
    htext = 0
    h = 1

    for _ in range(m - 1):
        h = (h * base) % mod

    for i in range(m):
        hpattern = (base * hpattern + ord(pattern[i])) % mod
        htext = (base * htext + ord(text[i])) % mod

    result = []
    for i in range(n - m + 1):
        if hpattern == htext:
            if text[i:i + m] == pattern:
                result.append(i)
        if i < n - m:
            htext = (base * (htext - ord(text[i]) * h) + ord(text[i + m])) % mod
            htext = (htext + mod) % mod
    return result

# Алгоритм Боєра-Мура (за таблицею останньої появи символу)
def boyer_moore_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    skip = {pattern[i]: i for i in range(m)}
    result = []

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            result.append(i)
            i += m if i + m < n else 1
        else:
            i += max(1, j - skip.get(text[i + j], -1))
    return result

# ------------------ Експеримент ------------------

def measure(text, pattern, algo, algo_name):
    time = timeit.timeit(lambda: algo(text, pattern), number=10)
    return {"algorithm": algo_name, "pattern": pattern, "time": time}


def run_experiment(text1, text2, patterns):
    results = []
    algos = [
        (kmp_search, "KMP"),
        (boyer_moore_search, "Boyer-Moore"),
        (rabin_karp_search, "Rabin-Karp")
    ]

    for text, tname in [(text1, "Стаття 1"), (text2, "Стаття 2")]:
        for pattern in patterns:
            for algo, name in algos:
                res = measure(text, pattern, algo, name)
                res["text"] = tname
                results.append(res)

    return pd.DataFrame(results)

# ------------------ Запуск ------------------

if __name__ == "__main__":
    # Приклад текстів
    with open("stattya1.txt", "r", encoding="utf-8") as f:
        text1 = f.read()
    with open("stattya2.txt", "r", encoding="utf-8") as f:
        text2 = f.read()

    # Підрядки: один реальний, один вигаданий
    patterns = ["алгоритм", "вигаданийпідрядок"]

    df = run_experiment(text1, text2, patterns)
    print(df.to_markdown(index=False))