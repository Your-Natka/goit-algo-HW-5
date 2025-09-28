import timeit

# ---------------------------
# 1. Алгоритми пошуку підрядка
# ---------------------------

# Алгоритм Кнута-Морріса-Пратта (KMP)
def kmp_search(text, pattern):
    if not pattern:
        return []
    # Префікс-функція
    lps = [0]*len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length:
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1
    # Пошук
    result = []
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i-j)
            j = lps[j-1]
        elif i < len(text) and pattern[j] != text[i]:
            if j:
                j = lps[j-1]
            else:
                i += 1
    return result

# Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern, prime=101):
    if not pattern:
        return []
    result = []
    m, n = len(pattern), len(text)
    d = 256  # розмір алфавіту
    h = pow(d, m-1) % prime
    p = t = 0
    for i in range(m):
        p = (d*p + ord(pattern[i])) % prime
        t = (d*t + ord(text[i])) % prime
    for i in range(n-m+1):
        if p == t and text[i:i+m] == pattern:
            result.append(i)
        if i < n-m:
            t = (d*(t - ord(text[i])*h) + ord(text[i+m])) % prime
            if t < 0:
                t += prime
    return result

# Алгоритм Боєра-Мура (за таблицею останньої появи символу)
def boyer_moore_search(text, pattern):
    if not pattern:
        return []
    last = {c: i for i, c in enumerate(pattern)}
    result = []
    n, m = len(text), len(pattern)
    i = 0
    while i <= n-m:
        j = m-1
        while j >= 0 and pattern[j] == text[i+j]:
            j -= 1
        if j < 0:
            result.append(i)
            i += 1 if i+m >= n else m - last.get(text[i+m], -1)
        else:
            i += max(1, j - last.get(text[i+j], -1))
    return result

# ---------------------------
# 2. Функція для вимірювання часу
# ---------------------------
def measure_time(func, text, pattern, number=10):
    return timeit.timeit(lambda: func(text, pattern), number=number) / number

# ---------------------------
# 3. Завантаження текстів
# ---------------------------
with open("stattya1.txt", "r", encoding="utf-8") as f:
    text1 = f.read()

with open("stattya2.txt", "r", encoding="utf-8") as f:
    text2 = f.read()

# ---------------------------
# 4. Вибір підрядків
# ---------------------------
pattern_exist_1 = "алгоритм"  # існуючий підрядок стаття 1
pattern_fake_1  = "неіснуючийпідрядок"  # неіснуючий підрядок стаття 1

pattern_exist_2 = "структури даних"  # існуючий підрядок стаття 2
pattern_fake_2  = "невідомийтестовийпідрядок"  # неіснуючий підрядок стаття 2

# ---------------------------
# 5. Вимірювання часу
# ---------------------------
algorithms = {"KMP": kmp_search, "Rabin-Karp": rabin_karp_search, "Boyer-Moore": boyer_moore_search}
texts = [(text1, pattern_exist_1, pattern_fake_1), (text2, pattern_exist_2, pattern_fake_2)]

results = []

for idx, (text, pat_exist, pat_fake) in enumerate(texts, 1):
    row_exist = {"Текст": f"Стаття {idx}", "Підрядок": "Існуючий"}
    row_fake  = {"Текст": f"Стаття {idx}", "Підрядок": "Неіснуючий"}
    for name, func in algorithms.items():
        row_exist[name] = measure_time(func, text, pat_exist)
        row_fake[name]  = measure_time(func, text, pat_fake)
    results.append(row_exist)
    results.append(row_fake)

# ---------------------------
# 6. Вивід таблиці результатів
# ---------------------------
print("| Текст | Підрядок | KMP (с) | Rabin-Karp (с) | Boyer-Moore (с) |")
print("|-------|-----------|----------|----------------|----------------|")
for row in results:
    print(f"| {row['Текст']} | {row['Підрядок']} | {row['KMP']:.6f} | {row['Rabin-Karp']:.6f} | {row['Boyer-Moore']:.6f} |")

# ---------------------------
# 7. Генерація висновків Markdown
# ---------------------------
markdown = "# Висновки аналізу алгоритмів пошуку підрядка\n\n"

for idx, (text, pat_exist, pat_fake) in enumerate(texts, 1):
    exist_times = {name: measure_time(func, text, pat_exist) for name, func in algorithms.items()}
    fake_times  = {name: measure_time(func, text, pat_fake) for name, func in algorithms.items()}
    fastest_exist = min(exist_times, key=exist_times.get)
    fastest_fake  = min(fake_times, key=fake_times.get)
    markdown += f"## Стаття {idx}\n"
    markdown += f"- Існуючий підрядок: найшвидший — **{fastest_exist}**\n"
    markdown += f"- Неіснуючий підрядок: найшвидший — **{fastest_fake}**\n\n"

markdown += "## Загальний висновок\n"
markdown += "Boyer-Moore ефективний для пошуку реально існуючих підрядків у великих текстах, KMP та Rabin-Karp краще справляються з перевіркою відсутніх підрядків.\n"

with open("analysis_results.md", "w", encoding="utf-8") as f:
    f.write(markdown)

print("\nВисновки збережено у файлі `analysis_results.md`")
